import tkinter as tk
from tkinter import ttk, messagebox
from dbcon import DatabaseConnection
from ttkthemes import ThemedTk


class PagesUI(ThemedTk):
    def __init__(self, user_id):
        super().__init__(theme="breeze")
        self.user_id = user_id
        self.title("Page Management")
        self.geometry("1200x800")
        self.configure(bg="#f0f0f0")

        self.db = DatabaseConnection()
        self.connection = self.db.create_connection()

        self.style = ttk.Style()
        self.configure_style()

        self.create_widgets()
        self.load_pages()

    def configure_style(self):
        self.style.configure('TLabel', background="#f0f0f0", font=('Helvetica', 12), foreground="#333333")
        self.style.configure('TEntry', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12, 'bold'), background="#6200ea", foreground="#ffffff")
        self.style.map('TButton', background=[('active', '#6200ea'), ('!disabled', '#6200ea')],
                       foreground=[('active', '#ffffff')])
        self.style.configure('Card.TFrame', background="#ffffff", relief='groove', borderwidth=2)
        self.style.configure('Card.TLabel', background="#ffffff", font=('Helvetica', 10))

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self)

        self.create_page_tab = ttk.Frame(self.tab_control, padding=10, style='TFrame')
        self.view_pages_tab = ttk.Frame(self.tab_control, padding=10, style='TFrame')
        self.manage_members_tab = ttk.Frame(self.tab_control, padding=10, style='TFrame')

        self.tab_control.add(self.create_page_tab, text='Create Page')
        self.tab_control.add(self.view_pages_tab, text='View Pages')
        self.tab_control.add(self.manage_members_tab, text='Manage Members')
        self.tab_control.pack(expand=1, fill='both')

        self.create_page_widgets()
        self.view_pages_widgets()
        self.manage_members_widgets()

    def create_page_widgets(self):
        font_style = ('Helvetica', 12)

        ttk.Label(self.create_page_tab, text="Page Title", font=font_style).grid(row=0, column=0, padx=10, pady=10,
                                                                                 sticky='w')
        self.title_entry = ttk.Entry(self.create_page_tab, font=font_style)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.create_page_tab, text="Description", font=font_style).grid(row=1, column=0, padx=10, pady=10,
                                                                                  sticky='w')
        self.desc_entry = ttk.Entry(self.create_page_tab, font=font_style)
        self.desc_entry.grid(row=1, column=1, padx=10, pady=10)

        create_button = ttk.Button(self.create_page_tab, text="Create Page", command=self.create_page)
        create_button.grid(row=2, column=1, padx=10, pady=20, sticky="e")

    def create_page(self):
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()

        if not title:
            messagebox.showerror("Error", "Title is required")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("EXEC CreatePage @Title=?, @Description=?, @CreatedBy=?", (title, description, self.user_id))
            self.connection.commit()
            cursor.close()

            messagebox.showinfo("Success", "Page created successfully")
            self.title_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.load_pages()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to create page: {e}")

    def view_pages_widgets(self):
        self.pages_frame = ttk.Frame(self.view_pages_tab)
        self.pages_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        self.pages_canvas = tk.Canvas(self.pages_frame, bg="#f0f0f0")
        self.pages_scrollbar = ttk.Scrollbar(self.pages_frame, orient=tk.VERTICAL, command=self.pages_canvas.yview)
        self.pages_scrollable_frame = ttk.Frame(self.pages_canvas)

        self.pages_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.pages_canvas.configure(
                scrollregion=self.pages_canvas.bbox("all")
            )
        )

        self.pages_canvas.create_window((0, 0), window=self.pages_scrollable_frame, anchor="nw")
        self.pages_canvas.configure(yscrollcommand=self.pages_scrollbar.set)

        self.pages_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.pages_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


    def load_pages(self):
        for widget in self.pages_scrollable_frame.winfo_children():
            widget.destroy()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("EXEC ViewPagesWithDetails @UserID=?", self.user_id)
                pages = cursor.fetchall()
                for page in pages:
                    self.create_page_card(page)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load pages: {e}")

    def create_page_card(self, page):
        card_frame = ttk.Frame(self.pages_scrollable_frame, style='Card.TFrame', padding=10)
        card_frame.pack(fill=tk.X, padx=10, pady=5, expand=True)

        title_label = ttk.Label(card_frame, text=f"Page Name: {page.PageName}", style='Card.TLabel')
        title_label.grid(row=0, column=0, sticky='w')

        creator_label = ttk.Label(card_frame, text=f"Created By: {page.Creator}", style='Card.TLabel')
        creator_label.grid(row=1, column=0, sticky='w')

        created_at_label = ttk.Label(card_frame, text=f"Created At: {page.CreatedAt}", style='Card.TLabel')
        created_at_label.grid(row=2, column=0, sticky='w')

        view_members_button = ttk.Button(card_frame, text="View Members",
                                         command=lambda page_id=page.PageID: self.show_members(page_id))

        view_members_button.grid(row=3, column=0, pady=10, sticky='e')

    def show_members(self, page_id):
        members_window = tk.Toplevel(self)
        members_window.title("Page Members")
        members_window.geometry("600x400")

        members_frame = ttk.Frame(members_window)
        members_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tree = ttk.Treeview(members_frame, columns=('Username', 'Role', 'Added By', 'Added At'), show='headings')
        tree.heading('Username', text='Username')
        tree.heading('Role', text='Role')
        tree.heading('Added By', text='Added By')
        tree.heading('Added At', text='Added At')
        tree.pack(fill=tk.BOTH, expand=True)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("EXEC GetPageMembers @PageID=?", page_id)
                members = cursor.fetchall()
                for member in members:
                    tree.insert('', 'end', values=(member.Username, member.RoleName, member.AddedBy, member.AddedAt))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load members: {e}")

    def load_admin_page_names(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("EXEC ViewPagesWithDetails @UserID=?", self.user_id)
            pages = cursor.fetchall()
            cursor.close()

            admin_pages = [f"{page.PageName} (ID: {page.PageID})" for page in pages if self.is_user_admin(page.PageID)]
            if not admin_pages:
                messagebox.showinfo("Info", "You are not an admin for any pages.")
            self.page_name_combobox['values'] = admin_pages
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load page names: {e}")

    def manage_members_widgets(self):
        font_style = ('Helvetica', 12)

        ttk.Label(self.manage_members_tab, text="Page Name", font=font_style).grid(row=0, column=0, padx=10, pady=10,
                                                                                   sticky='w')
        self.page_name_combobox = ttk.Combobox(self.manage_members_tab, font=font_style)
        self.page_name_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.load_admin_page_names()

        ttk.Label(self.manage_members_tab, text="User Name", font=font_style).grid(row=1, column=0, padx=10, pady=10,
                                                                                   sticky='w')
        self.user_name_combobox = ttk.Combobox(self.manage_members_tab, font=font_style)
        self.user_name_combobox.grid(row=1, column=1, padx=10, pady=10)
        self.load_user_names()

        ttk.Label(self.manage_members_tab, text="Role", font=font_style).grid(row=2, column=0, padx=10, pady=10,
                                                                              sticky='w')
        self.role_combobox = ttk.Combobox(self.manage_members_tab, font=font_style, values=["Admin", "Member"])
        self.role_combobox.grid(row=2, column=1, padx=10, pady=10)

        add_member_button = ttk.Button(self.manage_members_tab, text="Add Member", command=self.add_member)
        add_member_button.grid(row=3, column=1, padx=10, pady=20, sticky="e")

    def load_user_names(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT UserID, Username FROM [User]")
            users = cursor.fetchall()
            cursor.close()

            self.user_name_combobox['values'] = [f"{user.Username} (ID: {user.UserID})" for user in users]
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load user names: {e}")

    def add_member(self):
        page_selection = self.page_name_combobox.get().strip()
        user_selection = self.user_name_combobox.get().strip()
        role = self.role_combobox.get().strip()

        if not page_selection or not user_selection or not role:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            page_id = int(page_selection.split(" (ID: ")[1][:-1])
            user_id = int(user_selection.split(" (ID: ")[1][:-1])
            role_id = 1 if role == "Admin" else 2  # Assuming role IDs: Admin=1, Member=2

            # Check if the current user is an admin of the page
            if not self.is_user_admin(page_id):
                messagebox.showerror("Permission Denied", "Only admins can add members to the page")
                return

            cursor = self.connection.cursor()
            cursor.execute("EXEC AddPageMember @PageID=?, @UserID=?, @RoleID=?, @AddedBy=?",
                           (page_id, user_id, role_id, self.user_id))
            self.connection.commit()
            cursor.close()

            messagebox.showinfo("Success", "Member added successfully")
            self.page_name_combobox.set('')
            self.user_name_combobox.set('')
            self.role_combobox.set('')
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add member: {e}")

    def is_user_admin(self, page_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT RoleID FROM PageMembers WHERE PageID = ? AND UserID = ?", (page_id, self.user_id))
            result = cursor.fetchone()
            cursor.close()

            if result:
                if result[0] == 1:  # RoleID 1 is Admin
                    return True
                else:
                    return False
            else:
                messagebox.showwarning("Warning", "No role found for the user on this page.")
                return False
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to check admin status: {e}")
            return False

