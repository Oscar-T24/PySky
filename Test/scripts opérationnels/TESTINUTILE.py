import pandas as pd
import tkinter as tk
from tkinter import ttk

# Define function to read CSV file and create table
def create_table(filename):
    # Read CSV file into pandas dataframe
    df = pd.read_csv(filename)
    
    # Create tkinter window
    root = tk.Tk()
    root.title('CSV Table')
    
    # Create treeview widget to display table
    tree = ttk.Treeview(root)
    tree['columns'] = list(df.columns)
    
    # Define column headings
    for col in df.columns:
        tree.heading(col, text=col)
    
    # Add rows to treeview
    for i, row in df.iterrows():
        tree.insert('', 'end', text=str(i), values=list(row))
    
    # Pack treeview into window
    tree.pack(side='left', fill='both', expand=True)
    
    # Run tkinter main loop
    root.mainloop()

import pandas as pd

# Define function to check for non-floating-point values
def check_floats(filename, column):
    # Read CSV file into pandas dataframe
    df = pd.read_csv(filename)
    
    # Check for non-floating-point values in column
    non_float_rows = df[~df[column].astype(str).apply(lambda x: x.replace('.', '', 1).isdigit())]
    
    # Print error message for each non-floating-point row
    for i, row in non_float_rows.iterrows():
        print(f"Error: Non-floating-point value '{row[column]}' in row {i}")
