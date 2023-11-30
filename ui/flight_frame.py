import tkinter as tk
from tkinter import ttk
from controllers.fightController import FlightController
from models.flight import Flight

class FlightWindow(tk.Frame):
    
    def __init__(self, back_callback, parent=None):
        tk.Frame.__init__(self, parent)
        self.back_callback = back_callback
        self.controller = FlightController()
        
        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=0, sticky='ew')

        # Add buttons to the button frame
        back_button = tk.Button(button_frame, text="Back", command=self.go_back)
        back_button.pack(side=tk.LEFT)

        add_button = tk.Button(button_frame, text="Add flight", command=self.add_new_flight)
        add_button.pack(side=tk.LEFT)
        
        edit_button = tk.Button(button_frame, text="Edit flight", command=self.edit)
        edit_button.pack(side=tk.LEFT)
        
        delete_button = tk.Button(button_frame, text="Delete flight")
        delete_button.pack(side=tk.LEFT)

        # Create a frame for the Treeview
        tree_frame = tk.Frame(self)
        tree_frame.grid(row=1, column=0, sticky='nsew')

        # Make the Treeview frame expandable
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add a Treeview to the Treeview frame
        self.tree = ttk.Treeview(tree_frame)
        self.tree["columns"] = ("One", "Two")
        self.tree.heading("One", text="Column 1")
        self.tree.heading("Two", text="Column 2")

        # for i in range(100):  # Add more items to make the scrollbar necessary
        #     tree.insert("", "end", text="Item %s" % i, values=("Value %s" % i, "Value %s" % (i+1)))

        # Add a Scrollbar to the frame
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Treeview to use the Scrollbar
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(fill=tk.BOTH, expand=True)
        
    def insert_to_table(self):
        for i in range(5): 
            self.tree.insert("", "end", text="Item %s" % i, values=("Value %s" % i, "Value %s" % (i+1)))
            
    def add_new_flight(self):
        self.controller.add_flight(Flight('VN202', 'Hanoi', 'Ho Chi Minh City', '2023-12-01 06:00', '2023-12-01 08:00', 200, 50))
        
    def edit(self):
        self.controller.delete_flight(Flight('VN202', 'Ho Chi Minh City', 'Da Nang', '2023-12-01 09:00', '2023-12-01 10:30', 150, 30))

    def start(self):
        self.mainloop()

    def go_back(self):
        self.pack_forget()
        self.back_callback()