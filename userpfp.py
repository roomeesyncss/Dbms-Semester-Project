# import tkinter as tk
# from tkinter import ttk, messagebox
# import pyodbc
# from dbcon import DatabaseConnection
#
# class UserPfP(tk.Toplevel):
#     def __init__(self, parent, user_id):
#         super().__init__(parent)
#         self.parent = parent
#         self.user_id = user_id
#         self.title("User Profile")
#         self.geometry("800x600")  # Increased width to accommodate posts
#
#         self.configure(bg="#f0f0f0")
#         self.db = DatabaseConnection()
#         self.connection = self.db.create_connection()
#
#         self.user_profile = self.fetch_user_profile(user_id)
#         if self.user_profile:
#             self.create_profile_widgets()
#             self.load_posts()  # Automatically load posts
#         else:
#             messagebox.showerror("Error", "Failed to fetch user profile.")
#
#     def fetch_user_profile(self, user_id):
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute("{CALL UserProfileById(?)}", (user_id,))
#             user_profile = cursor.fetchone()
#             print("User Profile:", user_profile)
#             return user_profile
#         except Exception as e:
#             print("Error fetching user profile:", e)
#             return None
#         finally:
#             cursor.close()
#
#     def create_profile_widgets(self):
#         user_id, username, email, full_name, is_admin, registration_date, country, phone, password = self.user_profile
#
#         self.configure(bg="#f0f0f0")
#
#         header_frame = tk.Frame(self, bg="#3b5998", padx=10, pady=10)
#         header_frame.pack(fill="x")
#
#         username_label = tk.Label(header_frame, text=username, fg="white", bg="#3b5998", font=("Arial", 16, "bold"))
#         username_label.pack()
#
#         main_frame = tk.Frame(self, bg="#f0f0f0", padx=20, pady=20)
#         main_frame.pack(fill="both", expand=True)
#
#         keys = [
#             ("User ID:", user_id),
#             ("Username:", username),
#             ("Email:", email),
#             ("Full Name:", full_name if full_name else ""),
#             ("Admin:", "Yes" if is_admin else "No"),
#             ("Registration Date:", registration_date.strftime('%Y-%m-%d')),
#             ("Country:", country if country else ""),
#             ("Phone:", phone if phone else ""),
#         ]
#
#         for row, (attribute, value) in enumerate(keys):
#             label = tk.Label(main_frame, text=attribute, bg="#f0f0f0", fg="#3b5998", font=("Arial", 12, "bold"))
#             label.grid(row=row, column=0, sticky="w", padx=10, pady=5)
#
#             entry = ttk.Entry(main_frame, style="Profile.TEntry")
#             entry.insert(0, str(value))
#             entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
#
#             if attribute == "Username:":
#                 self.username_entry = entry
#             elif attribute == "Email:":
#                 self.email_entry = entry
#             elif attribute == "Full Name:":
#                 self.full_name_entry = entry
#             elif attribute == "Country:":
#                 self.country_entry = entry
#             elif attribute == "Phone:":
#                 self.phone_entry = entry
#
#         # Password Field
#         password_label = tk.Label(main_frame, text="Password:", bg="#f0f0f0", fg="#3b5998", font=("Arial", 12, "bold"))
#         password_label.grid(row=len(keys), column=0, sticky="w", padx=10, pady=5)
#
#         self.password_entry = ttk.Entry(main_frame, style="Profile.TEntry", show="*")
#         self.password_entry.grid(row=len(keys), column=1, padx=10, pady=5, sticky="ew")
#
#         # Update Profile Button
#         ubut = ttk.Button(main_frame, text="Update Profile", command=self.update_profile)
#         ubut.grid(row=len(keys) + 1, column=0, columnspan=2, pady=10, padx=10)
#
#         # Create a frame for posts with a scrollbar
#         posts_container = tk.Frame(self, bg="#f0f0f0")
#         posts_container.pack(fill="both", expand=True)
#
#         self.canvas = tk.Canvas(posts_container, bg="#f0f0f0")
#         self.canvas.pack(side="left", fill="both", expand=True)
#
#         self.scrollbar = ttk.Scrollbar(posts_container, orient="vertical", command=self.canvas.yview)
#         self.scrollbar.pack(side="right", fill="y")
#
#         self.canvas.configure(yscrollcommand=self.scrollbar.set)
#
#         self.post_frame = tk.Frame(self.canvas, bg="#f0f0f0")
#         self.canvas.create_window((0, 0), window=self.post_frame, anchor="nw")
#
#         self.post_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
#
#         style = ttk.Style()
#         style.configure("Profile.TButton", font=("Arial", 12), padding=8, foreground="white", background="#3b5998")
#         style.map("Profile.TButton", background=[("active", "#365899")])
#
#         style.configure("Profile.TEntry", font=("Arial", 12), padding=5, background="white", relief="solid")
#
#     def update_profile(self):
#         updated_username = self.username_entry.get().strip()
#         updated_email = self.email_entry.get().strip()
#         updated_full_name = self.full_name_entry.get().strip()
#         updated_country = self.country_entry.get().strip()
#         updated_phone = self.phone_entry.get().strip()
#         updated_password = self.password_entry.get().strip()
#
#         # Validate phone number input
#         try:
#             updated_phone_numeric = int(updated_phone)
#         except ValueError:
#             messagebox.showerror("Error", "Phone number must be numeric.")
#             return
#
#         connection = self.db.create_connection()
#         try:
#             cursor = connection.cursor()
#             cursor.execute("{CALL UpdateUser(?, ?, ?, ?, ?, ?, ?)}",
#                            (self.user_id, updated_username, updated_full_name, updated_email, updated_password, updated_country, updated_phone_numeric))
#             connection.commit()
#             messagebox.showinfo("Success", "Profile updated successfully.")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to update profile: {e}")
#         finally:
#             cursor.close()
#
#     def load_posts(self):
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute("EXEC GetUserPosts @UserID = ?", (self.user_id,))
#             posts = cursor.fetchall()
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to load posts: {e}")
#             return
#         finally:
#             cursor.close()
#
#         for widget in self.post_frame.winfo_children():
#             widget.destroy()
#
#         for post in posts:
#             username, content, timestamp, likes, comments, shares, post_id = post
#             self.create_post_widget(username, content, timestamp, likes, comments, post_id, shares)
#
#     def create_post_widget(self, username, content, timestamp, likes, comments, post_id, shares):
#         post_frame = tk.Frame(self.post_frame, bg='#ffffff', padx=20, pady=15, relief=tk.RAISED, borderwidth=1)
#         post_frame.pack(fill=tk.X, padx=10, pady=10)
#
#         user_label = tk.Label(post_frame, text=username, font=('Leelawadee', 14, 'bold'), bg='#ffffff', fg='#3a4be8')
#         user_label.pack(anchor='w')
#
#         content_label = tk.Label(post_frame, text=content, wraplength=750, justify=tk.LEFT, bg='#ffffff', font=('Segoe UI', 12))
#         content_label.pack(anchor='w')
#
#         timestamp_label = tk.Label(post_frame, text=timestamp.strftime('%Y-%m-%d %H:%M:%S'), bg='#ffffff', font=('Segoe UI', 6))
#         timestamp_label.pack(anchor='e')
#
#         action_frame = tk.Frame(post_frame, bg='#ffffff')
#         action_frame.pack(fill=tk.X, pady=10)
#
#         edit_button = ttk.Button(action_frame, text="Edit", command=lambda: self.edit_post(post_id))
#         edit_button.pack(side=tk.LEFT, padx=5)
#
#         delete_button = ttk.Button(action_frame, text="Delete", command=lambda: self.delete_post(post_id))
#         delete_button.pack(side=tk.LEFT, padx=5)
#
#     def delete_post(self, post_id):
#         confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this post?")
#         if confirmation:
#             connection = self.db.create_connection()
#             try:
#                 cursor = connection.cursor()
#                 cursor.execute("{CALL DeleteUserPost(?)}", (post_id,))
#                 connection.commit()
#                 messagebox.showinfo("Success", "Post deleted successfully.")
#                 # Reload posts after delete
#                 self.load_posts()
#             except Exception as e:
#                 messagebox.showerror("Error", f"Failed to delete post: {e}")
#             finally:
#                 cursor.close()
#                 connection.close()
#
#     def get_new_content_from_user(self):
#         new_content = None
#
#         def save_new_content():
#             nonlocal new_content
#             new_content = new_content_entry.get()
#             new_content_window.destroy()
#
#         new_content_window = tk.Toplevel(self)
#         new_content_window.title("Edit Post")
#         new_content_window.geometry("400x200")
#
#         new_content_label = tk.Label(new_content_window, text="Enter new content:")
#         new_content_label.pack()
#
#         new_content_entry = tk.Entry(new_content_window, width=50)
#         new_content_entry.pack()
#
#         save_button = ttk.Button(new_content_window, text="Save", command=save_new_content)
#         save_button.pack()
#
#         new_content_window.focus_force()
#         new_content_window.grab_set()
#         new_content_window.wait_window()
#
#         return new_content
#
#     def edit_post(self, post_id):
#         new_content = self.get_new_content_from_user()  # Implement this function to get the new content from the user
#
#         if not new_content:
#             # User canceled the edit
#             return
#
#         confirmation = messagebox.askyesno("Confirm Edit", "Are you sure you want to edit this post?")
#         if confirmation:
#             connection = self.db.create_connection()
#             try:
#                 cursor = connection.cursor()
#                 cursor.execute("{CALL EditUserPost(?, ?)}", (post_id, new_content))
#                 connection.commit()
#                 messagebox.showinfo("Success", "Post edited successfully.")
#                 # Reload posts after edit
#                 self.load_posts()
#             except Exception as e:
#                 messagebox.showerror("Error", f"Failed to edit post: {e}")
#             finally:
#                 cursor.close()
#                 connection.close()
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyodbc
from dbcon import DatabaseConnection

