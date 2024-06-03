import tkinter as tk
from tkinter import ttk
import pyodbc
from tkinter import messagebox
from userpfp import UserPfP
from usermsg import UserMessages
import threading
from datetime import  datetime
from notif import NotificationsPage
from usersettings import  SettingsUI
from userpage import PagesUI
class UserMFeed(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.geometry('1200x800')
        self.title('User Feed')
        self.username = username
        self.create_widgets()
        self.sidebar_frame.pack_forget()

    def create_database_connection(self):
        server_name = 'localhost\\SQLEXPRESS'
        database_name = 'Facebook'
        trusted_connection = 'yes'
        connection_string = f'DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};Trusted_Connection={trusted_connection};'
        connection = pyodbc.connect(connection_string)
        return connection

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        main_frame = tk.Frame(self, bg='#f0f2f5')
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.sidebar_frame = tk.Frame(main_frame, bg='#3b5998', width=250)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        sidebar_button_1 = tk.Button(self.sidebar_frame, text='Function 1', font=('Segoe UI', 12), fg='white',
                                     bg='#3b5998', activebackground='#4e69a2', activeforeground='white', relief=tk.FLAT,
                                     command=lambda: None)
        sidebar_button_1.pack(pady=15, padx=20, fill=tk.X)

        Mcframecon = tk.Frame(main_frame, bg='#f0f2f5')
        Mcframecon.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        navbar_frame = tk.Frame(Mcframecon, bg='#3b5998', padx=20, pady=10)
        navbar_frame.pack(fill=tk.X)

        tk.Label(navbar_frame, text='Facebook', font=('Segoe UI', 20, 'bold'), fg='white', bg='#3b5998').pack(
            side=tk.LEFT, padx=10)

        nav_buttons_frame = tk.Frame(navbar_frame, bg='#3b5998')
        nav_buttons_frame.pack(side=tk.LEFT, padx=10)

        nav_buttons = [
            ('Home', self.go_home),
            ('Profile', self.go_profile),
            ('Friends', self.go_friends),
            ('Notifications', self.go_notifications),
            ('Messages', self.go_messages),
            ('Pages', self.go_pages),
            ('Settings', self.go_settings),

            ('Sidebar', self.toggle_sidebar)
        ]

        for button_text, command in nav_buttons:
            nav_button = tk.Button(nav_buttons_frame, text=button_text, font=('Segoe UI', 12), fg='white', bg='#3b5998',
                                   activebackground='#4e69a2', activeforeground='white', relief=tk.FLAT,
                                   command=command)
            nav_button.pack(side=tk.LEFT, padx=10)

        feed_frame = tk.Frame(Mcframecon, bg='#f0f2f5')
        feed_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.canva_post = tk.Canvas(feed_frame, highlightthickness=0, bg='#f0f2f5')
        self.canva_post.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(feed_frame, orient=tk.VERTICAL, command=self.canva_post.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canva_post.configure(yscrollcommand=scrollbar.set)

        self.post_frame = tk.Frame(self.canva_post, bg='#f0f2f5')
        self.post_frame.bind('<Configure>',
                             lambda e: self.canva_post.configure(scrollregion=self.canva_post.bbox('all')))
        self.canva_post.create_window((0, 0), window=self.post_frame, anchor='nw')

        self.load_posts()

        buttons_frame = tk.Frame(Mcframecon, pady=10, bg='#f0f2f5')
        buttons_frame.pack(fill=tk.X)

        create_post_button = tk.Button(buttons_frame, text="Create Post", font=('Segoe UI', 12), fg='white',
                                       bg='#3b5998', activebackground='#4e69a2', activeforeground='white',
                                       relief=tk.FLAT, command=self.create_post)
        create_post_button.pack(side=tk.LEFT, padx=10)

        logout_button = tk.Button(buttons_frame, text="Logout", font=('Segoe UI', 12), fg='white', bg='#3b5998',
                                  activebackground='#4e69a2', activeforeground='white', relief=tk.FLAT,
                                  command=self.logout)
        logout_button.pack(side=tk.RIGHT, padx=10)

    def toggle_sidebar(self):
        if self.sidebar_frame.winfo_viewable():
            self.sidebar_frame.pack_forget()
        else:
            self.sidebar_frame.pack(side=tk.LEFT, fill=tk.BOTH)

    def load_posts(self):
        connection = self.create_database_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("EXEC GetUserPosts @Username = ?", (self.username,))
                posts = cursor.fetchall()
        finally:
            connection.close()

        for widget in self.post_frame.winfo_children():
            widget.destroy()

        for post in posts:
            username, content, timestamp, likes, comments, shares, post_id = post
            self.create_post_widget(username, content, timestamp, likes, comments, post_id, shares)

    def create_post_widget(self, username, content, timestamp, likes, comments, post_id, shares):
        post_frame = tk.Frame(self.post_frame, bg='#ffffff', padx=20, pady=15, relief=tk.RAISED, borderwidth=1)
        post_frame.pack(fill=tk.X, padx=10, pady=10)

        user_label = tk.Label(post_frame, text=username, font=('Leelawadee', 14, 'bold'), bg='#ffffff', fg='#3a4be8')
        user_label.pack(anchor='w')

        content_label = tk.Label(post_frame, text=content, wraplength=800, justify=tk.LEFT, bg='#ffffff',
                                 font=('Segoe UI', 12))
        content_label.pack(anchor='w')

        timestamp_label = tk.Label(post_frame, text=timestamp.strftime('%Y-%m-%d %H:%M:%S'), bg='#ffffff',
                                   font=('Segoe UI', 6))
        timestamp_label.pack(anchor='e')

        action_frame = tk.Frame(post_frame, bg='#ffffff')
        action_frame.pack(fill=tk.X, pady=10)

        def share_post(post_id):
            user_id = self.get_user_id()
            if not user_id:
                messagebox.showerror("Error", "Failed to get user ID.")
                return

            connection = self.create_database_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        EXEC SharePost2 @PostID = ?, @UserID = ?
                    """, (post_id, user_id))
                    updated_share_count = cursor.fetchone()[0]
                    shares_label.config(text=f'🔄 {updated_share_count}')

                    connection.commit()
                    messagebox.showinfo("Success", "Post shared successfully woho.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to share post: {e}")
            finally:
                connection.close()

        def toggle_like_in_background(post_id, likes_label):
            connection = self.create_database_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("EXEC ToggleLikePost @Username = ?, @PostID = ?", (username, post_id))
                    result = cursor.fetchone()
                    if result:
                        like_count = result[0]
                        likes_label.config(text=f'❤ {like_count}')
                        # self.load_posts()

                    connection.commit()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to toggle like status: {e}")
            finally:
                connection.close()

        def like_post(post_id, likes_label):
            threading.Thread(target=toggle_like_in_background, args=(post_id, likes_label)).start()
        def load_comments(post_id):
            comments_list.delete(0, tk.END)
            connection = self.create_database_connection()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            SELECT u.Username, c.Content, c.Timestamp
                            FROM Comments c
                            JOIN Users u ON c.UserID = u.UserID
                            WHERE c.PostID = ?
                            ORDER BY c.Timestamp DESC
                        """, (post_id,))
                        cmt = cursor.fetchall()

                        for comment in cmt:
                            username, content, timestamp = comment
                            try:
                                formatted_time = datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S.%f').strftime(
                                    '%Y-%m-%d %H:%M')
                            except ValueError:
                                formatted_time = datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S').strftime(
                                    '%Y-%m-%d %H:%M')
                            comments_list.insert(tk.END, f"{username} ({formatted_time}): {content}")

                except pyodbc.Error as e:
                    messagebox.showerror("Database Error", f"Failed to load comments: {e}")
                finally:
                    connection.close()

        def comment_post(post_id):
            comment_content = comment_entry.get("1.0", tk.END).strip()
            if not comment_content:
                messagebox.showerror("Error", "Comment content cannot be empty.")
                return

            user_id = self.get_user_id()
            if not user_id:
                messagebox.showerror("Error", "Failed to fetch user ID.")
                return

            connection = self.create_database_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Comments (PostID, UserID, Content, Timestamp)
                        VALUES (?, ?, ?, ?)
                    """, (post_id, user_id, comment_content, datetime.now()))
                    connection.commit()

                comment_entry.delete("1.0", tk.END)
                load_comments(post_id)
                messagebox.showinfo("Success", "Comment posted successfully!")
            except pyodbc.Error as e:
                messagebox.showerror("Database Error", f"Failed to post comment: {e}")
            finally:
                connection.close()

        def open_cmt():
            if comments_section_frame.winfo_viewable():
                comments_section_frame.pack_forget()
                toggle_button.config(text=">>")
            else:
                comments_section_frame.pack(fill=tk.X, padx=10, pady=5)
                load_comments(post_id)
                toggle_button.config(text="<<")

        like_button = tk.Button(action_frame, text='Like', font=('Segoe UI', 10), fg='#3b5998', bg='#ffffff',
                                activebackground='#e9ebee', activeforeground='#3b5998', relief=tk.FLAT,
                                command=lambda: like_post(post_id, likes_label))
        like_button.pack(side=tk.LEFT, padx=5)

        comment_button = tk.Button(action_frame, text='Comment', font=('Segoe UI', 10), fg='#3b5998', bg='#ffffff',
                                   activebackground='#e9ebee', activeforeground='#3b5998', relief=tk.FLAT,
                                   command=open_cmt)
        comment_button.pack(side=tk.LEFT, padx=5)

        share_button = tk.Button(action_frame, text='Share', font=('Segoe UI', 10), fg='#3b5998', bg='#ffffff',
                                 activebackground='#e9ebee', activeforeground='#3b5998', relief=tk.FLAT,
                                 command=lambda p=post_id: share_post(p))
        share_button.pack(side=tk.LEFT, padx=5)

        likes_label = tk.Label(action_frame, text=f'❤ {likes}', font=('Segoe UI', 10), fg='#3b5998', bg='#ffffff')
        likes_label.pack(side=tk.LEFT, padx=5)


        comments_label = tk.Label(action_frame, text=f'💬 {comments}', font=('Segoe UI', 10), fg='#3b5998', bg='#ffffff')
        comments_label.pack(side=tk.LEFT, padx=5)

        shares_label = tk.Label(action_frame, text=f'🔄 {shares}', font=('Segoe UI', 10), fg='#3b5998', bg='#ffffff')
        shares_label.pack(side=tk.LEFT, padx=5)

        comments_section_frame = tk.Frame(post_frame, bg='#f0f2f5')
        comments_section_frame.pack_forget()  # Initially hide the comments section

        comments_list = tk.Listbox(comments_section_frame, height=3, width=40, font=('Segoe UI', 10), bg='#f0f2f5')
        comments_list.pack(side=tk.TOP, fill=tk.X, expand=True, padx=5, pady=5)

        comment_entry = tk.Text(comments_section_frame, height=1, width=40, font=('Segoe UI', 10))
        comment_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        post_comment_button = tk.Button(comments_section_frame, text="Post", font=('Segoe UI', 10), fg='white',
                                        bg='#3b5998', activebackground='#4e69a2', activeforeground='white',
                                        relief=tk.FLAT,
                                        command=lambda p=post_id: comment_post(p))
        post_comment_button.pack(side=tk.RIGHT, padx=5)

        toggle_button = tk.Button(post_frame, text=">>", font=('Segoe UI', 10), fg='#3b5998', bg='#ffffff',
                                  activebackground='#e9ebee', activeforeground='#3b5998', relief=tk.FLAT,
                                  command=open_cmt)
        toggle_button.pack(side=tk.RIGHT, padx=5, pady=5)


    def go_home(self):
        pass

    def go_profile(self):
        profile_window = UserPfP(self, username=self.username)
        profile_window.grab_set()

    def go_friends(self):
        connection = self.create_database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT UserID FROM Users WHERE Username = ?", (self.username,))
                user_id = cursor.fetchone()[0]

                cursor.execute("""
                     SELECT Users.Username
                     FROM Friendships
                     INNER JOIN Users ON Friendships.UserID2 = Users.UserID
                     WHERE Friendships.UserID1 = ? AND Friendships.Status = 'Accepted'
                     UNION
                     SELECT Users.Username
                     FROM Friendships
                     INNER JOIN Users ON Friendships.UserID1 = Users.UserID
                     WHERE Friendships.UserID2 = ? AND Friendships.Status = 'Accepted'
                 """, (user_id, user_id))
                friends = cursor.fetchall()
        finally:
            connection.close()

        def remove_friend(friend_name):
            connection = self.create_database_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT UserID FROM Users WHERE Username = ?", (friend_name,))
                    friend_id = cursor.fetchone()[0]

                    cursor.execute("DELETE FROM Friendships WHERE UserID1 = ? AND UserID2 = ?", (user_id, friend_id))
                    connection.commit()
            finally:
                connection.close()

            friends_dialog.destroy()
            self.go_friends()

        friends_dialog = tk.Toplevel(self)
        friends_dialog.title("Friends")
        friends_dialog.geometry("600x500")
        friends_dialog.configure(bg="#f0f2f5")

        friends_frame = tk.Frame(friends_dialog, bg="#f0f2f5")
        friends_frame.pack(padx=20, pady=20)

        title_label = tk.Label(friends_frame, text="Your Friends", font=("Segoe UI", 20, "bold"), bg="#f0f2f5",
                               fg="#3b5998")
        title_label.pack(pady=10)

        accept_button = tk.Button(friends_frame, text="Seee your Friend Request", font=("Segoe UI", 12), bg="#3b5998",
                                  fg="#ffffff",
                                  command=self.accept_friend_request)
        accept_button.pack(pady=10)

        add_button = tk.Button(friends_frame, text="add new people", font=("Segoe UI", 12), bg="#3b5998",
                                  fg="#ffffff",
                                  command=self.add_friend)
        add_button.pack(pady=10)
        friends_canvas = tk.Canvas(friends_frame, bg="#f0f2f5", highlightthickness=0)
        friends_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        friends_scrollbar = tk.Scrollbar(friends_frame, orient=tk.VERTICAL, command=friends_canvas.yview)
        friends_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        friends_canvas.configure(yscrollcommand=friends_scrollbar.set)
        friends_canvas.bind('<Configure>', lambda e: friends_canvas.configure(scrollregion=friends_canvas.bbox("all")))

        friends_interior = tk.Frame(friends_canvas, bg="#f0f2f5")
        friends_canvas.create_window((0, 0), window=friends_interior, anchor="nw")

        for friend in friends:
            friend_name = friend[0]
            friend_frame = tk.Frame(friends_interior, bg="#ffffff", relief=tk.RAISED, borderwidth=1)
            friend_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

            friend_name_label = tk.Label(friend_frame, text=friend_name, font=("Segoe UI", 14), bg="#ffffff",
                                         fg="#3b5998")
            friend_name_label.pack(side=tk.LEFT, padx=10, pady=10)

            remove_button = tk.Button(friend_frame, text="Remove", font=("Segoe UI", 12), bg="#3b5998", fg="#ffffff",
                                      command=lambda f=friend_name: remove_friend(f))
            remove_button.pack(side=tk.RIGHT, padx=10, pady=10)



    def accept_friend_request(self):
        request_window = tk.Toplevel(self)
        request_window.title("Manage Friend Requests")
        request_window.geometry("550x500")
        request_window.configure(bg="#f0f2f5")

        title_label = tk.Label(request_window, text="Manage Friend Requests", font=("Segoe UI", 18, "bold"),
                               bg="#f0f2f5", fg="#3b5998")
        title_label.pack(pady=10)

        connection = self.create_database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT UserID FROM Users WHERE Username = ?", (self.username,))
                user_id = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT Users.Username, Friendships.FriendshipID
                    FROM Friendships
                    INNER JOIN Users ON Friendships.UserID1 = Users.UserID
                    WHERE Friendships.UserID2 = ? AND Friendships.Status = 'Pending'
                """, (user_id,))
                pending_requests = cursor.fetchall()

            if not pending_requests:
                no_requests_label = tk.Label(request_window, text="You have no pending friend requests.",
                                             font=("Segoe UI", 14), bg="#f0f2f5", fg="#3b5998")
                no_requests_label.pack(pady=20)
                return

            results_frame = tk.Frame(request_window, bg="#f0f2f5")
            results_frame.pack(pady=10, fill=tk.BOTH, expand=True)

            results_canvas = tk.Canvas(results_frame, bg="#f0f2f5", highlightthickness=0)
            results_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            results_scrollbar = tk.Scrollbar(results_frame, orient=tk.VERTICAL, command=results_canvas.yview)
            results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            results_canvas.configure(yscrollcommand=results_scrollbar.set)
            results_canvas.bind('<Configure>',
                                lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all")))

            results_interior = tk.Frame(results_canvas, bg="#f0f2f5")
            results_canvas.create_window((0, 0), window=results_interior, anchor="nw")

            def update_request_status(friendship_id, username, status):
                connection = self.create_database_connection()
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("UPDATE Friendships SET Status = ? WHERE FriendshipID = ?",
                                       (status, friendship_id))
                        connection.commit()
                        messagebox.showinfo("Success", f"Friend request {status.lower()}ed for {username}.")
                finally:
                    connection.close()
                request_window.destroy()
                self.accept_friend_request()

            for username, friendship_id in pending_requests:
                card_frame = tk.Frame(results_interior, bg="#ffffff", relief=tk.RAISED, borderwidth=1)
                card_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

                user_label = tk.Label(card_frame, text=username, font=("Segoe UI", 14), bg="#ffffff", fg="#3b5998")
                user_label.pack(side=tk.LEFT, padx=10, pady=10)

                button_frame = tk.Frame(card_frame, bg="#ffffff")
                button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

                accept_button = tk.Button(button_frame, text="Accept", font=("Segoe UI", 12), bg="#3b5998",
                                          fg="#ffffff",
                                          command=lambda fid=friendship_id, uname=username: update_request_status(fid,
                                                                                                                  uname,
                                                                                                                  'Accepted'))
                accept_button.pack(side=tk.LEFT, padx=5)

                reject_button = tk.Button(button_frame, text="Reject", font=("Segoe UI", 12), bg="#ff4d4d",
                                          fg="#ffffff",
                                          command=lambda fid=friendship_id, uname=username: update_request_status(fid,
                                                                                                                  uname,
                                                                                                                  'Rejected'))
                reject_button.pack(side=tk.LEFT, padx=5)

        finally:
            connection.close()

    def go_messages(self):
        UserMessages(self, self.username)

    def go_settings(self):
        user_id = self.get_user_id()
        if user_id:
            SettingsUI(self, user_id)
        else:
            messagebox.showerror("Error", "Failed to get user ID.")

    def add_friend(self):
        add_friend_window = tk.Toplevel(self)
        add_friend_window.title("Add Friend")
        add_friend_window.geometry("550x500")
        add_friend_window.configure(bg="#f0f2f5")

        title_label = tk.Label(add_friend_window, text="Add Friend", font=("Segoe UI", 18, "bold"), bg="#f0f2f5",
                               fg="#3b5998")
        title_label.pack(pady=10)

        search_frame = tk.Frame(add_friend_window, bg="#f0f2f5")
        search_frame.pack(pady=10)

        search_label = tk.Label(search_frame, text="Search for users:", font=("Segoe UI", 12), bg="#f0f2f5",
                                fg="#3b5998")
        search_label.pack(side=tk.LEFT, padx=10)

        search_entry = tk.Entry(search_frame, font=("Segoe UI", 12))
        search_entry.pack(side=tk.LEFT, padx=10)

        search_button = tk.Button(search_frame, text="Search", font=("Segoe UI", 12), bg="#3b5998", fg="#ffffff",
                                  command=lambda: search_users(search_entry.get()))
        search_button.pack(side=tk.LEFT, padx=10)

        results_frame = tk.Frame(add_friend_window, bg="#f0f2f5")
        results_frame.pack(pady=10)

        results_canvas = tk.Canvas(results_frame, bg="#f0f2f5", highlightthickness=0)
        results_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        results_scrollbar = tk.Scrollbar(results_frame, orient=tk.VERTICAL, command=results_canvas.yview)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        results_canvas.configure(yscrollcommand=results_scrollbar.set)
        results_canvas.bind('<Configure>', lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all")))

        results_interior = tk.Frame(results_canvas, bg="#f0f2f5")
        results_canvas.create_window((0, 0), window=results_interior, anchor="nw")

        def search_users(query):
            connection = self.create_database_connection()
            try:
                with connection.cursor() as cursor:
                    user_id = self.get_user_id()

                    cursor.execute("""
                        SELECT Users.Username
                        FROM Users
                        WHERE Users.UserID NOT IN (
                            SELECT UserID2
                            FROM Friendships
                            WHERE UserID1 = ?
                            UNION
                            SELECT UserID1
                            FROM Friendships
                            WHERE UserID2 = ?
                        ) AND Users.Username LIKE ?
                    """, (user_id, user_id, f"%{query}%"))
                    users = cursor.fetchall()
            finally:
                connection.close()

            for widget in results_interior.winfo_children():
                widget.destroy()

            if users:
                for user in users:
                    username = user[0]
                    user_frame = tk.Frame(results_interior, bg="#ffffff", relief=tk.RAISED, borderwidth=1)
                    user_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

                    user_label = tk.Label(user_frame, text=username, font=("Segoe UI", 14), bg="#ffffff", fg="#3b5998")
                    user_label.pack(side=tk.LEFT, padx=10, pady=10)

                    add_button = tk.Button(user_frame, text="Add", font=("Segoe UI", 12), bg="#3b5998", fg="#ffffff",
                                           command=lambda u=username: send_friend_request(u))
                    add_button.pack(side=tk.RIGHT, padx=10, pady=10)
            else:
                no_results_label = tk.Label(results_interior, text="No users found.", font=("Segoe UI", 14),
                                            bg="#f0f2f5", fg="#3b5998")
                no_results_label.pack(pady=10)

        def send_friend_request(friend_username):
            connection = self.create_database_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT UserID FROM Users WHERE Username = ?", (friend_username,))
                    friend_id = cursor.fetchone()
                    if friend_id:
                        cursor.execute("INSERT INTO Friendships (UserID1, UserID2, Status) VALUES (?, ?, 'Pending')",
                                       (self.get_user_id(), friend_id[0]))
                        connection.commit()
                        tk.messagebox.showinfo("Success", f"Friend request sent to {friend_username}.")
                    else:
                        tk.messagebox.showerror("Error", f"User '{friend_username}' not found.")
            finally:
                connection.close()

            search_entry.delete(0, tk.END)
            search_users("")

    def get_user_id(self):
        connection = self.create_database_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT UserID FROM Users WHERE Username = ?", (self.username,))
                result = cursor.fetchone()
                if result:
                    user_id = result[0]
                    print(f"UserID for '{self.username}': {user_id}")
                else:
                    user_id = None
                    print(f"Username '{self.username}' not found in the Users table.")
        except pyodbc.Error as e:
            print(f"Error fetching UserID: {e}")
            user_id = None
        finally:
            connection.close()
        return user_id

    def create_post(self):
        dialog = PostDialog(self, self.username)
        self.wait_window(dialog)

        if dialog.post_content:
            connection = self.create_database_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("EXEC GetUserId ?", (self.username,))
                    user_id = cursor.fetchone()[0]
                    cursor.execute("EXEC CreatePost ?, ?", (user_id, dialog.post_content))
                    connection.commit()
                self.load_posts()
            finally:
                connection.close()
    def go_notifications(self):
        user_id = self.get_user_id()
        if not user_id:
            messagebox.showerror("Error", "Failed to fetch user ID.")
            return

        notifications_window = NotificationsPage(self, user_id)
        notifications_window.grab_set()
    def go_pages(self):
        user_id = self.get_user_id()
        if user_id:
            PagesUI(self)
        else:
            messagebox.showerror("Error", "Failed to get user ID.")

    def logout(self):
        self.destroy()
        self.parent.deiconify()



# class SignupUserFeed(tk.Toplevel):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#         self.geometry('800x600')
#         self.title('User Feed')
#         self.create_widgets()
#
#     def create_widgets(self):
#         # Create components for user feed window for signup users
#         tk.Label(self, text="Signup User Feed", font=("Arial", 20)).pack(pady=20)
#         tk.Button(self, text="Load Posts", command=self.load_posts).pack(pady=10)
#         self.posts_text = tk.Text(self, width=60, height=20)
#         self.posts_text.pack(pady=10)
#         tk.Button(self, text="Logout", command=self.logout).pack(pady=10)
#
#     def load_posts(self):
#         pass
#
#
#     def logout(self):
#         self.destroy()
#         self.parent.deiconify()


class PostDialog(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.title("Create Post")
        self.geometry("400x200")

        self.username = username
        self.post_content = None

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="What's on your mind?", font=('Arial', 14, 'bold')).pack(pady=10)

        ttk.Label(self, text=f"User: {self.username}", font=('Arial', 12)).pack(pady=5)

        self.post_text = tk.Text(self, width=40, height=4)
        self.post_text.pack(pady=5)

        submit_button = tk.Button(self, text="Post", font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                                  bg='#18941f', cursor='hand2', activebackground='#3047ff', fg='white',
                                  command=self.submit_post)
        submit_button.pack(pady=5)

    def submit_post(self):
        self.post_content = self.post_text.get("1.0", tk.END).strip()
        self.destroy()
