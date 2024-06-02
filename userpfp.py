import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from dbcon import DatabaseConnection

class UserPfP(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.title("User Profile")
        self.geometry("400x500")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")
        self.db = DatabaseConnection()
        self.connection = self.db.create_connection()

        self.user_profile = self.fetch_user_profile(username)
        if self.user_profile:
            self.create_profile_widgets()
        else:
            messagebox.showerror("Error", "Failed to fetch user profile.")

    def fetch_user_profile(self, username):
        try:
            cursor = self.connection.cursor()
            cursor.execute("{CALL UserProfile(?)}", (username,))
            user_profile = cursor.fetchone()
            print("User Profile:", user_profile)  #
            return user_profile
        except Exception as e:
            print("Error fetching user profile:", e)
            return None
        finally:
            cursor.close()

    def create_profile_widgets(self):
        user_id, username, email, full_name, is_admin, registration_date, country, phone = self.user_profile

        self.configure(bg="#f0f0f0")

        header_frame = tk.Frame(self, bg="#3b5998", padx=10, pady=10)
        header_frame.pack(fill="x")

        username_label = tk.Label(header_frame, text=username, fg="white", bg="#3b5998", font=("Arial", 16, "bold"))
        username_label.pack()

        main_frame = tk.Frame(self, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        keys = [
            ("User ID:", user_id),
            ("Email:", email),
            ("Full Name:", full_name if full_name else ""),
            ("Admin:", "Yes" if is_admin else "No"),
            ("Registration Date:", registration_date.strftime('%Y-%m-%d')),
            ("Country:", country if country else ""),
            ("Phone:", phone if phone else ""),
        ]

        for row, (attribute, value) in enumerate(keys):
            label = tk.Label(main_frame, text=attribute, bg="#f0f0f0", fg="#3b5998", font=("Arial", 12, "bold"))
            label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

            entry = ttk.Entry(main_frame, style="Profile.TEntry")
            entry.insert(0, str(value))
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")

            if attribute == "Email:":
                self.email_entry = entry
            elif attribute == "Full Name:":
                self.full_name_entry = entry
            elif attribute == "Country:":
                self.country_entry = entry
            elif attribute == "Phone:":
                self.phone_entry = entry

        # Update Profile Button
        ubut = ttk.Button(main_frame, text="Update Profile", command=self.update_profile)
        ubut.grid(row=len(keys), column=0, columnspan=2, pady=10, padx=10)

        change_picture_button = ttk.Button(main_frame, text="now it should be someyjhing else",
                                           command=self.change_profile_picture)
        change_picture_button.grid(row=len(keys) + 1, column=0, columnspan=2, pady=5, padx=10)

        style = ttk.Style()
        style.configure("Profile.TButton", font=("Arial", 12), padding=8, foreground="white", background="#3b5998")
        style.map("Profile.TButton",
                  background=[("active", "#365899")])

        style.configure("Profile.TEntry",
                        font=("Arial", 12),
                        padding=5,
                        background="white",
                        relief="solid")

    def update_profile(self):
        updated_email = self.email_entry.get().strip()
        updated_full_name = self.full_name_entry.get().strip()
        updated_country = self.country_entry.get().strip()
        updated_phone = self.phone_entry.get().strip()

        connection = self.db.create_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("{CALL UpdateUserProf(?, ?, ?, ?, ?)}",
                           (self.username, updated_email, updated_full_name, updated_country, updated_phone))
            connection.commit()
            messagebox.showinfo("Success", "Profile updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update profile: {e}")
        finally:
            cursor.close()

    def change_profile_picture(self):
        pass
