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
        self.sidebar_frame.pack_forget()

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
            ('Manage Users', self.load_users),
            ('Manage Posts', self.load_posts),
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
                cursor.execute("EXEC GetUserPosts @UserID=?", (1,))  # Replace with actual Admin UserID if needed
                posts = cursor.fetchall()
        finally:
            connection.close()

        columns = ('Username', 'Content', 'CreatedAt', 'PostID')
        tree = ttk.Treeview(posts_frame, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER)

        for post in posts:
            # Display Username, Content, and CreatedAt in the tree view
            tree.insert('', tk.END, values=(post[0], post[1], post[2], post[6]))

        button_frame = tk.Frame(posts_frame, bg='#f0f2f5')
        button_frame.pack(pady=10)

        delete_button = tk.Button(button_frame, text="Delete Post", font=('Segoe UI', 12), command=lambda: self.delete_post(tree))
        delete_button.pack(side=tk.LEFT, padx=5)

    def delete_post(self, tree):
        selected_item = tree.selection()
        if selected_item:
            post_id_str = tree.item(selected_item)['values'][3]  # Extract PostID from the correct column
            post_id = int(re.sub(r'[^\d]', '', str(post_id_str)))  # Remove non-digit characters and convert to integer
            connection = self.create_database_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("EXEC DeleteUserPost @PostID=?", (post_id,))
                    connection.commit()
                    tree.delete(selected_item)
                    messagebox.showinfo("Success", "Post deleted successfully.")
            finally:
                connection.close()


    def load_reports(self):
        self.clear_content_frame()
        reports_frame = tk.Frame(self.content_frame, bg='#f0f2f5')
        reports_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(reports_frame, text="Handle Reports", font=('Segoe UI', 18, 'bold'), bg='#f0f2f5').pack(pady=10)

        connection = self.create_database_connection()
        try:
            with connection.cursor() as cursor:
                # Use the view to get the reports data
                cursor.execute(
                    "SELECT ReportID, ReportedByUsername, ReportedPostID, ReportedPostContent, ReportReason, ReportDescription, ReportDate FROM AdminViewReports")
                reports = cursor.fetchall()
        finally:
            connection.close()

        # Define columns for the Treeview widget
        columns = (
        'ReportID', 'ReportedByUsername', 'ReportedPostID', 'ReportedPostContent', 'ReportReason', 'ReportDescription',
        'ReportDate')
        tree = ttk.Treeview(reports_frame, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=True)

        # Set up the column headers
        tree.heading('ReportID', text='Report ID')
        tree.heading('ReportedByUsername', text='Reported By')
        tree.heading('ReportedPostID', text='Post ID')
        tree.heading('ReportedPostContent', text='Post Content')
        tree.heading('ReportReason', text='Reason')
        tree.heading('ReportDescription', text='Description')
        tree.heading('ReportDate', text='Date')

        # Adjust the width and alignment for better readability
        tree.column('ReportID', anchor=tk.CENTER, width=80)
        tree.column('ReportedByUsername', anchor=tk.CENTER, width=150)
        tree.column('ReportedPostID', anchor=tk.CENTER, width=80)
        tree.column('ReportedPostContent', anchor=tk.W, width=300)
        tree.column('ReportReason', anchor=tk.CENTER, width=150)
        tree.column('ReportDescription', anchor=tk.W, width=300)
        tree.column('ReportDate', anchor=tk.CENTER, width=150)

        # Insert data into the Treeview
        for report in reports:
            tree.insert('', tk.END, values=report)

        # Add a button frame for handling reports
        button_frame = tk.Frame(reports_frame, bg='#f0f2f5')
        button_frame.pack(pady=10)

        # Button to handle the selected report
        handle_button = tk.Button(button_frame, text="Handle Report", font=('Segoe UI', 12),
                                  command=lambda: self.handle_report(tree))
        handle_button.pack(side=tk.LEFT, padx=5)

    def handle_report(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("No selection", "Please select a report to handle.")
            return

        report_values = tree.item(selected_item)['values']
        print(f"Debug: report_values = {report_values}")  # Debugging: Print report_values to check the format

        try:
            # Clean and parse ReportID
            raw_report_id = report_values[0].strip("(),'")
            report_id = int(raw_report_id)

            # Clean and parse ReportedPostID
            raw_reported_post_id = report_values[2].strip("(),'")
            reported_post_id = int(raw_reported_post_id)

            # Clean ReportReason
            report_reason = report_values[4].strip("(),'")

            # Clean ReportDescription
            # Assuming description is split into parts and needs to be recombined
            report_description_parts = report_values[5:len(report_values) - 4]
            report_description = " ".join(part.strip("(),'") for part in report_description_parts)

            # Handle date parts (you can adapt this based on your actual date format)
            raw_date_parts = report_values[-4:]
            report_date = " ".join(raw_date_parts).replace('datetime.datetime(', '').replace(')', '').replace(',', '')

        except ValueError as ve:
            messagebox.showerror("Data Error", f"Invalid data format: {ve}")
            return

        handle_window = tk.Toplevel(self)
        handle_window.title("Handle Report")
        handle_window.geometry("400x400")

        tk.Label(handle_window, text="Report Details", font=('Segoe UI', 14, 'bold')).pack(pady=10)

        tk.Label(handle_window, text=f"Report ID: {report_id}", font=('Segoe UI', 12)).pack(anchor='w', padx=10, pady=2)
        tk.Label(handle_window, text=f"Reported Post ID: {reported_post_id}", font=('Segoe UI', 12)).pack(anchor='w',
                                                                                                          padx=10,
                                                                                                          pady=2)
        tk.Label(handle_window, text=f"Report Reason: {report_reason}", font=('Segoe UI', 12)).pack(anchor='w', padx=10,
                                                                                                    pady=2)
        tk.Label(handle_window, text=f"Report Description: {report_description}", font=('Segoe UI', 12),
                 wraplength=350).pack(anchor='w', padx=10, pady=2)
        tk.Label(handle_window, text=f"Report Date: {report_date}", font=('Segoe UI', 12)).pack(anchor='w', padx=10,
                                                                                                pady=2)

        button_frame = tk.Frame(handle_window)
        button_frame.pack(pady=20)

        dismiss_button = tk.Button(button_frame, text="Dismiss Report", font=('Segoe UI', 12),
                                   command=lambda: self.dismiss_report(report_id, handle_window))
        dismiss_button.pack(side=tk.LEFT, padx=10)

        delete_post_button = tk.Button(button_frame, text="Delete Post", font=('Segoe UI', 12),
                                       command=lambda: self.delete_postr(report_id, reported_post_id, handle_window))
        delete_post_button.pack(side=tk.LEFT, padx=10)

    def dismiss_report(self, report_id, handle_window):
        connection = self.create_database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Report WHERE ReportID = ?", (report_id,))
                connection.commit()
                messagebox.showinfo("Report Handled", f"Report ID {report_id} has been dismissed.")
                handle_window.destroy()
                self.load_reports()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to dismiss report: {e}")
        finally:
            connection.close()

    def delete_postr(self, report_id, reported_post_id, handle_window):
        connection = self.create_database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Report WHERE ReportID = ?", (report_id,))
                # Then delete the post itself
                cursor.execute("DELETE FROM Post WHERE PostID = ?", (reported_post_id,))

                connection.commit()
                messagebox.showinfo("Post Deleted",
                                    f"The reported post with Post ID {reported_post_id} has been deleted and report ID {report_id} has been resolved.")
                handle_window.destroy()
                self.load_reports()
        except Exception as e:
            print(f"Error occurred: {e}")
            messagebox.showerror("Error", f"Failed to delete post and resolve report: {e}")
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

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = AdminFeed(root, 'admin_username')
    app.mainloop()
