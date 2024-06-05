import tkinter as tk
from tkinter import messagebox
import pyodbc
from dbcon import DatabaseConnection


class NotificationsPage(tk.Toplevel):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.user_id = user_id
        self.title("Notifications")
        self.geometry("600x500")
        self.configure(bg="#f0f2f5")

        self.db = DatabaseConnection()
        self.connection = self.db.create_connection()

        self.create_widgets()
        self.load_notif()

    def create_widgets(self):
        self.notifications_frame = tk.Frame(self, bg="#f0f2f5")
        self.notifications_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.n_lbox = tk.Listbox(self.notifications_frame, font=('Segoe UI', 12), bg="#ffffff", activestyle='none')
        self.n_lbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.notifications_frame, orient=tk.VERTICAL, command=self.n_lbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.n_lbox.config(yscrollcommand=scrollbar.set)

        # Mark as Read button
        self.read_button = tk.Button(self, text="Mark as Read", font=('Segoe UI', 12), bg="#3b5998", fg="#ffffff",
                                     command=self.mark_as_read)
        self.read_button.pack(pady=10)

    def load_notif(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("EXEC GetUserNotifications @UserID = ?", (self.user_id,))
                notifications = cursor.fetchall()

                for notification in notifications:
                    notification_id, content, created_at = notification
                    display_text = f"{created_at.strftime('%Y-%m-%d %H:%M:%S')}: {content}"
                    self.n_lbox.insert(tk.END, display_text)
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to load notifications: {e}")
        finally:
            self.connection.close()

    def mark_as_read(self):
        pass
        # selected_indices = self.n_lbox.curselection()
        # if not selected_indices:
        #     messagebox.showinfo("No Selection", "Please select a notification to mark as read.")
        #     return
        #
        # try:
        #     with self.connection.cursor() as cursor:
        #         for index in selected_indices:
        #             notification_text = self.n_lbox.get(index)
        #             notification_id = self.extr_notid_id(notification_text)
        #             cursor.execute("EXEC MarkNotificationAsRead @NotificationID = ?", (notification_id,))
        #         self.connection.commit()
        #
        #         self.load_notif()
        #         messagebox.showinfo("Success", "Selected notifications marked as read.")
        # except pyodbc.Error as e:
        #     messagebox.showerror("Database Error", f"Failed to mark notifications as read: {e}")

    def extr_notid_id(self, notification_text):

        start = notification_text.find("(ID: ") + len("(ID: ")
        end = notification_text.find(")", start)
        return int(notification_text[start:end])


