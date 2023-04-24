import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import csv

# Function to open file dialog and select an image file
def select_image_file():
    image_file = askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    return image_file

# Function to save image filename and corresponding weather to CSV file
def save_weather(image_file, weather):
    '''
    sauvegarde l'image (son indice determiné), la temperature environnante, l'humidité, la pression 
    '''
    with open('weather_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([image_file, weather])

# Function to display image and dropdown menu for weather selection
def display_image():
    # Create tkinter window
    root = tk.Tk()

    # Open file dialog and select image file
    image_file = "paris.png" # select_image_file() pour selectionner plus facilement

    # Load image and display in window
    img = tk.PhotoImage(file=image_file)
    canvas = tk.Canvas(root, width=500, height=500) #tk.Canvas(root, width=img.width(), height=img.height())
    canvas.create_image(0, 0, anchor='nw', image=img)
    canvas.pack()

    # Create dropdown menu for weather selection
    weather_label = ttk.Label(root, text='Select Weather:')
    weather_label.pack(pady=10)
    weather_var = tk.StringVar(root)
    weather_dropdown = ttk.Combobox(root, textvariable=weather_var, values=['Sunny', 'Rainy', 'Cloudy', 'Foggy', 'Night'])
    weather_dropdown.pack()

    # Create button to save weather and close window
    save_button = ttk.Button(root, text='Save Weather', command=lambda: save_weather(image_file, weather_var.get()))
    save_button.pack(pady=10)

    root.mainloop()

display_image()
