import tkinter as tk
from tkinter import ttk, simpledialog
import pyodbc
from tkinter import messagebox
from datetime import datetime
from userfeed import UserMFeed
from signup import SignupPage
from adminfeed import AdminFeed
from dbcon import DatabaseConnection

class FacebookMainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1280x720')
        self.title('Facebook Login')
        self.create_widgets()
        self.db = DatabaseConnection()
        self.connection = self.db.create_connection()

    def log_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        query = "SELECT UserID, IsAdmin FROM [User] WHERE Username = ? AND Password = ?"
        cursor = self.connection.cursor()
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        if user:
            tk.messagebox.showinfo("Success", f"Login succesful welcome.")

            self.withdraw()
            is_admin = user[1]
            if is_admin:
                admin_feed = AdminFeed(self, username)
                admin_feed.mainloop()
            else:
                user_feed = UserMFeed(self, username)
                user_feed.mainloop()
        else:
            print("Invalid username or password!")
            messagebox.showerror("Error", "invalid usename or pssword")

    def create_widgets(self):
        self.create_labels()
        self.create_entries()
        self.create_buttons()

    def create_labels(self):
        canvas = tk.Canvas(self, width=420, height=378, bg="#dbc9f5", highlightthickness=0)
        canvas.place(x=819, y=175)
        canvas.create_line(28, 260, 400, 260)

        radius = 20

        canvas.create_arc((0, 0, radius * 2, radius * 2), start=90, extent=90, style="arc", outline="",
                          fill="white")  # Top-left
        canvas.create_arc((canvas.winfo_width() - radius * 2, 0, canvas.winfo_width(), radius * 2), start=0, extent=90,
                          style="arc", outline="", fill="white")  # Top-right
        canvas.create_arc((0, canvas.winfo_height() - radius * 2, radius * 2, canvas.winfo_height()), start=180,
                          extent=90, style="arc", outline="", fill="white")  # Bottom-left
        canvas.create_arc((canvas.winfo_width() - radius * 2, canvas.winfo_height() - radius * 2, canvas.winfo_width(),
                           canvas.winfo_height()), start=270, extent=90, style="arc", outline="",
                          fill="white")  # Bottom-right

        canvas.configure(
            bg="white",
            highlightthickness=0,
            relief="ridge",
            width=420,
            height=378,
            bd=2,

        )


        tk.Label(self, text="Facebook", font="Arial 43 bold", fg="#427bff").place(x=230, y=210)
        tk.Label(self, text="Facebook helps you connect and share", font="Leelawadee 20", fg="black").place(x=230,
                                                                                                            y=290)
        tk.Label(self, text="with the people in your life.", font="Leelawadee 20", fg="black").place(x=230, y=323)

    def create_entries(self):

        self.username_entry = tk.Entry(self, width=30, font="Courier", highlightthickness=1)
        self.username_entry.insert(0, 'roomi')
        self.username_entry.place(x=880, y=207, height=50)

        self.password_entry = tk.Entry(self, width=30, font="Courier", highlightthickness=1, show='*')
        self.password_entry.insert(0, 'Password')
        self.password_entry.place(x=880, y=267, height=50)

    def create_buttons(self):
        login_button = tk.Button(self, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=20, bd=0, bg='#427bff',
                                 cursor='hand2', activebackground='#3047ff', fg='white', command=self.log_user)
        login_button.place(x=930, y=340)

        tk.Button(self, text="Forgotten password?", command=self.forgot_password, border=0, bg="white", fg="blue",
                  font="Leelawadee 10").place(x=940, y=400)

        createAcc_button = tk.Button(self, text='Create Account', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                                     bg='#18941f', cursor='hand2', activebackground='#3047ff', fg='white',
                                     command=self.open_signup_page)
        createAcc_button.place(x=930, y=460)

    def forgot_password(self):

        pass

    def open_signup_page(self):
        self.withdraw()
        signup_page = SignupPage(self)
        signup_page.mainloop()
        self.deiconify()