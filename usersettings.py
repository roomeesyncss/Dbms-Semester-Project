import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from dbcon import DatabaseConnection

class SettingsUI(tk.Toplevel):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.user_id = user_id
        self.title("User Settings")
        self.geometry("400x400")
        self.configure(bg='#f0f2f5')
        self.db = DatabaseConnection()
        self.create_widgets()
        self.initialize_settings()

    def create_widgets(self):
        tk.Label(self, text="Notification Preference", bg='#f0f2f5', font=('Segoe UI', 12)).pack(pady=10)
        self.notification_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self, text="Enable Notifications", variable=self.notification_var, bg='#f0f2f5', font=('Segoe UI', 10)).pack()

        tk.Label(self, text="Privacy Level", bg='#f0f2f5', font=('Segoe UI', 12)).pack(pady=10)
        self.privacy_var = tk.StringVar(value="Public")
        privacy_options = ["Public", "Friends Only", "Private"]
        tk.OptionMenu(self, self.privacy_var, *privacy_options).pack()

        tk.Label(self, text="Theme", bg='#f0f2f5', font=('Segoe UI', 12)).pack(pady=10)
        self.theme_var = tk.StringVar(value="Light")
        theme_options = ["Light", "Dark"]
        tk.OptionMenu(self, self.theme_var, *theme_options).pack()

        tk.Label(self, text="Language", bg='#f0f2f5', font=('Segoe UI', 12)).pack(pady=10)
        self.language_var = tk.StringVar(value="English")
        language_options = ["English", "Spanish", "French", "German"]
        tk.OptionMenu(self, self.language_var, *language_options).pack()

        tk.Button(self, text="Save Settings", command=self.save_settings, bg='#3b5998', fg='white', font=('Segoe UI', 12)).pack(pady=20)

        self.load_settings()

    def create_database_connection(self):
        return self.db.create_connection()

    def initialize_settings(self):
        connection = self.create_database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    IF NOT EXISTS (SELECT 1 FROM Settings WHERE UserID = ?)
                    BEGIN
                        INSERT INTO Settings (UserID, NotificationPreference, PrivacyLevel, Theme, Language)
                        VALUES (?, 1, 'Public', 'Light', 'English')
                    END
                """, (self.user_id, self.user_id))
                connection.commit()
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to initialize settings: {e}")
        finally:
            connection.close()

    def load_settings(self):
        connection = self.create_database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT NotificationPreference, PrivacyLevel, Theme, Language FROM Settings WHERE UserID = ?", (self.user_id,))
                settings = cursor.fetchone()
                if settings:
                    self.notification_var.set(settings[0])
                    self.privacy_var.set(settings[1])
                    self.theme_var.set(settings[2])
                    self.language_var.set(settings[3])
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to load settings: {e}")
        finally:
            connection.close()

    def save_settings(self):
        notification_pref = self.notification_var.get()
        privacy_level = self.privacy_var.get()
        theme = self.theme_var.get()
        language = self.language_var.get()

        connection = self.create_database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    EXEC UpdateUserSettings @UserID=?, @NotificationPreference=?, @PrivacyLevel=?, @Theme=?, @Language=?
                """, (self.user_id, notification_pref, privacy_level, theme, language))
                connection.commit()
                messagebox.showinfo("Success", "Settings updated successfully!")
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to update settings: {e}")
        finally:
            connection.close()
