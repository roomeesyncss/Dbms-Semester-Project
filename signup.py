from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter as tk
import pyodbc
from userfeed import UserMFeed
from tkinter import messagebox
from dbcon import DatabaseConnection



class SignupPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry('1260x700')
        self.title('Signup Page')
        self.configure(bg="#f0f2f5")  # Light gray background
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

                # Check if username already exists
                cursor.execute("SELECT COUNT(*) FROM [User] WHERE Username = ?", (username,))
                username_count = cursor.fetchone()[0]
                if username_count > 0:
                    tk.messagebox.showerror("Error", "Username already exists. Please choose a different username.")
                    return

                # Check if email already exists
                cursor.execute("SELECT COUNT(*) FROM [User] WHERE Email = ?", (email,))
                email_count = cursor.fetchone()[0]
                if email_count > 0:
                    tk.messagebox.showerror("Error", "Email already exists. Please use a different email.")
                    return

                # If username and email are unique, insert the new user
                cursor.execute("""
                    INSERT INTO [User] (Username, Password, Email, isAdmin)
                    OUTPUT INSERTED.UserID
                    VALUES (?, ?, ?, ?)
                """, (username, password, email, is_admin))
                user_id = cursor.fetchone()[0]

                self.connection.commit()

                tk.messagebox.showinfo("Success", "Registered successfully.")
                self.withdraw()
                signup_user_feed = UserMFeed(self.parent, username)
                signup_user_feed.mainloop()
            except pyodbc.Error as e:
                tk.messagebox.showerror("Error", "Error during registration. Please try again.")

        else:
            tk.messagebox.showinfo("Error", "Please fill all fields.")

    def create_widgets(self):
        self.create_labels()
        self.create_entries()
        self.create_buttons()

    def create_labels(self):
        # Title and description
        tk.Label(self, text="Facebook", font=("Arial", 43, "bold"), fg="#4267B2", bg="#f0f2f5").place(x=230, y=210)
        tk.Label(self, text="Facebook helps you connect and share", font=("Helvetica", 20), fg="black",
                 bg="#f0f2f5").place(x=230, y=290)
        tk.Label(self, text="with the people in your life.", font=("Helvetica", 20), fg="black", bg="#f0f2f5").place(
            x=230, y=323)

        # Signup panel background
        self.signup_canvas = tk.Canvas(self, width=420, height=450, bg="#fff", highlightthickness=0)
        self.signup_canvas.place(x=819, y=175)

        # Adding a frame to group entry and buttons
        self.entry_frame = tk.Frame(self, bg="#fff")
        self.entry_frame.place(x=819, y=175, width=420, height=450)

        # Rounded corners effect (manually draw arcs)
        radius = 20
        self.signup_canvas.create_arc((0, 0, radius * 2, radius * 2), start=90, extent=90, style="arc",
                                      outline="#dbdbdb")
        self.signup_canvas.create_arc((420 - radius * 2, 0, 420, radius * 2), start=0, extent=90, style="arc",
                                      outline="#dbdbdb")
        self.signup_canvas.create_arc((0, 450 - radius * 2, radius * 2, 450), start=180, extent=90, style="arc",
                                      outline="#dbdbdb")
        self.signup_canvas.create_arc((420 - radius * 2, 450 - radius * 2, 420, 450), start=270, extent=90, style="arc",
                                      outline="#dbdbdb")

    def create_entries(self):
        entry_bg = "#f7f7f7"  # Slightly off-white for entry background
        entry_fg = "#667594"  # Black text color
        entry_font = ("Arial", 14)

        # Username Entry
        self.username_ent = tk.Entry(self.entry_frame, width=30, font=entry_font, bg=entry_bg, fg=entry_fg, bd=0,
                                     highlightthickness=1, relief="flat")
        self.username_ent.insert(0, 'Username')
        self.username_ent.place(x=50, y=50, height=50)
        self.username_ent.configure(highlightbackground="#dbdbdb", highlightcolor="#4267B2")

        # Email Entry
        self.email_entry = tk.Entry(self.entry_frame, width=30, font=entry_font, bg=entry_bg, fg=entry_fg, bd=0,
                                    highlightthickness=1, relief="flat")
        self.email_entry.insert(0, 'Email')
        self.email_entry.place(x=50, y=120, height=50)
        self.email_entry.configure(highlightbackground="#dbdbdb", highlightcolor="#4267B2")

        # Password Entry
        self.password_e = tk.Entry(self.entry_frame, width=30, font=entry_font, bg=entry_bg, fg=entry_fg, show="*",
                                   bd=0, highlightthickness=1, relief="flat")
        self.password_e.insert(0, 'Password')
        self.password_e.place(x=50, y=190, height=50)
        self.password_e.configure(highlightbackground="#dbdbdb", highlightcolor="#4267B2")

        # Admin Checkbox
        self.is_adminvar = tk.IntVar()
        self.is_admin_checkbox = tk.Checkbutton(self.entry_frame, text="Sign up as Admin", variable=self.is_adminvar,
                                                bg="#fff", font=("Arial", 12))
        self.is_admin_checkbox.place(x=50, y=260)

    def create_buttons(self):
        button_font = ("Arial", 14, "bold")
        signup_button_bg = "#42b72a"
        signup_button_fg = "#fff"
        signup_button_active_bg = "#36a420"
        button_font = ("Arial", 14, "bold")
        login_button_bg = "#4267B2"
        login_button_fg = "#fff"
        login_button_active_bg = "#365899"

        create_account_bg = "#42b72a"
        create_account_active_bg = "#36a420"

        # Signup Button
        signup_button = tk.Button(self.entry_frame, text='SIGN UP', font=button_font, width=20, bd=0,
                                  bg=signup_button_bg,
                                  cursor='hand2', activebackground=signup_button_active_bg, fg=signup_button_fg,
                                  command=self.sign_user)
        signup_button.place(x=100, y=320)
        signup_button.bind("<Enter>", lambda e: signup_button.config(bg=signup_button_active_bg))
        signup_button.bind("<Leave>", lambda e: signup_button.config(bg=signup_button_bg))

        login_button = tk.Button(self.entry_frame, text="Back to login", font=button_font, width=20, bd=0, bg=login_button_bg,
                                 cursor='hand2', activebackground=login_button_active_bg, fg=login_button_fg,
                                 command=self.back_to_login)
        login_button.place(x=100, y=370)  # Centered within the frame
        login_button.bind("<Enter>", lambda e: login_button.config(bg=login_button_active_bg))
        login_button.bind("<Leave>", lambda e: login_button.config(bg=login_button_bg))

        # # Back to Login Button
        # back_button = tk.Button(self.entry_frame, text="Back to Login", command=self.back_to_login, border=0,
        #                         bg="white", fg="blue",
        #                         font=("Arial", 12, "underline"))
        # back_button.place(x=150, y=380)


    def back_to_login(self):
        self.destroy()
        self.parent.deiconify()


if __name__ == "__main__":
    # Mocking a parent window for the sake of this example
    root = tk.Tk()
    root.withdraw()
    app = SignupPage(root)
    app.mainloop()
