import tkinter as tk
from tkinter import ttk
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def fetch_stock_data(api_key, symbol, interval):
    url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&apikey={api_key}'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('Error fetching data:', response.status_code)
        return None

def arrange_stock_data(stock_data):
    arranged_data = ""
    if stock_data and 'values' in stock_data:
        arranged_data += "Date\t\t\tOpen\n"
        for entry in stock_data['values']:
            arranged_data += f"{entry['datetime']}\t{entry['open']}\n"
    else:
        arranged_data = "Error fetching data. Please try again."
    return arranged_data

def update_stock_data():
    global plot_canvas  # Declare plot_canvas as global
    # Clear previous data label content
    data_label.config(text="")
    
    # Clear previous plot
    if plot_canvas:
        plot_canvas.get_tk_widget().destroy()
    
    api_key = '75d6d4a55a6b40b7a33d778ea2ee3297'  # Replace 'YOUR_API_KEY' with your Twelve Data API key
    symbol = symbol_var.get()
    interval = interval_var.get()
    
    stock_data = fetch_stock_data(api_key, symbol, interval)
    
    arranged_data = arrange_stock_data(stock_data)
    
    # Display arranged data
    data_label.config(text=arranged_data)

def plot_stock_data():
    global plot_canvas
    data_label.config(text="")
    if plot_canvas:
        plot_canvas.get_tk_widget().destroy()
    api_key = '75d6d4a55a6b40b7a33d778ea2ee3297'  
    symbol = symbol_var.get()
    interval = interval_var.get()
    stock_data = fetch_stock_data(api_key, symbol, interval)
    if stock_data and 'values' in stock_data:
        times = [entry['datetime'] for entry in stock_data['values']]
        prices = [entry['open'] for entry in stock_data['values']]
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(times, prices, label='Stock Price', color='lightblue')  # Adjust plot color
        ax.set_title('Stock Price Over Time', color='white')  # Set title color
        ax.set_xlabel('Time', color='white')  # Set x-axis label color
        ax.set_ylabel('Price', color='white')  # Set y-axis label color
        ax.tick_params(axis='x', colors='white')  # Set x-axis tick color
        ax.tick_params(axis='y', colors='white')  # Set y-axis tick color
        ax.spines['top'].set_color('white')  # Set top spine color
        ax.spines['bottom'].set_color('white')  # Set bottom spine color
        ax.spines['left'].set_color('white')  # Set left spine color
        ax.spines['right'].set_color('white')  # Set right spine color
        ax.legend(facecolor='black', edgecolor='white')  # Set legend color
        fig.patch.set_facecolor('#1e1e1e')  # Set figure background color
        ax.set_facecolor('#1e1e1e')  # Set plot background color
        plt.xticks(rotation=45)  # Rotate x-axis tick labels
        plt.tight_layout()
        plot_canvas = FigureCanvasTkAgg(fig, master=root)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)



# Create the GUI window
root = tk.Tk()
root.title("Stock Market App")
root.state('zoomed')


# Set dark theme
root.configure(bg="#1e1e1e")
style = ttk.Style(root)
style.theme_use("clam")
style.configure('TLabel', foreground='white', background='#1e1e1e')
style.configure('TButton', foreground='white', background='#404040')

# Create a label for symbol selection
symbol_label = ttk.Label(root, text="Select Stock Symbol:")
symbol_label.pack(padx=10, pady=10)

# Define stock symbols
symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'FB', 'BABA', 'NVDA', 'NFLX', 'AMD', 'PYPL', 'ADBE', 'INTC', 'CRM', 'CSCO']

# Create a dropdown menu for stock symbols
symbol_var = tk.StringVar(value=symbols[0])
symbol_dropdown = ttk.OptionMenu(root, symbol_var, *symbols)
symbol_dropdown.pack(padx=10, pady=10)

# Create a label for interval selection
interval_label = ttk.Label(root, text="Select Time Interval:")
interval_label.pack(padx=10, pady=10)

# Define time intervals
intervals = ['1min', '5min', '15min', '30min', '60min']

# Create a dropdown menu for time intervals
interval_var = tk.StringVar(value=intervals[0])
interval_dropdown = ttk.OptionMenu(root, interval_var, *intervals)
interval_dropdown.pack(padx=10, pady=10)

# Create a button to fetch and update stock data
update_button = ttk.Button(root, text="Update Data", command=update_stock_data)
update_button.pack(padx=10, pady=10)

# Create a button to plot stock data
plot_button = ttk.Button(root, text="Plot Data", command=plot_stock_data)
plot_button.pack(padx=10, pady=10)

# Create a label to display stock data
data_label = ttk.Label(root, text="", wraplength=400)
data_label.pack(padx=10, pady=10)

# Variable to hold plot canvas
plot_canvas = None

# Run the Tkinter event loop
root.mainloop()
