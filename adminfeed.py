import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import re
class AdminFeed(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.geometry('1200x800')
        self.title('Admin Feed')
        self.username = username
        self.create_widgets()
        self.sidebar_frame.pack_forget()  # Initially hide the sidebar

    def create_database_connection(self):
        server_name = 'localhost\\SQLEXPRESS01'
        database_name = 'Facebook'
        trusted_connection = 'yes'
        connection_string = f'DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};Trusted_Connection={trusted_connection};'
        connection = pyodbc.connect(connection_string)
        return connection

    def create_widgets(self):
        main_frame = tk.Frame(self, bg='#f0f2f5')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Sidebar Frame
        self.sidebar_frame = tk.Frame(main_frame, bg='#3b5998', width=250)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        # Sidebar Buttons
        self.create_sidebar_buttons()

        # Content Frame
        self.content_frame = tk.Frame(main_frame, bg='#f0f2f5')
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Navigation Bar
        navbar_frame = tk.Frame(self.content_frame, bg='#3b5998', padx=20, pady=10)
        navbar_frame.pack(fill=tk.X)

        tk.Label(navbar_frame, text='Admin Dashboard', font=('Segoe UI', 20, 'bold'), fg='white', bg='#3b5998').pack(
            side=tk.LEFT, padx=10)

        # Navigation Buttons
        self.create_navbar_buttons(navbar_frame)

    def create_sidebar_buttons(self):
        button_config = {'font': ('Segoe UI', 14), 'fg': 'white', 'bg': '#3b5998', 'activebackground': '#4e69a2',
                         'activeforeground': 'white', 'relief': tk.FLAT}

        sidebar_buttons = [
            ('Manage Users', self.load_users),
            ('Manage Posts', self.load_posts),
            ('Handle Reports', self.load_reports)
        ]

        for button_text, command in sidebar_buttons:
            button = tk.Button(self.sidebar_frame, text=button_text, **button_config, command=command)
            button.pack(pady=15, padx=20, fill=tk.X)

    def create_navbar_buttons(self, parent_frame):
        nav_buttons_frame = tk.Frame(parent_frame, bg='#3b5998')
        nav_buttons_frame.pack(side=tk.LEFT, padx=10)

        nav_buttons = [
            ('Home', self.go_home),
            ('Profile', self.go_profile),
            ('Friends', self.go_friends),
            ('Manage user',  self.load_users),
            ('Manage Post', self.load_posts),
            ('Settings', self.go_settings),
            ('Reports', self.load_reports),
            ('Sidebar', self.toggle_sidebar)
        ]

        button_config = {'font': ('Segoe UI', 12), 'fg': 'white', 'bg': '#3b5998', 'activebackground': '#4e69a2',
                         'activeforeground': 'white', 'relief': tk.FLAT}

        for button_text, command in nav_buttons:
            nav_button = tk.Button(nav_buttons_frame, text=button_text, **button_config, command=command)
            nav_button.pack(side=tk.LEFT, padx=10)

    def toggle_sidebar(self):
        if self.sidebar_frame.winfo_viewable():
            self.sidebar_frame.pack_forget()
        else:
            self.sidebar_frame.pack(side=tk.LEFT, fill=tk.BOTH)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def load_users(self):
        self.clear_content_frame()
        users_frame = tk.Frame(self.content_frame, bg='#f0f2f5')
        users_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(users_frame, text="Manage Users", font=('Segoe UI', 18, 'bold'), bg='#f0f2f5').pack(pady=10)

        connection = self.create_database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("EXEC GetAllUsers")
                users = cursor.fetchall()
        finally:
            connection.close()

        columns = ('UserID', 'Username', 'Email', 'IsAdmin')
        tree = ttk.Treeview(users_frame, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER)

        for user in users:
            tree.insert('', tk.END, values=user)
            print(f"Inserted values: {user}")

        button_frame = tk.Frame(users_frame, bg='#f0f2f5')
        button_frame.pack(pady=10)

        delete_button = tk.Button(button_frame, text="Delete User", font=('Segoe UI', 12), command=lambda: self.delete_user(tree))
        delete_button.pack(side=tk.LEFT, padx=5)

    def delete_user(self, tree):
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item)['values']
            user_id_str = values[0]  # Extract the string containing the UserID
            user_id = int(re.sub(r'[^\d]', '', user_id_str))  # Remove non-digit characters and convert to integer
            connection = self.create_database_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("EXEC DeleteUser @UserID=?", (user_id,))
                    connection.commit()
                    tree.delete(selected_item)
                    messagebox.showinfo("Success", "User deleted successfully.")
            finally:
                connection.close()


    def load_posts(self):
        self.clear_content_frame()
        posts_frame = tk.Frame(self.content_frame, bg='#f0f2f5')
        posts_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(posts_frame, text="Manage Posts", font=('Segoe UI', 18, 'bold'), bg='#f0f2f5').pack(pady=10)

        connection = self.create_database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT PostID, UserID, Content, Timestamp FROM Posts")
                posts = cursor.fetchall()
        finally:
            connection.close()

        columns = ('PostID', 'UserID', 'Content', 'Timestamp')
        tree = ttk.Treeview(posts_frame, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER)

        for post in posts:
            tree.insert('', tk.END, values=post)

        button_frame = tk.Frame(posts_frame, bg='#f0f2f5')
        button_frame.pack(pady=10)

        delete_button = tk.Button(button_frame, text="Delete Post", font=('Segoe UI', 12),
                                  command=lambda: self.delete_post(tree))
        delete_button.pack(side=tk.LEFT, padx=5)

    def load_reports(self):
        self.clear_content_frame()
        reports_frame = tk.Frame(self.content_frame, bg='#f0f2f5')
        reports_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(reports_frame, text="Handle Reports", font=('Segoe UI', 18, 'bold'), bg='#f0f2f5').pack(pady=10)

        connection = self.create_database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT ReportID, PostID, UserID, Reason FROM Reports")
                reports = cursor.fetchall()
        finally:
            connection.close()

        columns = ('ReportID', 'PostID', 'UserID', 'Reason')
        tree = ttk.Treeview(reports_frame, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER)

        for report in reports:
            tree.insert('', tk.END, values=report)

        button_frame = tk.Frame(reports_frame, bg='#f0f2f5')
        button_frame.pack(pady=10)

        handle_button = tk.Button(button_frame, text="Handle Report", font=('Segoe UI', 12),
                                  command=lambda: self.handle_report(tree))
        handle_button.pack(side=tk.LEFT, padx=5)


    def delete_post(self, tree):
        selected_item = tree.selection()
        if selected_item:
            post_id = int(tree.item(selected_item)['values'][0])  # Ensure post_id is an integer
            connection = self.create_database_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM Posts WHERE PostID = ?", (post_id,))
                    connection.commit()
                    tree.delete(selected_item)
                    messagebox.showinfo("Success", "Post deleted successfully.")
            finally:
                connection.close()

    def handle_report(self, tree):
        selected_item = tree.selection()
        if selected_item:
            report_id = int(tree.item(selected_item)['values'][0])  # Ensure report_id is an integer
            post_id = int(tree.item(selected_item)['values'][1])  # Ensure post_id is an integer
            connection = self.create_database_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM Posts WHERE PostID = ?", (post_id,))
                    cursor.execute("DELETE FROM Reports WHERE ReportID = ?", (report_id,))
                    connection.commit()
                    tree.delete(selected_item)
                    messagebox.showinfo("Success", "Report handled and post deleted successfully.")
            finally:
                connection.close()

    def go_home(self):
        pass

    def go_profile(self):
        pass

    def go_friends(self):
        pass

    def go_notifications(self):
        pass

    def go_messages(self):
        pass

    def go_settings(self):
        pass

    def add_friend(self):
        pass

    def logout(self):
        self.destroy()
        self.parent.deiconify()


