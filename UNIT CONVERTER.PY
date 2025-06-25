import tkinter as tk
from tkinter import ttk

# Conversion function
def convert_length():
    try:
        length = float(entry_length.get())
        from_unit = from_unit_var.get()
        to_unit = to_unit_var.get()

        # Conversion logic
        if from_unit == "Kilometer":
            length *= 1000  # Convert to meters
        elif from_unit == "Meter":
            pass  # No conversion needed
        elif from_unit == "Centimeter":
            length /= 100  # Convert to meters
        elif from_unit == "Millimeter":
            length /= 1000  # Convert to meters
        elif from_unit == "Feet":
            length *= 0.3048  # Convert to meters
        elif from_unit == "Inches":
            length *= 0.0254  # Convert to meters

        if to_unit == "Kilometer":
            result = length / 1000  # Convert to kilometers
        elif to_unit == "Meter":
            result = length  # No conversion needed
        elif to_unit == "Centimeter":
            result = length * 100  # Convert to centimeters
        elif to_unit == "Millimeter":
            result = length * 1000  # Convert to millimeters
        elif to_unit == "Feet":
            result = length / 0.3048  # Convert to feet
        elif to_unit == "Inches":
            result = length / 0.0254  # Convert to inches

        result_label.config(text=f"Converted Length: {result} {to_unit}")
    except ValueError:
        result_label.config(text="Please enter a valid number.")

# Create the main window
root = tk.Tk()
root.title("Length Converter")

# Calculate the center coordinates of the window
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = 0  # Align top

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create frame for "Unit converter" text
hello_frame = ttk.Frame(root, style="Hello.TFrame")
hello_frame.place(relx=0.5, rely=0.01, anchor=tk.N)

# Create label for "Unit converter" text

hello_label = tk.Label(hello_frame, text="Unit converter", font=("Arial", 18),foreground="#491B26", bg="#ffddee")
hello_label.pack()

# Create container frame
container_frame = ttk.Frame(root, padding=40, borderwidth=3, relief="raised", style="Container.TFrame")
container_frame.place(relx=0.5, rely=0.1, anchor=tk.N)

# Create and add widgets to the container frame
label_length = ttk.Label(container_frame, text="Enter Length:")
label_length.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

entry_length = ttk.Entry(container_frame)
entry_length.grid(row=0, column=1, padx=5, pady=5)

label_from_unit = ttk.Label(container_frame, text="From Unit:")
label_from_unit.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

from_unit_var = tk.StringVar()
from_unit_option = ttk.Combobox(container_frame, textvariable=from_unit_var, values=["Kilometer", "Meter", "Centimeter", "Millimeter", "Feet", "Inches"])
from_unit_option.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

label_to_unit = ttk.Label(container_frame, text="To Unit:")
label_to_unit.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

to_unit_var = tk.StringVar()
to_unit_option = ttk.Combobox(container_frame, textvariable=to_unit_var, values=["Kilometer", "Meter", "Centimeter", "Millimeter", "Feet", "Inches"])
to_unit_option.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

convert_button = ttk.Button(container_frame, text="Convert", command=convert_length, style="TButton")
convert_button.grid(row=3, column=0, columnspan=2, pady=10)

result_label = ttk.Label(container_frame, text="", style="TLabel")
result_label.grid(row=4, column=0, columnspan=2, sticky=tk.W)

# Create custom styles for the button, label, and container frame
style = ttk.Style()
style.configure("TButton", foreground="#491B26", background="#242021",font=("Arial", 12))
style.configure("TLabel", background="#FEDAEC",bordercolor="black", font=("Arial", 12))
style.configure("Container.TFrame", background="#EAE0DA", bordercolor="black")
style.configure("Hello.TFrame", background="#D8C6DE")
root.configure(bg="#D8C6DE")

root.mainloop()
