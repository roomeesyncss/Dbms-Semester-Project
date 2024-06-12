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
                self.chat_id_to_username = {}  # Dictionary to map chat_id to other user's username
                for chat in chats:
                    chat_id, user1, user2 = chat
                    other_user = user1 if user1 != self.username else user2
                    self.chat_id_to_username[chat_id] = other_user  # Map chat_id to other user's username
                    self.chat_listbox.insert(tk.END, other_user)  # Insert only the other user's name
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to load chats: {e}")

    def on_chat_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            other_user = event.widget.get(index)  # Get the username of the selected chat
            chat_id = None
            for cid, username in self.chat_id_to_username.items():
                if username == other_user:
                    chat_id = cid
                    break
            if chat_id:
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
        other_user = self.chat_listbox.get(index)
        chat_id = None
        for cid, username in self.chat_id_to_username.items():
            if username == other_user:
                chat_id = cid
                break

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
