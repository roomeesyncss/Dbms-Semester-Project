import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from dbcon import DatabaseConnection
from userfeed import UserMFeed
from signup import SignupPage
from adminfeed import AdminFeed


class FacebookMainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1280x720')
        self.title('Facebook Login')
        self.configure(bg="#f0f2f5")  # Light gray background
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
            tk.messagebox.showinfo("Success", f"Login successful. Welcome {username}.")

            self.withdraw()
            is_admin = user[1]
            if is_admin:
                admin_feed = AdminFeed(self, username)
                admin_feed.mainloop()
            else:
                user_feed = UserMFeed(self, username)
                user_feed.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

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

        # Login panel background
        self.login_canvas = tk.Canvas(self, width=420, height=378, bg="#fff", highlightthickness=0)
        self.login_canvas.place(x=819, y=175)

        # Adding a frame to group entry and buttons
        self.entry_frame = tk.Frame(self, bg="#fff")
        self.entry_frame.place(x=819, y=175, width=420, height=378)

        # Rounded corners effect (manually draw arcs)
        radius = 20
        self.login_canvas.create_arc((0, 0, radius * 2, radius * 2), start=90, extent=90, style="arc",
                                     outline="#dbdbdb")
        self.login_canvas.create_arc((420 - radius * 2, 0, 420, radius * 2), start=0, extent=90, style="arc",
                                     outline="#dbdbdb")
        self.login_canvas.create_arc((0, 378 - radius * 2, radius * 2, 378), start=180, extent=90, style="arc",
                                     outline="#dbdbdb")
        self.login_canvas.create_arc((420 - radius * 2, 378 - radius * 2, 420, 378), start=270, extent=90, style="arc",
                                     outline="#dbdbdb")

    def create_entries(self):
        entry_bg = "#f7f7f7"  # Slightly off-white for entry background
        entry_fg = "#667594"  # Black text color
        entry_font = ("Arial", 14)

        # Username Entry
        self.username_entry = tk.Entry(self.entry_frame, width=30, font=entry_font, bg=entry_bg, fg=entry_fg, bd=0,
                                       highlightthickness=1, relief="flat")
        self.username_entry.insert(0, 'Username')
        self.username_entry.place(x=50, y=50, height=50)  # Adjusted positioning within the frame
        self.username_entry.configure(highlightbackground="#dbdbdb", highlightcolor="#4267B2")

        # Password Entry
        self.password_entry = tk.Entry(self.entry_frame, width=30, font=entry_font, bg=entry_bg, fg=entry_fg, show='*',
                                       bd=0, highlightthickness=1, relief="flat")
        self.password_entry.insert(0, 'Password')
        self.password_entry.place(x=50, y=120, height=50)  # Adjusted positioning within the frame
        self.password_entry.configure(highlightbackground="#dbdbdb", highlightcolor="#4267B2")

    def create_buttons(self):
        # Button styling
        button_font = ("Arial", 14, "bold")
        login_button_bg = "#4267B2"
        login_button_fg = "#fff"
        login_button_active_bg = "#365899"

        create_account_bg = "#42b72a"
        create_account_active_bg = "#36a420"

        # Login Button
        login_button = tk.Button(self.entry_frame, text='LOGIN', font=button_font, width=18, bd=0, bg=login_button_bg,
                                 cursor='hand2', activebackground=login_button_active_bg, fg=login_button_fg,
                                 command=self.log_user)
        login_button.place(x=107, y=220)  # Centered within the frame
        login_button.bind("<Enter>", lambda e: login_button.config(bg=login_button_active_bg))
        login_button.bind("<Leave>", lambda e: login_button.config(bg=login_button_bg))


        createAcc_button = tk.Button(self.entry_frame, text='Create Account', font=button_font, width=18, bd=0,
                                     bg=create_account_bg, cursor='hand2', activebackground=create_account_active_bg,
                                     fg='white',
                                     command=self.open_signup_page)
        createAcc_button.place(x=107, y=270)  # Centered within the frame
        createAcc_button.bind("<Enter>", lambda e: createAcc_button.config(bg=create_account_active_bg))
        createAcc_button.bind("<Leave>", lambda e: createAcc_button.config(bg=create_account_bg))

    def forgot_password(self):
        tk.messagebox.showinfo("Forgot Password", "Password reset feature is not yet implemented.")

    def open_signup_page(self):
        self.withdraw()
        signup_page = SignupPage(self)
        signup_page.mainloop()
        self.deiconify()


if __name__ == "__main__":
    app = FacebookMainApp()
    app.mainloop()
