import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from datetime import datetime

class BMIHistory:
    def __init__(self):
        self.history = []

    def add_entry(self, bmi):
        entry = {"bmi": bmi, "date": datetime.now()}
        self.history.append(entry)

    def clear_history(self):
        self.history = []

    def save_history(self, filename="bmi_history.txt"):
        with open(filename, "w") as f:
            for entry in self.history:
                f.write("{},{}\n".format(entry["bmi"], entry["date"].strftime("%Y-%m-%d %H:%M:%S")))

    def load_history(self, filename="bmi_history.txt"):
        self.clear_history()
        try:
            with open(filename, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    bmi = float(parts[0])
                    date = datetime.strptime(parts[1], "%Y-%m-%d %H:%M:%S")
                    entry = {"bmi": bmi, "date": date}
                    self.history.append(entry)
        except FileNotFoundError:
            pass

def calculate_bmi():
    # Validate input
    weight_str = weight_entry.get()
    height_str = height_entry.get()
    if not weight_str or not height_str:
        result_label.config(text="Please enter both weight and height.", foreground="red")
        return
    try:
        weight = float(weight_str)
        height = float(height_str) / 100  # converting height from cm to meters
    except ValueError:
        result_label.config(text="Please enter valid numerical values.", foreground="red")
        return

    bmi = weight / (height * height)
    result_label.config(text="Your BMI: {:.2f}".format(bmi))
    display_bmi_category(bmi)
    recommend_action(bmi)
    history.add_entry(bmi)

def display_bmi_category(bmi):
    if bmi < 18.5:
        bmi_category_label.config(text="Underweight", foreground="blue")
    elif 18.5 <= bmi < 24.9:
        bmi_category_label.config(text="Normal Weight", foreground="green")
    elif 24.9 <= bmi < 29.9:
        bmi_category_label.config(text="Overweight", foreground="orange")
    elif bmi >= 29.9:
        bmi_category_label.config(text="Obese", foreground="red")

def recommend_action(bmi):
    if bmi < 18.5:
        recommendation_label.config(text="Recommendation: Increase calorie intake with nutritious foods and strength training.")
    elif 18.5 <= bmi < 24.9:
        recommendation_label.config(text="Recommendation: Maintain a balanced diet and regular exercise routine.")
    elif 24.9 <= bmi < 29.9:
        recommendation_label.config(text="Recommendation: Focus on portion control and increase physical activity.")
    elif bmi >= 29.9:
        recommendation_label.config(text="Recommendation: Seek medical advice for a personalized weight loss plan.")

def clear_fields():
    weight_entry.delete(0, 'end')
    height_entry.delete(0, 'end')
    result_label.config(text="")
    bmi_category_label.config(text="", foreground="black")
    recommendation_label.config(text="")

def save_history():
    history.save_history()
    result_label.config(text="BMI history saved to bmi_history.txt", foreground="green")

def load_history():
    history.load_history()
    result_label.config(text="BMI history loaded from bmi_history.txt", foreground="green")

def plot_history():
    if history.history:
        dates = [entry["date"] for entry in history.history]
        bmis = [entry["bmi"] for entry in history.history]
        plt.plot(dates, bmis, marker='o')
        plt.xlabel('Date')
        plt.ylabel('BMI')
        plt.title('BMI History')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        result_label.config(text="No BMI history to plot.", foreground="red")

# Create the main window
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x400")

# Create style
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))

# BMI history object
history = BMIHistory()

# Create labels and entries for weight and height
weight_label = ttk.Label(root, text="Weight (kg):")
weight_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

weight_entry = ttk.Entry(root)
weight_entry.grid(row=0, column=1, padx=10, pady=10)

height_label = ttk.Label(root, text="Height (cm):")
height_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

height_entry = ttk.Entry(root)
height_entry.grid(row=1, column=1, padx=10, pady=10)

# Create a button to calculate BMI
calculate_button = ttk.Button(root, text="Calculate BMI", command=calculate_bmi)
calculate_button.grid(row=2, columnspan=2, padx=10, pady=10)

# Create a label to display the result
result_label = ttk.Label(root, text="", font=("Helvetica", 14, "bold"))
result_label.grid(row=3, columnspan=2, padx=10, pady=10)

# Create a label to display BMI category
bmi_category_label = ttk.Label(root, text="", font=("Helvetica", 9, "bold"))
bmi_category_label.grid(row=4, columnspan=2, padx=10, pady=10)

# Create a label to provide recommendations
recommendation_label = ttk.Label(root, text="", font=("Helvetica", 7))
recommendation_label.grid(row=5, columnspan=2, padx=10, pady=10)

# Create a button to clear fields
clear_button = ttk.Button(root, text="Clear", command=clear_fields)
clear_button.grid(row=6, columnspan=2, padx=10, pady=10)

# Create a button to save history
save_button = ttk.Button(root, text="Save History", command=save_history)
save_button.grid(row=7, columnspan=2, padx=10, pady=10)

# Create a button to load history
load_button = ttk.Button(root, text="Load History", command=load_history)
load_button.grid(row=8, columnspan=2, padx=10, pady=10)

# Create a button to plot history
plot_button = ttk.Button(root, text="Plot History", command=plot_history)
plot_button.grid(row=9, columnspan=2, padx=10, pady=10)

# Run the main event loop
root.mainloop()