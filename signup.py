from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter as tk
import pyodbc
from userfeed import  UserMFeed
from tkinter import messagebox
from dbcon import DatabaseConnection
class SignupPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry('1260x700')
        self.title('Signup Page')
        self.create_widgets()

        self.db = DatabaseConnection()
        self.connection = self.db.create_connection()

    def sign_user(self):
        username = self.username_ent.get()
        password = self.password_e.get()
        email = self.email_entry.get()
        is_admin = self.is_adminvar.get()  # 1 if checked, 0 if unchecked

        if username and password and email:
            try:
                cursor = self.connection.cursor()
                cursor.execute("""
                    INSERT INTO [User] (Username, Password, Email, isAdmin)
                    OUTPUT INSERTED.UserID
                    VALUES (?, ?, ?, ?)
                """, (username, password, email, is_admin))
                user_id = cursor.fetchone()[0]

                self.connection.commit()

                tk.messagebox.showinfo("Success", f"Registered successfully.")
                self.withdraw()
                # No need to check isAdmin or access Admin table since isAdmin is in User table
                signup_user_feed = UserMFeed(self.parent, username)
                signup_user_feed.mainloop()
            except pyodbc.Error as e:
                tk.messagebox.showinfo("Error", f"fill all field.")

        else:
            tk.messagebox.showinfo("Error", f"fill all field.")

    # Other methods remain unchanged

    def create_widgets(self):
        self.create_labels()
        self.create_entries()
        self.create_buttons()

    def create_labels(self):
        canvas = tk.Canvas(self, width=420, height=378, bg="#fffcfc")
        canvas.place(x=819, y=175)
        tk.Label(self, text="Facebook", font="Arial 43 bold", fg="#427bff").place(x=230, y=210)
        tk.Label(self, text="Facebook helps you connect and share", font="Leelawadee 20", fg="black").place(x=230, y=290)
        tk.Label(self, text="with the people in your life.", font="Leelawadee 20", fg="black").place(x=230, y=323)

    def create_entries(self):
        self.username_ent = tk.Entry(self, width=30, font="Courier", highlightthickness=1)
        self.username_ent.insert(0, 'Username')
        self.username_ent.place(x=880, y=207, height=50)

        self.email_entry = tk.Entry(self, width=30, font="Courier", highlightthickness=1)
        self.email_entry.insert(0, 'Email')
        self.email_entry.place(x=880, y=267, height=50)

        self.password_e = tk.Entry(self, width=30, font="Courier", highlightthickness=1, show="*")
        self.password_e.insert(0, 'Password')
        self.password_e.place(x=880, y=327, height=50)

        self.is_adminvar = tk.IntVar()
        self.is_admin_checkbox = tk.Checkbutton(self, text="Sign up as Admin", variable=self.is_adminvar)
        self.is_admin_checkbox.place(x=880, y=387)

    def create_buttons(self):
        signup_button = tk.Button(self, text='SIGN UP', font=("yu gothic ui", 13, "bold"), width=20, bd=0, bg='#18941f',
                                  cursor='hand2', activebackground='#3047ff', fg='white', command=self.sign_user)
        signup_button.place(x=930, y=447)

        back_button = tk.Button(self, text="Back to Login", command=self.back_to_login, border=0, bg="white", fg="blue",
                                font="Leelawadee 10")
        back_button.place(x=940, y=500)

    def back_to_login(self):
        self.destroy()
        self.parent.deiconify()
