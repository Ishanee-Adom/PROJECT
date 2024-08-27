import database
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog, colorchooser
from PIL import Image, ImageTk
import json
import time
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry
import sqlite3

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Splash Screen")
        self.root.geometry("600x400")
        self.root.configure(bg="blue")

        # Load and display car image
        car_image_path = "other.png"

        try:
            image = Image.open(car_image_path)
            image = image.resize((300, 200), Image.LANCZOS)
            self.car_photo = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.car_photo = None

        self.create_widgets()

        # Show the splash screen for 3 seconds, then move to the login window
        self.root.after(3000, self.show_login_window)

    def create_widgets(self):
        canvas = tk.Canvas(self.root, bg='light blue', width=800, height=500)
        canvas.pack()

        if self.car_photo:
            canvas.create_oval(250, 100, 450, 300, fill="white", outline="white")
            canvas.create_image(300, 200, image=self.car_photo)

        splash_label = tk.Label(self.root, text="Welcome to AREJIJ Car Rentals", font=("Helvetica", 24), bg="white", fg="black")
        splash_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def show_login_window(self):
        self.root.destroy()  # Close splash screen
        LoginWindow()  # Open login window


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AREJIJ CAR RENTAL MANAGEMENT SYSTEM")
        self.geometry("800x400")
        self.configure(bg="light blue")

        # Load and display image
        self.load_image()

        # Login frame
        login_frame = tk.Frame(self, bg="white")
        login_frame.place(x=400, y=50, width=380, height=300)

        # Title
        tk.Label(login_frame, text="AREJIJ CAR RENTAL SYSTEM", font=("Arial", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=3, pady=10)

        # Username label and entry
        tk.Label(login_frame, text="Username", font=("Arial", 12), bg="white").grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12))
        self.username_entry.grid(row=1, column=1, pady=10, padx=10)

        # Password label and entry
        tk.Label(login_frame, text="Password", font=("Arial", 12), bg="white").grid(row=2, column=0, pady=10, padx=10, sticky="w")
        self.password_entry = tk.Entry(login_frame, font=("Arial", 12), show="*")
        self.password_entry.grid(row=2, column=1, pady=10, padx=10)

        # Login button
        login_button = tk.Button(login_frame, text="LOGIN", font=("Arial", 12, "bold"), bg="yellow", fg="black", command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=20)

    def load_image(self):
        image_frame = tk.Frame(self, bg="white")
        image_frame.place(x=50, y=50, width=300, height=300)

        image_path = "login.png"  # Adjust the path as necessary
        load = Image.open(image_path)
        render = ImageTk.PhotoImage(load)

        img = tk.Label(image_frame, image=render, bg="white")
        img.image = render
        img.place(x=0, y=0)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "password":  # Example validation
            messagebox.showinfo("Login", "Login successful!")
            self.destroy()  # Close the login window
            CarRentalSystem()  # Open the main application window
        else:
            messagebox.showerror("Login", "Invalid username or password")


class CarRentalSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AREJIJ CAR RENTAL MANAGEMENT SYSTEM")
        self.geometry("1024x768")
        self.configure(bg="#f0f0f0")

        # Initialize database
        database.create_customer_table()

        # Sidebar menu
        self.create_sidebar()

        # Main content area
        self.main_frame = tk.Frame(self, bg="#f0f0f0")
        self.main_frame.place(x=150, y=50, width=850, height=700)

        # Top bar for logout and rent buttons
        self.top_bar = tk.Frame(self, bg="#f0f0f0")
        self.top_bar.place(x=150, y=10, width=850, height=40)

        # Log out button
        self.logout_button = tk.Button(self.top_bar, text="Log Out", command=self.logout, bg="#ff5252", fg="white", font=("Arial", 12, "bold"))
        self.logout_button.pack(side=tk.RIGHT, padx=10)

        # Rent This Car button (initially hidden)
        self.rent_button = tk.Button(self.top_bar, text="Rent This Car", command=self.open_rental_form, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))

        # Initialize total revenue
        self.total_revenue = 0

        # Show dashboard immediately after login
        self.show_dashboard()

        self.mainloop()

    def create_sidebar(self):
        sidebar = tk.Frame(self, bg="orange")
        sidebar.place(x=0, y=0, width=150, height=400)

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Manage Cars", self.manage_cars),
            ("Manage Customers", self.manage_customers),
            ("View All Cars", self.view_all_cars),
            ("Exit", self.exit_system)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(sidebar, text=text, command=command, bg="orange", fg="white", font=("Arial", 12, "bold"))
            btn.place(x=10, y=50*i+20, width=130, height=40)

    def show_dashboard(self):
        self.clear_main_frame()
        
        # Title
        title_label = tk.Label(self.main_frame, text="Dashboard", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333333")
        title_label.pack(pady=(20, 30))

        # Create a frame for the dashboard widgets
        dashboard_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Define some sample data (replace with actual data in a real application)
        total_cars = 5
        available_cars = 5
        rented_cars = 0
        total_customers = 4

        # Create dashboard widgets
        self.create_info_card(dashboard_frame, "Total Cars", total_cars, "#4caf50", 0, 0)
        self.create_info_card(dashboard_frame, "Available Cars", available_cars, "#2196f3", 0, 1)
        self.create_info_card(dashboard_frame, "Rented Cars", rented_cars, "#ff9800", 1, 0)
        self.create_info_card(dashboard_frame, "Total Customers", total_customers, "#9c27b0", 1, 1)

        # Revenue card
        revenue_frame = tk.Frame(dashboard_frame, bg="white", relief=tk.RAISED, borderwidth=1)
        revenue_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        tk.Label(revenue_frame, text="Total Revenue", font=("Arial", 16, "bold"), bg="white", fg="#333333").pack(pady=(15, 5))
        self.revenue_label = tk.Label(revenue_frame, text=f"${self.total_revenue:,.2f}", font=("Arial", 24, "bold"), bg="white", fg="#4caf50")
        self.revenue_label.pack(pady=(5, 15))

        # Recent rentals
        rentals_frame = tk.Frame(dashboard_frame, bg="white", relief=tk.RAISED, borderwidth=1)
        rentals_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        tk.Label(rentals_frame, text="Recent Rentals", font=("Arial", 16, "bold"), bg="white", fg="#333333").pack(pady=(15, 5))
        
        # Sample rental data (replace with actual data)
        rentals = [
            ("John Doe", "Toyota Camry", "2023-05-01"),
            ("Jane Smith", "Honda Civic", "2023-05-02"),
            ("Bob Johnson", "Ford Mustang", "2023-05-03")
        ]
        
        for rental in rentals:
            tk.Label(rentals_frame, text=f"{rental[0]} - {rental[1]} ({rental[2]})", font=("Arial", 12), bg="white", fg="#666666").pack(pady=2)

        # Configure grid
        dashboard_frame.grid_columnconfigure(0, weight=1)
        dashboard_frame.grid_columnconfigure(1, weight=1)
        for i in range(4):
            dashboard_frame.grid_rowconfigure(i, weight=1)

    def create_info_card(self, parent, title, value, color, row, column):
        frame = tk.Frame(parent, bg="white", relief=tk.RAISED, borderwidth=1)
        frame.grid(row=row, column=column, sticky="nsew", padx=10, pady=10)
        
        tk.Label(frame, text=title, font=("Arial", 14, "bold"), bg="white", fg="#333333").pack(pady=(15, 5))
        tk.Label(frame, text=str(value), font=("Arial", 24, "bold"), bg="white", fg=color).pack(pady=(5, 15))

    def manage_cars(self):
        self.clear_main_frame()
        
        # Create a frame for the manage cars content
        manage_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        manage_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(manage_frame, text="Manage Cars", font=("Helvetica", 24), bg="#f0f0f0", fg="#333333")
        title_label.pack(pady=(0, 20))

        # Create a frame for buttons
        button_frame = tk.Frame(manage_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=10)

        # Style for buttons
        button_style = {"font": ("Helvetica", 12), "bg": "#4CAF50", "fg": "white", "padx": 15, "pady": 10, "bd": 0}

        # Interactive buttons
        add_btn = tk.Button(button_frame, text="Add New Car", command=self.add_new_car, **button_style)
        delete_btn = tk.Button(button_frame, text="Delete Selected Car", command=self.delete_car, **button_style)

        add_btn.pack(side=tk.LEFT, padx=(0, 10))
        delete_btn.pack(side=tk.LEFT)  # Added delete button

        # Create a frame for the car list
        list_frame = tk.Frame(manage_frame, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Create a treeview for the car list
        columns = ("ID", "Make", "Model", "Year", "Price", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode='browse')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Load cars from JSON file
        self.load_cars()

        # Add scrollbar to the treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_cars(self):
        try:
            with open('cars.json', 'r') as f:
                cars = json.load(f)
        except FileNotFoundError:
            cars = []

        # Clear existing entries in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add cars to the treeview
        for i, car in enumerate(cars, start=1):
            # Set a default status if not present
            status = car.get('status', 'Available')  # Default status
            self.tree.insert("", tk.END, values=(i, car['make'], car['model'], car['year'], f"${car['price']:,.2f}", status))

    def delete_car(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Delete Car", "Please select a car to delete.")
            return

        # Get the selected car's index
        selected_index = self.tree.index(selected_item[0])

        # Load existing cars
        try:
            with open('cars.json', 'r') as f:
                cars = json.load(f)
        except FileNotFoundError:
            cars = []

        # Remove the selected car
        del cars[selected_index]

        # Save the updated car list back to the JSON file
        with open('cars.json', 'w') as f:
            json.dump(cars, f, indent=2)

        messagebox.showinfo("Success", "Car deleted successfully.")
        self.load_cars()  # Refresh the car list

    def add_new_car(self):
        # Dialog for adding a new car
        car_info = simpledialog.askstring("New Car", "Enter car details (Make,Model,Year,Price):")
        if car_info:
            make, model, year, price = car_info.split(',')
            new_car = {
                "make": make.strip(),
                "model": model.strip(),
                "year": int(year.strip()),
                "price": float(price.strip()),
                "status": "Available",
                "image_path": "default_car_image.png",  # You should have a default image
                "description": "New car added to the fleet.",
                "performance": "Standard performance."
            }
            
            # Load existing cars
            try:
                with open('cars.json', 'r') as f:
                    cars = json.load(f)
            except FileNotFoundError:
                cars = []
            
            # Add new car and save
            cars.append(new_car)
            with open('cars.json', 'w') as f:
                json.dump(cars, f, indent=2)
            
            messagebox.showinfo("Success", f"Added new car: {make} {model}")
            self.load_cars()  # Refresh the car list

    def manage_customers(self):
        self.clear_main_frame()
        
        # Create a notebook for different customer management tabs
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Add Customer Tab
        add_frame = ttk.Frame(notebook)
        notebook.add(add_frame, text="Add Customer")
        self.create_add_customer_form(add_frame)

        # View Customers Tab
        self.view_frame = ttk.Frame(notebook)
        notebook.add(self.view_frame, text="View Customers")
        self.create_customer_tree(self.view_frame)

        # Customer Stats Tab
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Customer Stats")
        self.create_customer_stats(stats_frame)

    def create_add_customer_form(self, parent):
        # Stylish form for adding customers
        style = ttk.Style()
        style.configure("TEntry", padding=5)
        style.configure("TButton", padding=5, font=("Arial", 12))

        form_frame = ttk.Frame(parent, padding="20 20 20 20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Add New Customer", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        fields = [("Name", "name"), ("Contact No", "contact"), ("Driving License", "license"), ("Address", "address")]
        self.customer_entries = {}

        for i, (label, field) in enumerate(fields, start=1):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            self.customer_entries[field] = entry

        # Date of Birth field with calendar widget
        ttk.Label(form_frame, text="Date of Birth").grid(row=len(fields)+1, column=0, sticky="e", padx=5, pady=5)
        self.dob_entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.dob_entry.grid(row=len(fields)+1, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(form_frame, text="Add Customer", command=self.add_customer).grid(row=len(fields)+2, column=0, columnspan=2, pady=20)

    def create_customer_tree(self, parent):
        # Create a treeview to display customers
        columns = ("ID", "Name", "Contact", "License", "Address", "DOB")
        tree = ttk.Treeview(parent, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Add some sample data (replace with actual data in a real application)
        sample_data = [
            (1, "John Doe", "1234567890", "DL12345", "123 Main St", "1990-01-01"),
            (2, "Jane Smith", "9876543210", "DL67890", "456 Elm St", "1985-05-15"),
        ]

        for item in sample_data:
            tree.insert("", tk.END, values=item)

    def create_customer_stats(self, parent):
        # Create a simple bar chart of customer age groups
        fig, ax = plt.subplots(figsize=(6, 4))
        age_groups = ['18-25', '26-35', '36-45', '46-55', '56+']
        customers = [15, 30, 25, 18, 12]  # Sample data
        ax.bar(age_groups, customers)
        ax.set_ylabel('Number of Customers')
        ax.set_title('Customer Age Distribution')

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

    def add_customer(self):
        # Get values from entries
        customer_data = {field: entry.get() for field, entry in self.customer_entries.items()}
        customer_data['dob'] = self.dob_entry.get_date().strftime("%Y-%m-%d")

        # Here you would typically save this data to your database
        print("Adding customer:", customer_data)
        messagebox.showinfo("Success", f"Added new customer: {customer_data['name']}")

        # Clear the form
        for entry in self.customer_entries.values():
            entry.delete(0, tk.END)
        self.dob_entry.set_date(None)

        # Update the customer tree
        self.update_customer_tree()

    def update_customer_tree(self):
        # Clear the existing tree
        for item in self.view_frame.winfo_children():
            item.destroy()

        # Create a new treeview to display customers
        columns = ("ID", "Name", "Contact", "License", "Address", "DOB")
        tree = ttk.Treeview(self.view_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Add some sample data (replace with actual data in a real application)
        sample_data = [
            (1, "John Doe", "1234567890", "DL12345", "123 Main St", "1990-01-01"),
            (2, "Jane Smith", "9876543210", "DL67890", "456 Elm St", "1985-05-15"),
        ]

        for item in sample_data:
            tree.insert("", tk.END, values=item)

    def view_all_cars(self):
        self.clear_main_frame()
        
        # Create a frame for the car display that fills most of the main frame
        car_frame = ttk.Frame(self.main_frame)
        car_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Create the CarDisplay inside this frame
        self.car_display = CarDisplay(car_frame, self)

        # Show the Rent This Car button
        self.rent_button.pack(side=tk.RIGHT, padx=10)

    def open_rental_form(self):
        if hasattr(self, 'car_display') and self.car_display.cars:
            car = self.car_display.cars[self.car_display.current_car_index]
            RentalForm(self, car)

    def exit_system(self):
        self.destroy()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Hide the Rent This Car button when clearing the main frame
        self.rent_button.pack_forget()

    def logout(self):
        self.destroy()
        LoginWindow()  # Return to the login window

    def update_revenue(self, amount):
        self.total_revenue += amount
        if hasattr(self, 'revenue_label'):
            self.revenue_label.config(text=f"${self.total_revenue:,.2f}")


class CarDisplay:
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent
        self.cars = []
        self.current_car_index = 0
        self.load_cars()

        # Frame for image
        self.image_frame = tk.Frame(master, width=400, height=300)
        self.image_frame.pack(side=tk.LEFT, padx=20, pady=20)
        self.image_frame.pack_propagate(False)

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # Frame for specs
        self.specs_frame = ttk.Frame(master)
        self.specs_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Use Text widgets with scrollbars for better text display
        self.description_text = self.create_scrollable_text(self.specs_frame, height=5, width=50)
        self.description_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.performance_text = self.create_scrollable_text(self.specs_frame, height=5, width=50)
        self.performance_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.price_text = self.create_scrollable_text(self.specs_frame, height=2, width=50)
        self.price_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Navigation buttons
        self.button_frame = ttk.Frame(master)
        self.button_frame.pack(side=tk.BOTTOM, pady=20, fill=tk.X)

        ttk.Button(self.button_frame, text="Previous", command=self.show_previous_car).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Next", command=self.show_next_car).pack(side=tk.LEFT, padx=5)

        self.show_current_car()

        # Start the automatic sliding
        self.slide_timer = self.master.after(10000, self.auto_slide)

    def create_scrollable_text(self, parent, height, width):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True)
        
        text = tk.Text(frame, height=height, width=width, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return text

    def load_cars(self):
        try:
            with open('cars.json', 'r') as f:
                self.cars = json.load(f)
        except FileNotFoundError:
            self.cars = []

    def show_current_car(self):
        if not self.cars:
            return

        car = self.cars[self.current_car_index]
        
        # Load and display image
        image = Image.open(car['image_path'])
        image = image.resize((400, 300), Image.LANCZOS)
        self.current_photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.current_photo)

        # Display specs
        self.description_text.delete('1.0', tk.END)
        self.description_text.insert(tk.END, f"Description:\n{car['description']}")

        self.performance_text.delete('1.0', tk.END)
        self.performance_text.insert(tk.END, f"Performance:\n{car['performance']}")

        self.price_text.delete('1.0', tk.END)
        self.price_text.insert(tk.END, f"Price: ${car['price']:,.2f}")
 
    def show_next_car(self):
        if self.cars:
            self.current_car_index = (self.current_car_index + 1) % len(self.cars)
            self.slide_to_next()

    def show_previous_car(self):
        if self.cars:
            self.current_car_index = (self.current_car_index - 1) % len(self.cars)
            self.slide_to_previous()

    def slide_to_next(self):
        # Cancel any existing timer
        if hasattr(self, 'slide_timer'):
            self.master.after_cancel(self.slide_timer)

        # Slide current image out to the left
        for i in range(40):
            self.image_label.place(x=-i*10, y=0)
            self.master.update()
            time.sleep(0.01)

        self.show_current_car()
        self.image_label.place(x=0, y=0)

        # Restart the timer
        self.slide_timer = self.master.after(10000, self.auto_slide)

    def slide_to_previous(self):
        # Cancel any existing timer
        if hasattr(self, 'slide_timer'):
            self.master.after_cancel(self.slide_timer)

        # Slide current image out to the right
        for i in range(40):
            self.image_label.place(x=i*10, y=0)
            self.master.update()
            time.sleep(0.01)

        self.show_current_car()
        self.image_label.place(x=0, y=0)

        # Restart the timer
        self.slide_timer = self.master.after(10000, self.auto_slide)

    def auto_slide(self):
        self.show_next_car()


class RentalForm(tk.Toplevel):
    def __init__(self, master, car):
        super().__init__(master)
        self.car = car
        self.title("Rent a Car")
        self.geometry("400x400")
        self.configure(bg="#f0f0f0")

        # Car details
        make = self.car.get('make', 'Unknown Make')
        model = self.car.get('model', 'Unknown Model')
        price = self.car.get('price', 0.0)

        tk.Label(self, text=f"Rent {make} {model}", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        tk.Label(self, text=f"Price per day: ${price:.2f}", font=("Arial", 12), bg="#f0f0f0").pack()

        # Create a frame for the form
        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=20, padx=20, fill='both', expand=True)

        # Customer details
        tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky='w', pady=5)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Driver's License:").grid(row=1, column=0, sticky='w', pady=5)
        self.drivers_license_entry = tk.Entry(form_frame)
        self.drivers_license_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky='w', pady=5)
        self.email_entry = tk.Entry(form_frame)
        self.email_entry.grid(row=2, column=1, pady=5)

        # Checkbox for agreement
        self.agree_var = tk.BooleanVar()
        self.agree_check = tk.Checkbutton(self, text="I agree to pay the amount", variable=self.agree_var)
        self.agree_check.pack(pady=10)

        # Confirm button
        tk.Button(self, text="Submit", command=self.submit_rental).pack(pady=20)

    def submit_rental(self):
        name = self.name_entry.get()
        drivers_license = self.drivers_license_entry.get()
        email = self.email_entry.get()

        if not self.agree_var.get():
            messagebox.showerror("Error", "You must agree to pay the amount.")
            return

        if not name or not drivers_license or not email:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        # Save rental details to SQLite database
        self.save_rental_to_db(name, drivers_license, email)

        messagebox.showinfo("Success", "Rental information saved successfully.")
        self.destroy()  # Close the form

    def save_rental_to_db(self, name, drivers_license, email):
        # Connect to SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect('rentals.db')
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rentals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                drivers_license TEXT,
                email TEXT,
                car_make TEXT,
                car_model TEXT,
                price REAL
            )
        ''')

        # Insert rental data
        cursor.execute('''
            INSERT INTO rentals (name, drivers_license, email, car_make, car_model, price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, drivers_license, email, self.car['make'], self.car['model'], self.car['price']))

        # Commit changes and close the connection
        conn.commit()
        conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    splash_screen = SplashScreen(root)
    root.mainloop()