class UserPfP(tk.Toplevel):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.parent = parent
        self.user_id = user_id
        self.title("User Profile")
        self.geometry("850x650")  # Increased width to accommodate posts and provide a cleaner layout

        self.configure(bg="#e9ebee")
        self.db = DatabaseConnection()
        self.connection = self.db.create_connection()

        self.user_profile = self.fetch_user_profile(user_id)
        if self.user_profile:
            self.create_profile_widgets()
            self.load_posts()  # Automatically load posts
        else:
            messagebox.showerror("Error", "Failed to fetch user profile.")

    def fetch_user_profile(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("{CALL UserProfileById(?)}", (user_id,))
            user_profile = cursor.fetchone()
            print("User Profile:", user_profile)
            return user_profile
        except Exception as e:
            print("Error fetching user profile:", e)
            return None
        finally:
            cursor.close()

    def create_profile_widgets(self):
        user_id, username, email, full_name, is_admin, registration_date, country, phone, password = self.user_profile

        # Header Frame with Facebook Blue
        header_frame = tk.Frame(self, bg="#3b5998", padx=10, pady=10)
        header_frame.pack(fill="x")

        username_label = tk.Label(header_frame, text=username, fg="white", bg="#3b5998", font=("Helvetica", 18, "bold"))
        username_label.pack(side="left")

        # Add profile picture placeholder
        # profile_pic = Image.open("default_profile.png")  # Replace with actual profile picture path
        # profile_pic = profile_pic.resize((50, 50), Image.ANTIALIAS)
        # profile_pic = ImageTk.PhotoImage(profile_pic)
        # profile_pic_label = tk.Label(header_frame, image=profile_pic, bg="#3b5998")
        # profile_pic_label.image = profile_pic  # Keep a reference to avoid garbage collection
        # profile_pic_label.pack(side="right")

        # Main frame for profile details
        main_frame = tk.Frame(self, bg="#ffffff", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        details_frame = tk.Frame(main_frame, bg="#ffffff")
        details_frame.pack(side="left", fill="y", padx=20)

        keys = [
            ("Username:", username),
            ("Email:", email),
            ("Full Name:", full_name if full_name else ""),
            ("Admin:", "Yes" if is_admin else "No"),
            ("Registration Date:", registration_date.strftime('%Y-%m-%d')),
            ("Country:", country if country else ""),
            ("Phone:", phone if phone else ""),
        ]

        for row, (attribute, value) in enumerate(keys):
            label = tk.Label(details_frame, text=attribute, bg="#ffffff", fg="#3b5998", font=("Arial", 12, "bold"))
            label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

            entry = ttk.Entry(details_frame, style="Profile.TEntry")
            entry.insert(0, str(value))
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")

            if attribute == "Username:":
                self.username_entry = entry
            elif attribute == "Email:":
                self.email_entry = entry
            elif attribute == "Full Name:":
                self.full_name_entry = entry
            elif attribute == "Country:":
                self.country_entry = entry
            elif attribute == "Phone:":
                self.phone_entry = entry

        # Password Field
        password_label = tk.Label(details_frame, text="Password:", bg="#ffffff", fg="#3b5998", font=("Arial", 12, "bold"))
        password_label.grid(row=len(keys), column=0, sticky="w", padx=10, pady=5)

        self.password_entry = ttk.Entry(details_frame, style="Profile.TEntry", show="*")
        self.password_entry.grid(row=len(keys), column=1, padx=10, pady=5, sticky="ew")

        # Update Profile Button
        update_button = ttk.Button(details_frame, text="Update Profile", command=self.update_profile, style="Profile.TButton")
        update_button.grid(row=len(keys) + 1, column=0, columnspan=2, pady=10, padx=10)

        # Posts Section
        posts_frame = tk.Frame(main_frame, bg="#e9ebee", padx=20, pady=20)
        posts_frame.pack(side="right", fill="both", expand=True)

        self.canvas = tk.Canvas(posts_frame, bg="#e9ebee")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(posts_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.post_frame = tk.Frame(self.canvas, bg="#e9ebee")
        self.canvas.create_window((0, 0), window=self.post_frame, anchor="nw")

        self.post_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Style Configuration
        style = ttk.Style()
        style.configure("Profile.TButton", font=("Helvetica", 12), padding=8, foreground="white", background="#4267b2")
        style.map("Profile.TButton", background=[("active", "#365899")])

        style.configure("Profile.TEntry", font=("Arial", 12), padding=5, background="white", relief="solid")

    def update_profile(self):
        updated_username = self.username_entry.get().strip()
        updated_email = self.email_entry.get().strip()
        updated_full_name = self.full_name_entry.get().strip()
        updated_country = self.country_entry.get().strip()
        updated_phone = self.phone_entry.get().strip()
        updated_password = self.password_entry.get().strip()

        # Validate phone number input
        try:
            updated_phone_numeric = int(updated_phone)
        except ValueError:
            messagebox.showerror("Error", "Phone number must be numeric.")
            return

        connection = self.db.create_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("{CALL UpdateUser(?, ?, ?, ?, ?, ?, ?)}",
                           (self.user_id, updated_username, updated_full_name, updated_email, updated_password, updated_country, updated_phone_numeric))
            connection.commit()
            messagebox.showinfo("Success", "Profile updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update profile: {e}")
        finally:
            cursor.close()

    def load_posts(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("EXEC GetUserOnlyPosts @UserID = ?", (self.user_id,))
            posts = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load posts: {e}")
            return
        finally:
            cursor.close()

        # Clear the post frame
        for widget in self.post_frame.winfo_children():
            widget.destroy()

        # Display the user's posts
        for post in posts:
            username, content, timestamp, likes, comments, shares, post_id = post
            self.create_post_widget(username, content, timestamp, likes, comments, post_id, shares)

    def create_post_widget(self, username, content, timestamp, likes, comments, post_id, shares):
        post_frame = tk.Frame(self.post_frame, bg='#ffffff', padx=20, pady=15, relief=tk.RAISED, borderwidth=1)
        post_frame.pack(fill=tk.X, padx=10, pady=10)

        user_label = tk.Label(post_frame, text=username, font=('Helvetica', 14, 'bold'), bg='#ffffff', fg='#3b5998')
        user_label.pack(anchor='w')

        content_label = tk.Label(post_frame, text=content, wraplength=750, justify=tk.LEFT, bg='#ffffff', font=('Arial', 12))
        content_label.pack(anchor='w')

        timestamp_label = tk.Label(post_frame, text=timestamp.strftime('%Y-%m-%d %H:%M:%S'), bg='#ffffff', font=('Arial', 8))
        timestamp_label.pack(anchor='e')

        # Action buttons (Edit/Delete)
        action_frame = tk.Frame(post_frame, bg='#ffffff')
        action_frame.pack(fill=tk.X, pady=10)

        edit_button = ttk.Button(action_frame, text="Edit", command=lambda: self.edit_post(post_id), style="Profile.TButton")
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = ttk.Button(action_frame, text="Delete", command=lambda: self.delete_post(post_id), style="Profile.TButton")
        delete_button.pack(side=tk.LEFT, padx=5)

    def delete_post(self, post_id):
        confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this post?")
        if confirmation:
            connection = self.db.create_connection()
            try:
                cursor = connection.cursor()
                cursor.execute("{CALL DeleteUserPost(?)}", (post_id,))
                connection.commit()
                messagebox.showinfo("Success", "Post deleted successfully.")
                # Reload posts after delete
                self.load_posts()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete post: {e}")
            finally:
                cursor.close()
                connection.close()

    def get_new_content_from_user(self):
        new_content = None

        def save_new_content():
            nonlocal new_content
            new_content = new_content_entry.get()
            new_content_window.destroy()

        new_content_window = tk.Toplevel(self)
        new_content_window.title("Edit Post")
        new_content_window.geometry("400x200")

        new_content_label = tk.Label(new_content_window, text="Enter new content:")
        new_content_label.pack()

        new_content_entry = tk.Entry(new_content_window, width=50)
        new_content_entry.pack()

        save_button = ttk.Button(new_content_window, text="Save", command=save_new_content, style="Profile.TButton")
        save_button.pack()

        new_content_window.focus_force()
        new_content_window.grab_set()
        new_content_window.wait_window()

        return new_content

    def edit_post(self, post_id):
        new_content = self.get_new_content_from_user()  # Implement this function to get the new content from the user

        if not new_content:
            # User canceled the edit
            return

        confirmation = messagebox.askyesno("Confirm Edit", "Are you sure you want to edit this post?")
        if confirmation:
            connection = self.db.create_connection()
            try:
                cursor = connection.cursor()
                cursor.execute("{CALL EditUserPost(?, ?)}", (post_id, new_content))
                connection.commit()
                messagebox.showinfo("Success", "Post edited successfully.")
                self.load_posts()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to edit post: {e}")
            finally:
                cursor.close()
                connection.close()
