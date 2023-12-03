import tkinter as tk
from tkinter import ttk, font
from utils.color import Color
from controllers.analysis_controller import AnalysisController
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

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
        
        self.chart_1(tab_view)
        self.chart_2(tab_view)
        self.chart_3(tab_view)
        self.chart_4(tab_view)
        self.chart_5(tab_view)

        tab_view.grid(row=0, column=0, sticky='nsew')
        
    def chart_1(self, tab_view):
        tab = ttk.Frame(tab_view, width=980, height=600) 
        tab_view.add(tab, text='Chart 1')  
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        fig = plt.Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        df = self.controller.get_flights_pd()

        status_counts = df['flight_status'].value_counts()
        ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140)
        ax.axis('equal') 
        ax.set_title('Flight Status Distribution')

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().grid(sticky='nsew')
        
    def chart_2(self, tab_view):
        tab = ttk.Frame(tab_view, width=980, height=600) 
        tab_view.add(tab, text='Chart 2')  
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        fig = plt.Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        df = self.controller.get_flights_pd()
        airline_counts = df['airline'].value_counts()
        airline_counts.plot(kind='bar', ax=ax)

        ax.set_title('Flights per Airline')
        ax.set_xlabel('Airline')
        ax.set_ylabel('Number of Flights')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, horizontalalignment='center')

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().grid(sticky='nsew')
        
    def chart_3(self, tab_view):
        tab = ttk.Frame(tab_view, width=980, height=600) 
        tab_view.add(tab, text='Chart 3')  
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        fig = plt.Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        df = self.controller.get_flights_pd()
        ax.hist(df['price'], bins=20, edgecolor='black')

        ax.set_title('Flight Price Distribution')
        ax.set_xlabel('Price')
        ax.set_ylabel('Number of Flights')

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().grid(sticky='nsew')
        
    def chart_4(self, tab_view):
        tab = ttk.Frame(tab_view, width=980, height=600) 
        tab_view.add(tab, text='Chart 4')  
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        fig = plt.Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        df = self.controller.get_bookings_pd()
        df['booking_time'] = pd.to_datetime(df['booking_time'])

        daily_bookings = df.resample('D', on='booking_time').size()
        daily_bookings.plot(ax=ax)
        ax.set_title('Bookings Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Bookings')

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().grid(sticky='nsew')
        
    def chart_5(self, tab_view):
        tab = ttk.Frame(tab_view, width=980, height=600) 
        tab_view.add(tab, text='Chart 5')  
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        fig = plt.Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        df = self.controller.get_flights_pd()
        destination_counts = df['destination'].value_counts()
        top_destinations = destination_counts[:10]
        fig, ax = plt.subplots()
        top_destinations.plot(kind='bar', ax=ax)
        
        ax.set_title('Top Destinations')
        ax.set_xlabel('Destination')
        ax.set_ylabel('Number of Flights')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, horizontalalignment='center')

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().grid(sticky='nsew')
    
    def start(self):
        self.mainloop()

    def go_back(self):
        self.pack_forget()
        self.back_callback()
        