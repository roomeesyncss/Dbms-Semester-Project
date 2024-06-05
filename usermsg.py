import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from dbcon import DatabaseConnection
import pyodbc

class UserMessages(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.title("Messages")
        self.geometry("900x700")

        self.configure(bg="#f0f2f5")

        self.db = DatabaseConnection()
        self.connection = self.db.create_connection()

        self.user_id = self.get_user_id(self.username)
        if not self.user_id:
            messagebox.showerror("Error", "Failed to fetch user ID.")
            self.destroy()
            return

        self.create_message_widgets()
        self.load_chats()

    def get_user_id(self, username):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("{CALL GetUserId(?)}", (username,))
                result = cursor.fetchone()
                return result[0] if result else None
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch user ID: {e}")
            return None

    def create_message_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TButton",
                        padding=6,
                        relief="flat",
                        background="#4267B2",
                        font=("Segoe UI", 12, "bold"),
                        foreground="#FFFFFF")
        style.map("TButton",
                  background=[("active", "#365899")])

        style.configure("TLabel",
                        background="#f0f2f5",
                        foreground="#333333",
                        font=("Segoe UI", 12))

        style.configure("TEntry",
                        padding=6,
                        relief="flat",
                        font=("Segoe UI", 12))

        style.configure("TListbox",
                        font=("Segoe UI", 12),
                        background="#ffffff",
                        foreground="#000000",
                        selectbackground="#4267B2")

        self.main_frame = tk.Frame(self, bg="#f0f2f5")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.chat_frame = tk.Frame(self.main_frame, bg="#f0f2f5")
        self.chat_frame.pack(side="left", fill="y", padx=10, pady=10, expand=False)

        self.chat_listbox = tk.Listbox(self.chat_frame,
                                       font=("Segoe UI", 12),
                                       bg="#ffffff",
                                       fg="#000000",
                                       selectbackground="#4267B2",
                                       borderwidth=0,
                                       highlightthickness=0)
        self.chat_listbox.pack(fill="y", expand=True)
        self.chat_listbox.bind("<<ListboxSelect>>", self.on_chat_select)

        self.message_frame = tk.Frame(self.main_frame, bg="#ffffff")
        self.message_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.message_list = ScrolledText(self.message_frame,
                                         height=20,
                                         state='disabled',
                                         wrap='word',
                                         font=("Segoe UI", 12),
                                         bg="#ffffff",
                                         fg="#000000",
                                         borderwidth=0,
                                         highlightthickness=0)
        self.message_list.pack(fill="both", expand=True, padx=10, pady=10)

        self.new_message_frame = tk.Frame(self.message_frame, bg="#ffffff")
        self.new_message_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(self.new_message_frame, text="Message:", style="TLabel").pack(side="left")
        self.message_entry = ScrolledText(self.new_message_frame,
                                          height=5,
                                          width=50,
                                          font=("Segoe UI", 12),
                                          borderwidth=1,
                                          relief="solid")
        self.message_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        send_button = ttk.Button(self.new_message_frame, text="Send", command=self.send_message)
        send_button.pack(side="right", pady=10)

        self.new_chat_frame = tk.Frame(self, bg="#f0f2f5")
        self.new_chat_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(self.new_chat_frame, text="Start Chat with:", style="TLabel").pack(side="left")
        self.new_chat_entry = ttk.Entry(self.new_chat_frame, font=("Segoe UI", 12), width=30)
        self.new_chat_entry.pack(side="left", padx=5, fill="x", expand=True)

        new_chat_button = ttk.Button(self.new_chat_frame, text="Start Chat", command=self.start_new_chat)
        new_chat_button.pack(side="left", padx=5)

    def load_chats(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("{CALL GetChats(?)}", (self.user_id,))
                chats = cursor.fetchall()

                self.chat_listbox.delete(0, tk.END)
                for chat in chats:
                    chat_id, user1, user2 = chat
                    other_user = user1 if user1 != self.username else user2
                    self.chat_listbox.insert(tk.END, f"{chat_id}: {other_user}")
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to load chats: {e}")

    def on_chat_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            chat_info = event.widget.get(index)
            chat_id = int(chat_info.split(":")[0])
            self.load_messages(chat_id)

    def load_messages(self, chat_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("{CALL GetMessages(?)}", (chat_id,))
                messages = cursor.fetchall()

                self.message_list.config(state='normal')
                self.message_list.delete('1.0', tk.END)

                for message in messages:
                    sender, content, timestamp = message
                    formatted_time = datetime.strftime(timestamp, "%Y-%m-%d %H:%M:%S")
                    self.message_list.insert(tk.END, f"{sender} ({formatted_time}):\n{content}\n\n")

                self.message_list.config(state='disabled')
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to load messages: {e}")

    def send_message(self):
        selection = self.chat_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a chat first.")
            return

        index = selection[0]
        chat_info = self.chat_listbox.get(index)
        chat_id = int(chat_info.split(":")[0])
        message_content = self.message_entry.get("1.0", tk.END).strip()

        if not message_content:
            messagebox.showerror("Error", "Message content cannot be empty.")
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("{CALL SendMessage(?, ?, ?)}", (chat_id, self.user_id, message_content))
                self.connection.commit()
                messagebox.showinfo("Success", "Message sent successfully.")
                self.message_entry.delete("1.0", tk.END)
                self.load_messages(chat_id)  # Refresh messages
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")

    def start_new_chat(self):
        receiver_username = self.new_chat_entry.get().strip()

        if not receiver_username:
            messagebox.showerror("Error", "Receiver username cannot be empty.")
            return

        receiver_id = self.get_user_id(receiver_username)
        if not receiver_id:
            messagebox.showerror("Error", "Receiver does not exist.")
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("{CALL StartNewChat(?, ?)}", (self.user_id, receiver_id))
                self.connection.commit()
                messagebox.showinfo("Success", "Chat started successfully.")
                self.new_chat_entry.delete(0, tk.END)
                self.load_chats()  # Refresh chat list
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start chat: {e}")




# class UserMessages(tk.Toplevel):
#     def __init__(self, parent, username):
#         super().__init__(parent)
#         self.parent = parent
#         self.username = username
#         self.title("Messages")
#         self.geometry("800x600")
#         self.resizable(False, False)
#         self.configure(bg="#f0f0f0")
#
#         # Fetch user ID
#         self.user_id = self.get_user_id(self.username)
#         if not self.user_id:
#             messagebox.showerror("Error", "Failed to fetch user ID.")
#             self.destroy()
#             return
#
#         # Create UI elements
#         self.create_message_widgets()
#         self.load_messages()
#
#     def create_database_connection(self):
#         server_name = 'localhost\\SQLEXPRESS01'
#         database_name = 'SocialMedia'
#         trusted_connection = 'yes'
#         connection_string = f'DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};Trusted_Connection={trusted_connection};'
#         return pyodbc.connect(connection_string)
#
#     def get_user_id(self, username):
#         connection = self.create_database_connection()
#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT UserID FROM Users WHERE Username = ?", (username,))
#                 result = cursor.fetchone()
#                 return result[0] if result else None
#         finally:
#             connection.close()
#
#     def create_message_widgets(self):
#         # Main frame for messages
#         self.message_frame = tk.Frame(self, bg="#f0f0f0")
#         self.message_frame.pack(fill="both", expand=True, padx=10, pady=10)
#
#         # Listbox with scrollbar for message display
#         self.message_list = ScrolledText(self.message_frame, height=20, state='disabled', wrap='word', font=("Arial", 12))
#         self.message_list.pack(fill="both", expand=True, padx=10, pady=10)
#
#         # Frame for new message entry
#         self.new_message_frame = tk.Frame(self, bg="#f0f0f0")
#         self.new_message_frame.pack(fill="x", padx=10, pady=10)
#
#         tk.Label(self.new_message_frame, text="Send To:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
#         self.receiver_entry = ttk.Entry(self.new_message_frame, font=("Arial", 12))
#         self.receiver_entry.grid(row=0, column=1, sticky="ew", padx=5)
#
#         tk.Label(self.new_message_frame, text="Message:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, sticky="nw")
#         self.message_entry = ScrolledText(self.new_message_frame, height=5, width=50, font=("Arial", 12))
#         self.message_entry.grid(row=1, column=1, padx=5, pady=5)
#
#         send_button = ttk.Button(self.new_message_frame, text="Send", command=self.send_message, style="Custom.TButton")
#         send_button.grid(row=2, column=0, columnspan=2, pady=10)
#
#         # Adding reply and delete buttons
#         self.reply_button = ttk.Button(self.message_frame, text="Reply", command=self.reply_message, style="Custom.TButton")
#         self.reply_button.pack(side="left", padx=5)
#
#         self.delete_button = ttk.Button(self.message_frame, text="Delete", command=self.delete_message, style="Custom.TButton")
#         self.delete_button.pack(side="left", padx=5)
#
#     def load_messages(self):
#         connection = self.create_database_connection()
#         if connection:
#             try:
#                 with connection.cursor() as cursor:
#                     cursor.execute("""
#                         SELECT m.MessageID, u.Username, m.Content, m.Timestamp, m.Read
#                         FROM Messages m
#                         JOIN Users u ON m.SenderID = u.UserID
#                         WHERE m.ReceiverID = ?
#                         ORDER BY m.Timestamp DESC
#                     """, (self.user_id,))
#                     messages = cursor.fetchall()
#
#                     self.message_list.config(state='normal')
#                     self.message_list.delete('1.0', tk.END)
#
#                     self.messages = []  # Store message info
#                     for message in messages:
#                         message_id, sender, content, timestamp, read_status = message
#                         self.message_list.insert(tk.END, f"{sender} ({timestamp}) [{'Read' if read_status else 'Unread'}]:\n{content}\n\n")
#                         self.messages.append((message_id, sender, content, timestamp, read_status))
#
#                     self.message_list.config(state='disabled')
#             except pyodbc.Error as e:
#                 messagebox.showerror("Database Error", f"Failed to load messages: {e}")
#             finally:
#                 connection.close()
#
#     def send_message(self):
#         receiver_username = self.receiver_entry.get()
#         message_content = self.message_entry.get("1.0", tk.END).strip()
#
#         if not receiver_username or not message_content:
#             messagebox.showerror("Error", "Receiver and message content cannot be empty.")
#             return
#
#         receiver_id = self.get_user_id(receiver_username)
#         if not receiver_id:
#             messagebox.showerror("Error", "Receiver does not exist.")
#             return
#
#         connection = self.create_database_connection()
#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     INSERT INTO Messages (SenderID, ReceiverID, Content)
#                     VALUES (?, ?, ?)
#                 """, (self.user_id, receiver_id, message_content))
#                 connection.commit()
#                 messagebox.showinfo("Success", "Message sent successfully.")
#                 self.message_entry.delete("1.0", tk.END)
#                 self.load_messages()  # Refresh messages
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to send message: {e}")
#         finally:
#             connection.close()
#
#     def reply_message(self):
#         selected_text = self.message_list.selection_get()
#         if not selected_text:
#             messagebox.showerror("Error", "No message selected for reply.")
#             return
#
#         sender = selected_text.split(' ')[0]
#         self.receiver_entry.delete(0, tk.END)
#         self.receiver_entry.insert(0, sender)
#         self.message_entry.focus()
#
#     def delete_message(self):
#         try:
#             selected_text = self.message_list.selection_get()
#             if not selected_text:
#                 messagebox.showerror("Error", "No message selected for deletion.")
#                 return
#
#             # Extract message_id from the stored message info
#             for message in self.messages:
#                 message_id, sender, content, timestamp, read_status = message
#                 if sender in selected_text and content in selected_text:
#                     connection = self.create_database_connection()
#                     with connection.cursor() as cursor:
#                         cursor.execute("DELETE FROM Messages WHERE MessageID = ?", (message_id,))
#                         connection.commit()
#                         messagebox.showinfo("Success", "Message deleted successfully.")
#                         self.load_messages()  # Refresh messages
#                     break
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to delete message: {e}")
#
#     def mark_as_read(self, message_id):
#         connection = self.create_database_connection()
#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute("UPDATE Messages SET Read = 1 WHERE MessageID = ?", (message_id,))
#                 connection.commit()
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to mark message as read: {e}")
#         finally:
#             connection.close()
