
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from dbcon import DatabaseConnection  # Ensure dbcon.py provides the correct DatabaseConnection class
from ttkthemes import ThemedTk

class EventGui(ThemedTk):
    def __init__(self, user_id):
        super().__init__(theme="breeze")  # Applying a modern, light theme
        self.user_id = user_id  # Store the passed user ID
        self.title("Event Management")
        self.geometry("1000x700")
        self.configure(bg="#e8eaf6")  # Light background color for a pleasant look

        self.db = DatabaseConnection()
        self.connection = self.db.create_connection()

        self.style = ttk.Style()
        self.configure_style()

        self.create_widgets()
        self.load_events()

    def configure_style(self):
        # General styling for TTK widgets
        self.style.configure('TLabel', background="#e8eaf6", font=('Helvetica', 12), foreground="#333333")
        self.style.configure('TEntry', font=('Helvetica', 12))
        self.style.configure('TCombobox', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12, 'bold'), background="#6200ea", foreground="#ffffff")
        self.style.map('TButton', background=[('active', '#6200ea'), ('!disabled', '#6200ea')], foreground=[('active', '#ffffff')])

        # Styling for the notebook tabs
        self.style.configure('TNotebook.Tab', font=('Helvetica', 12, 'bold'), padding=(10, 5))
        self.style.map('TNotebook.Tab', background=[('selected', '#6200ea')], foreground=[('selected', '#ffffff')])

    def create_widgets(self):
        # Creating a Notebook for tabbed interface
        self.tab_control = ttk.Notebook(self)

        self.create_event_tab = ttk.Frame(self.tab_control, padding=10, style='TFrame')
        self.view_events_tab = ttk.Frame(self.tab_control, padding=10, style='TFrame')
        # Removed view_subscribers_tab initialization

        self.tab_control.add(self.create_event_tab, text='Create Event')
        self.tab_control.add(self.view_events_tab, text='View Events')
        # Removed addition of view_subscribers_tab to the notebook
        self.tab_control.pack(expand=1, fill='both')

        self.create_event_widgets()
        self.view_events_widgets()
        # Removed call to view_subscribers_widgets

    def create_event_widgets(self):
        # Using consistent padding and spacing
        font_style = ('Helvetica', 12)

        ttk.Label(self.create_event_tab, text="Event Name", font=font_style).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.event_name_entry = ttk.Entry(self.create_event_tab, font=font_style)
        self.event_name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.create_event_tab, text="Description", font=font_style).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.description_entry = ttk.Entry(self.create_event_tab, font=font_style)
        self.description_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.create_event_tab, text="Location", font=font_style).grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.location_entry = ttk.Entry(self.create_event_tab, font=font_style)
        self.location_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.create_event_tab, text="Start Time", font=font_style).grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.start_time_entry = DateEntry(self.create_event_tab, font=font_style, date_pattern='yyyy-mm-dd')
        self.start_time_entry.grid(row=3, column=1, padx=10, pady=10)

        ttk.Label(self.create_event_tab, text="Category", font=font_style).grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.category_combobox = ttk.Combobox(self.create_event_tab, font=font_style)
        self.category_combobox.grid(row=4, column=1, padx=10, pady=10)

        self.load_categories()

        create_button = ttk.Button(self.create_event_tab, text="Create Event", command=self.create_event)
        create_button.grid(row=5, column=0, columnspan=2, pady=10)

    def load_categories(self):
        connection = self.db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT EventCategoryID, CategoryName FROM EventCategories")
        categories = cursor.fetchall()
        cursor.close()
        connection.close()

        self.category_combobox['values'] = [f"{category[1]} (ID: {category[0]})" for category in categories]

    def create_event(self):
        event_name = self.event_name_entry.get()
        description = self.description_entry.get()
        location = self.location_entry.get()
        start_time = self.start_time_entry.get_date().strftime("%Y-%m-%d")
        category = self.category_combobox.get()

        if not event_name or not description or not location or not start_time or not category:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            category_id = int(category.split("(ID: ")[1].rstrip(')'))
        except (IndexError, ValueError):
            messagebox.showerror("Error", "Invalid category selected")
            return

        connection = self.db.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("{CALL CreateEvent(?, ?, ?, ?, ?, ?)}",
                           (event_name, description, location, start_time, self.user_id, category_id))  # Use the provided user ID
            connection.commit()
            messagebox.showinfo("Success", "Event created successfully")
            self.load_events()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create event: {e}")
        finally:
            cursor.close()
            connection.close()

    def view_events_widgets(self):
        # Frame for the event cards
        self.event_card_container = ttk.Frame(self.view_events_tab, style='TFrame')
        self.event_card_container.pack(fill=tk.BOTH, expand=True)

        # Scrollbar for the events list
        self.event_scrollbar = ttk.Scrollbar(self.event_card_container)
        self.event_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas for events with scrollbar
        self.event_canvas = tk.Canvas(self.event_card_container, yscrollcommand=self.event_scrollbar.set, bg="#f0f2f5")
        self.event_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.event_scrollbar.config(command=self.event_canvas.yview)

        # Frame to hold event cards
        self.cards_frame = ttk.Frame(self.event_canvas, style='TFrame')
        self.cards_frame.bind(
            "<Configure>",
            lambda e: self.event_canvas.configure(scrollregion=self.event_canvas.bbox("all"))
        )
        self.event_canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")

    def load_events(self):
        # Clear the current list of events
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        connection = self.db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT EventID, EventName, Description, Location, StartTime, CategoryName, SubscriberCount FROM GetAllEvents")
        events = cursor.fetchall()
        cursor.close()
        connection.close()

        for event in events:
            self.create_event_card(event)

    def create_event_card(self, event):
        # Create a card for each event with a shadow effect
        card = ttk.Frame(self.cards_frame, padding=10, relief="groove", style='TFrame')
        card.pack(pady=10, padx=10, fill=tk.X)

        # Detailed event information on each card
        ttk.Label(card, text=f"Event Name: {event[1]}", font=('Helvetica', 14, 'bold')).pack(anchor='w')
        ttk.Label(card, text=f"Description: {event[2]}", font=('Helvetica', 12)).pack(anchor='w')
        ttk.Label(card, text=f"Location: {event[3]}", font=('Helvetica', 12)).pack(anchor='w')
        ttk.Label(card, text=f"Start Time: {event[4]}", font=('Helvetica', 12)).pack(anchor='w')
        ttk.Label(card, text=f"Category: {event[5]}", font=('Helvetica', 12)).pack(anchor='w')
        ttk.Label(card, text=f"Subscribers: {event[6]}", font=('Helvetica', 12)).pack(anchor='w')

        # Subscribe and Delete buttons for each event
        action_frame = ttk.Frame(card)
        action_frame.pack(anchor='w', pady=5)

        subscribe_button = ttk.Button(action_frame, text="Subscribe", command=lambda event_id=event[0]: self.subscribe_to_event(event_id))
        subscribe_button.pack(side=tk.LEFT, padx=5)

        # delete_button = ttk.Button(action_frame, text="Delete Event", command=lambda event_id=event[0]: self.delete_event(event_id))
        # delete_button.pack(side=tk.LEFT, padx=5)

        # Moved view_subscribers_button to here since view_subscribers_tab is removed
        view_subscribers_button = ttk.Button(action_frame, text="View Subscribers", command=lambda event_id=event[0]: self.show_subscriber_dialog(event_id))
        view_subscribers_button.pack(side=tk.LEFT, padx=5)

    def subscribe_to_event(self, event_id):
        connection = self.db.create_connection()
        cursor = connection.cursor()

        try:
            # Check if the user is already subscribed
            cursor.execute("SELECT COUNT(*) FROM EventSubscribers WHERE EventID = ? AND UserID = ?", (event_id, self.user_id))
            already_subscribed = cursor.fetchone()[0]

            if (already_subscribed):
                messagebox.showinfo("Info", "You are already subscribed to this event.")
                return

            cursor.execute("{CALL SubscribeToEvent(?, ?)}", (event_id, self.user_id))
            connection.commit()
            messagebox.showinfo("Success", "Subscribed successfully")
            self.load_events()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to subscribe: {e}")
        finally:
            cursor.close()
            connection.close()

    # def delete_event(self, event_id):
    #     connection = self.db.create_connection()
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute("{CALL DeleteEvent(?)}", (event_id,))
    #         connection.commit()
    #         messagebox.showinfo("Success", "Event deleted successfully")
    #         self.load_events()
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Failed to delete event: {e}")
    #     finally:
    #         cursor.close()
    #         connection.close()

    # Removed view_subscribers_widgets definition

    def show_subscriber_dialog(self, event_id):
        connection = self.db.create_connection()
        cursor = connection.cursor()

        query = """
        SELECT
            U.Username,
            U.Email
        FROM
            EventSubscribers ES
            JOIN [User] U ON ES.UserID = U.UserID
        WHERE
            ES.EventID = ?
        """

        cursor.execute(query, (event_id,))
        subscribers = cursor.fetchall()
        cursor.close()
        connection.close()

        if not subscribers:
            messagebox.showinfo("Info", "No subscribers for this event.")
            return

        subscribers_info = "\n".join([f"Username: {username}, Email: {email}" for username, email in subscribers])
        messagebox.showinfo("Subscribers", f"Subscribers for Event ID {event_id}:\n\n{subscribers_info}")

