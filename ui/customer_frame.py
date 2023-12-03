import tkinter as tk
from tkinter import ttk, messagebox, font
from controllers.customer_controller import CustomerController
from utils.color import Color
from models.customer import Customer
from utils.result import Result

class CustomerWindow(tk.Frame):
    
    def __init__(self, back_callback, parent=None):
        tk.Frame.__init__(self, parent)
        self.back_callback = back_callback
        self.controller = CustomerController()
        self.setup_ui()
        
    def setup_ui(self):
        self["bg"] = Color.PRIMARY.value
        button_frame = tk.Frame(self)
        spacer = tk.Label(button_frame, height=1)  
        spacer["bg"] = Color.PRIMARY.value
        spacer.pack()
        button_frame.grid(row=0, column=0, sticky='ew')
        button_frame["bg"] = Color.PRIMARY.value
        
        def custom_button(root, text, command) -> tk.Button:
            button = tk.Button(root, text=text, command=command)
            button["font"] = font.Font(size=12)
            button["bg"] = Color.WHITE.value
            button["fg"] = Color.PRIMARY.value
            button["activebackground"] = Color.WHITE.value
            button["activeforeground"] = Color.PRIMARY.value
            return button

        # Add buttons to the button frame
        back_button = custom_button(button_frame, text="Back", command=self.go_back)
        back_button.pack(side=tk.LEFT, padx=10)

        add_button = custom_button(button_frame, text="Add customer", command=self.create_or_edit_customer)
        add_button.pack(side=tk.LEFT)
        
        edit_button = custom_button(button_frame, text="Edit customer", command=self.edit)
        edit_button.pack(side=tk.LEFT, padx=10)
        
        delete_button = custom_button(button_frame, text="Delete customer", command=self.delete)
        delete_button.pack(side=tk.LEFT)

        # Create a frame for the Treeview
        tree_frame = tk.Frame(self)
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # Make the Treeview frame expandable
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add a Treeview to the Treeview frame
        self.tree = ttk.Treeview(tree_frame, columns=('Customer ID', 'Name', 'Phone', 'Email'), show='headings')
        self.tree.tag_configure("evenrow", background=Color.FOUR.value) 
        self.tree.tag_configure("oddrow", background=Color.WHITE.value) 

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Add a Scrollbar to the frame
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbarX = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        scrollbarX.pack(side=tk.BOTTOM, fill=tk.X)

        # Configure the Treeview to use the Scrollbar
        self.tree.configure(yscrollcommand=scrollbar.set, xscrollcommand=scrollbarX.set)
        
        self.load_data_from_file()

        self.tree.pack(fill=tk.BOTH, expand=True)
        
    def load_data_from_file(self):
        data = self.controller.read_customers()
        for i in self.tree.get_children():
            self.tree.delete(i)
        for customer in data:
            self.tree.insert("", "end", values=(customer.customer_id, customer.name, customer.phone, customer.email))
        for i, item in enumerate(self.tree.get_children()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.item(item, tags=(tag,))
        
    def create_or_edit_customer(self, customer=None):
        # Create a new window
        window = tk.Toplevel()
        window["bg"] = Color.PRIMARY.value
        # Create labels and entry fields for each attribute of the Flight class
        labels = ['Customer ID', 'Name', 'Phone', 'Email']
        entries = []
        for label in labels:
            row = tk.Frame(window)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            tk.Label(row, width=15, text=label, anchor='w').pack(side=tk.LEFT)
            entry = tk.Entry(row)
            if customer is not None:
                entry.insert(0, getattr(customer, label.replace(' ', '_').lower()))
            entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries.append(entry)

        # Create a button that creates the Flight object and appends it to the CSV file
        def submit():
            customer_id, name, phone, email = [entry.get() for entry in entries]
            new_customer = Customer(customer_id, name, phone, email)
            if customer is None:
                self.handle_state(self.controller.append_customer(new_customer))
            else:
                self.handle_state(self.controller.edit_customer(new_customer))
            self.load_data_from_file()
            window.destroy()

        tk.Button(window, text='Submit', command=submit).pack(side=tk.LEFT, padx=5, pady=5)
        
    def edit(self):
        selected_row = self.tree.selection()
        item_values = self.tree.item(selected_row, 'values')
        
        if len(item_values) == 0:
            return
        customer_id, name, phone, email = item_values
        customer = Customer(customer_id, name, phone, email)
        self.create_or_edit_customer(customer)
    
    def delete(self):
        selected_row = self.tree.selection()
        item_values = self.tree.item(selected_row, 'values')
        
        if len(item_values) == 0:
            return
        result = messagebox.askquestion("Delete", "Are you sure you want to delete this item?", icon='warning')
        # Check the result
        if result == 'yes':
            self.handle_state(self.controller.remove_customer(item_values[0]))
            self.load_data_from_file()
            
    def handle_state(self, result: Result):
        if not(result.is_success()):
            messagebox.showerror("Error", result.error)

    def start(self):
        self.mainloop()

    def go_back(self):
        self.pack_forget()
        self.back_callback()