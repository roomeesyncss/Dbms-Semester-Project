import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from dbcon import DatabaseConnection

class PagesUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Manage Pages")
        self.geometry("700x500")
        self.configure(bg='#f8f9fa')
        self.db = DatabaseConnection()
        self.connection = self.db.create_connection()

        self.create_widgets()

    def create_widgets(self):
        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use('clam')

        style.configure("TNotebook", background='#f8f9fa')
        style.configure("TNotebook.Tab", background='#f8f9fa', font=('Segoe UI', 10, 'bold'), padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#007bff")], foreground=[("selected", "#ffffff")])

        style.configure("TLabel", background='#f8f9fa', font=('Segoe UI', 12))
        style.configure("TEntry", font=('Segoe UI', 12), padding=5)
        style.configure("TButton", font=('Segoe UI', 12, 'bold'), background='#007bff', foreground='#ffffff', padding=5)
        style.map("TButton", background=[("active", "#0056b3")], foreground=[("active", "#ffffff")])

        create_tab = ttk.Frame(nb, style="TFrame")
        nb.add(create_tab, text="Create Page")

        ttk.Label(create_tab, text="Title:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.title_entry = ttk.Entry(create_tab, width=50)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(create_tab, text="Description:").grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        self.desc_entry = tk.Text(create_tab, width=50, height=6, font=('Segoe UI', 12), wrap="word", bd=2, relief="groove")
        self.desc_entry.grid(row=1, column=1, padx=10, pady=10)

        create_button = ttk.Button(create_tab, text="Create Page", command=self.create_page)
        create_button.grid(row=2, column=1, padx=10, pady=20, sticky="e")

        member_tab = ttk.Frame(nb, style="TFrame")
        nb.add(member_tab, text="Add Page Member")

        ttk.Label(member_tab, text="Page ID:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.page_id_entry = ttk.Entry(member_tab, width=50)
        self.page_id_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(member_tab, text="User ID:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.user_id_entry = ttk.Entry(member_tab, width=50)
        self.user_id_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(member_tab, text="Role:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.role_entry = ttk.Entry(member_tab, width=50)
        self.role_entry.grid(row=2, column=1, padx=10, pady=10)

        add_member_button = ttk.Button(member_tab, text="Add Member", command=self.add_member)
        add_member_button.grid(row=3, column=1, padx=10, pady=20, sticky="e")

        view_tab = ttk.Frame(nb, style="TFrame")
        nb.add(view_tab, text="View Pages")

        self.pages_listbox = tk.Listbox(view_tab, font=('Segoe UI', 12), bd=2, relief="groove", bg='#ffffff')
        self.pages_listbox.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        view_button = ttk.Button(view_tab, text="Load Pages", command=self.show_pg)
        view_button.pack(pady=10)

    def create_page(self):
        title = self.title_entry.get().strip()
        description = self.desc_entry.get("1.0", tk.END).strip()
        created_by = 1

        if not title:
            messagebox.showerror("Error", "Title is required")
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("EXEC CreatePage @Title=?, @Description=?, @CreatedBy=?", (title, description, created_by))
                self.connection.commit()
                messagebox.showinfo("Success", "Page created successfully")
                self.title_entry.delete(0, tk.END)
                self.desc_entry.delete("1.0", tk.END)
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to create page: {e}")

    def add_member(self):
        page_id = self.page_id_entry.get().strip()
        user_id = self.user_id_entry.get().strip()
        role = self.role_entry.get().strip()

        if not page_id or not user_id or not role:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("EXEC AddPageMember @PageID=?, @UserID=?, @Role=?", (page_id, user_id, role))
                self.connection.commit()
                messagebox.showinfo("Success", "Member added successfully")
                self.page_id_entry.delete(0, tk.END)
                self.user_id_entry.delete(0, tk.END)
                self.role_entry.delete(0, tk.END)
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to add member: {e}")

    def show_pg(self):
        self.pages_listbox.delete(0, tk.END)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("EXEC ViewPages")
                pages = cursor.fetchall()
                for page in pages:
                    page_info = f"ID: {page.PageID}, Title: {page.Title}, Created By: {page.CreatedBy}, Created At: {page.CreatedAt}"
                    self.pages_listbox.insert(tk.END, page_info)
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to load pages: {e}")
