import tkinter as tk
from tkinter import ttk, font
from utils.color import Color
from controllers.analysis_controller import AnalysisController
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class AnalysisWindow(tk.Frame):
    
    def __init__(self, back_callback, parent=None):
        tk.Frame.__init__(self, parent)
        self.controller = AnalysisController()
        self.back_callback = back_callback
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
        
        back_button = custom_button(button_frame, text="Back", command=self.go_back)
        back_button.pack(side=tk.LEFT, padx=10)
        
        chart_frame = tk.Frame(self)
        chart_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        chart_frame.columnconfigure(0, weight=1)
        chart_frame.rowconfigure(0, weight=1)

        tab_view = ttk.Notebook(chart_frame)
        
        flights_df = self.controller.get_flights_pd()
        booking_df = self.controller.get_bookings_pd()
        
        flight_status_fig = plt.Figure(figsize=(10, 6))
        ax = flight_status_fig.add_subplot(111)
        status_counts = flights_df['flight_status'].value_counts()
        ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140)
        ax.axis('equal') 
        ax.set_title('Flight Status Distribution')
        self.chart('Flight Status Distribution', tab_view, flight_status_fig)
        
        flights_per_airline_fig = plt.Figure(figsize=(10, 6))
        ax = flights_per_airline_fig.add_subplot(111)
        airline_counts = flights_df['airline'].value_counts()
        airline_counts.plot(kind='bar', ax=ax)
        ax.set_title('Flights per Airline')
        ax.set_xlabel('Airline')
        ax.set_ylabel('Number of Flights')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, horizontalalignment='center')
        self.chart('Flights per Airline', tab_view, flights_per_airline_fig)
        
        flight_price_distribution_fig = plt.Figure(figsize=(10, 6))
        ax = flight_price_distribution_fig.add_subplot(111)
        ax.hist(flights_df['price'], bins=20, edgecolor='black')
        ax.set_title('Flight Price Distribution')
        ax.set_xlabel('Price')
        ax.set_ylabel('Number of Flights')
        self.chart('Flight Price Distribution', tab_view, flight_price_distribution_fig)
        
        bookings_over_time_fig = plt.Figure(figsize=(10, 6))
        ax = bookings_over_time_fig.add_subplot(111)
        booking_df['booking_time'] = pd.to_datetime(booking_df['booking_time'])
        daily_bookings = booking_df.resample('D', on='booking_time').size()
        daily_bookings.plot(ax=ax)
        ax.set_title('Bookings Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Bookings')
        self.chart('Bookings Over Time', tab_view, bookings_over_time_fig)
        
        top_destinations_fig = plt.Figure(figsize=(10, 6))
        ax = top_destinations_fig.add_subplot(111)
        destination_counts = flights_df['destination'].value_counts()
        top_destinations = destination_counts[:10]
        top_destinations.plot(kind='bar', ax=ax)
        ax.set_title('Top Destinations')
        ax.set_xlabel('Destination')
        ax.set_ylabel('Number of Flights')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, horizontalalignment='center')
        self.chart('Top Destinations', tab_view, top_destinations_fig)

        tab_view.grid(row=0, column=0, sticky='nsew')
        
    def chart(self, title, tab_view, fig):
        tab = ttk.Frame(tab_view, width=980, height=600) 
        tab_view.add(tab, text=title)  
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        canvas = FigureCanvasTkAgg(fig, master=tab)
        tool_bar = NavigationToolbar2Tk(canvas, tab, pack_toolbar=False)
        tool_bar.grid(sticky='new')
        canvas.draw()
        canvas.get_tk_widget().grid(sticky='nsew')
    
    def start(self):
        self.mainloop()

    def go_back(self):
        self.pack_forget()
        self.back_callback()
        