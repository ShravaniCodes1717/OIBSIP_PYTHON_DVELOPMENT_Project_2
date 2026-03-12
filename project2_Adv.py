"""
Advanced Version: GUI BMI Calculator with Data Storage and Visualization
Author: Your Name
Date: 2026
"""

import sys
import io

# Force UTF-8 encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime

# ==========================================
# BMI CALCULATION CONSTANTS
# ==========================================
BMI_CATEGORIES = {
    'underweight': (0, 18.5),
    'normal': (18.5, 24.9),
    'overweight': (25.0, 29.9),
    'obese': (30.0, float('inf'))
}

# ==========================================
# BMI CALCULATION
# ==========================================
def calculate_bmi(weight, height):
    """Calculate BMI from weight (kg) and height (m)."""
    if height <= 0:
        raise ValueError("Height must be greater than 0")
    return weight / (height ** 2)

# ==========================================
# BMI CATEGORIZATION
# ==========================================
def categorize_bmi(bmi):
    """Categorize BMI value and return category and description."""
    for category, (min_val, max_val) in BMI_CATEGORIES.items():
        if min_val <= bmi < max_val:
            descriptions = {
                'underweight': 'You are underweight. Consider consulting a nutritionist.',
                'normal': 'You have a normal weight. Keep up the good work!',
                'overweight': 'You are overweight. Consider a balanced diet and exercise.',
                'obese': 'You are obese. Please consult a healthcare professional.'
            }
            return category, descriptions[category]
    return 'unknown', 'Unable to categorize BMI.'

# ==========================================
# DATA STORAGE MODULE
# ==========================================
class BMIDataManager:
    def __init__(self, filename='bmi_history.json'):
        self.filename = filename
        self.records = []
        self.load_data()
    
    def save_record(self, record):
        """Save a single BMI record."""
        self.records.append(record)
        self.save_data()
    
    def save_data(self):
        """Save all records to JSON file."""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.records, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        """Load records from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.records = json.load(f)
            except Exception as e:
                print(f"Error loading data: {e}")
                self.records = []
        else:
            self.records = []
    
    def get_all_records(self):
        """Get all BMI records."""
        return self.records
    
    def get_average_bmi(self):
        """Calculate average BMI from all records."""
        if not self.records:
            return 0.0
        total = sum(record['bmi'] for record in self.records)
        return round(total / len(self.records), 2)
    
    def get_trend(self):
        """Analyze BMI trend (improving, stable, worsening)."""
        if len(self.records) < 2:
            return "Not enough data"
        
        recent = self.records[-1]['bmi']
        older = self.records[-2]['bmi']
        
        if recent < older - 1:
            return "Improving"
        elif recent > older + 1:
            return "Worsening"
        else:
            return "Stable"
    
    def clear_all(self):
        """Clear all records."""
        self.records = []
        self.save_data()
    
    def export_to_csv(self):
        """Export records to CSV file."""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")]
            )
            if filename:
                with open(filename, 'w', newline='') as f:
                    f.write("Date,Weight(kg),Height(m),BMI,Category\n")
                    for record in self.records:
                        f.write(f"{record['date']},{record['weight']},{record['height']},{record['bmi']},{record['category']}\n")
                messagebox.showinfo("Success", "Data exported to CSV successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Export error: {str(e)}")

# ==========================================
# VISUALIZATION MODULE
# ==========================================
class BMIVisualization:
    def __init__(self, parent):
        self.parent = parent
        self.fig = None
        self.ax = None
    
    def create_charts(self, records):
        """Create BMI trend chart."""
        try:
            import matplotlib
            matplotlib.use('TkAgg')
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
            
            if not records:
                tk.Label(self.parent, text="No data to display", font=("Arial", 12)).pack(pady=20)
                return
            
            # Create figure
            self.fig, self.ax = plt.subplots(figsize=(8, 4))
            
            # Extract data
            dates = [record['date'].split()[0] for record in records]
            bmis = [record['bmi'] for record in records]
            
            # Plot
            self.ax.plot(dates, bmis, marker='o', linestyle='-', color='blue')
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('BMI')
            self.ax.set_title('BMI Trend Over Time')
            self.ax.grid(True, alpha=0.3)
            
            # Add category lines
            self.ax.axhline(y=18.5, color='green', linestyle='--', alpha=0.5, label='Underweight')
            self.ax.axhline(y=25.0, color='orange', linestyle='--', alpha=0.5, label='Overweight')
            self.ax.axhline(y=30.0, color='red', linestyle='--', alpha=0.5, label='Obese')
            
            self.ax.legend(loc='upper right')
            
            # Embed in Tkinter
            canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
            # Add toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.parent)
            toolbar.update()
            
        except ImportError:
            tk.Label(self.parent, text="Matplotlib not installed. Install with: pip install matplotlib", 
                    font=("Arial", 12), fg="red").pack(pady=20)
        except Exception as e:
            tk.Label(self.parent, text=f"Error creating chart: {str(e)}", font=("Arial", 12), fg="red").pack(pady=20)

# ==========================================
# GUI CLASS
# ==========================================
class BMICalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Initialize data manager
        self.data_manager = BMIDataManager()
        
        # Create UI
        self.create_widgets()
        
        # Load existing data
        self.load_data()
        
    def create_widgets(self):
        """Create all GUI widgets."""
        # Title
        title_label = ttk.Label(
            self.root, 
            text="Advanced BMI Calculator", 
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)
        
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Input Details", padding=10)
        input_frame.pack(padx=20, pady=10, fill='x')
        
        # Weight Input
        ttk.Label(input_frame, text="Weight (kg):").grid(row=0, column=0, sticky='w', pady=5)
        self.weight_var = tk.DoubleVar()
        self.weight_entry = ttk.Entry(input_frame, textvariable=self.weight_var, width=15)
        self.weight_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Height Input
        ttk.Label(input_frame, text="Height (m):").grid(row=1, column=0, sticky='w', pady=5)
        self.height_var = tk.DoubleVar()
        self.height_entry = ttk.Entry(input_frame, textvariable=self.height_var, width=15)
        self.height_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Calculate Button
        calculate_btn = ttk.Button(
            input_frame, 
            text="Calculate BMI", 
            command=self.calculate_bmi
        )
        calculate_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Result Frame
        result_frame = ttk.LabelFrame(self.root, text="Results", padding=10)
        result_frame.pack(padx=20, pady=10, fill='x')
        
        self.result_label = ttk.Label(
            result_frame, 
            text="BMI will be displayed here", 
            font=("Arial", 14)
        )
        self.result_label.pack(pady=10)
        
        # Category Label
        self.category_label = ttk.Label(
            result_frame, 
            text="", 
            font=("Arial", 12, "bold")
        )
        self.category_label.pack(pady=5)
        
        # Health Advice Label
        self.advice_label = ttk.Label(
            result_frame, 
            text="", 
            font=("Arial", 10),
            foreground="blue"
        )
        self.advice_label.pack(pady=5)
        
        # Save Button
        save_btn = ttk.Button(
            self.root, 
            text="Save to History", 
            command=self.save_to_history
        )
        save_btn.pack(pady=10)
        
        # View History Button
        history_btn = ttk.Button(
            self.root, 
            text="View History & Charts", 
            command=self.view_history
        )
        history_btn.pack(pady=5)
        
        # Clear Button
        clear_btn = ttk.Button(
            self.root, 
            text="Clear All", 
            command=self.clear_all
        )
        clear_btn.pack(pady=5)
        
    def calculate_bmi(self):
        """Calculate BMI from user input."""
        try:
            weight = self.weight_var.get()
            height = self.height_var.get()
            
            # Validate inputs
            if weight <= 0 or height <= 0:
                messagebox.showerror("Error", "Please enter valid positive values.")
                return
            
            if weight > 500 or height > 3:
                messagebox.showwarning("Warning", "Values seem unrealistic. Please check.")
                return
            
            # Calculate BMI
            bmi = calculate_bmi(weight, height)
            category, description = categorize_bmi(bmi)
            
            # Display results
            self.result_label.config(text=f"BMI: {bmi:.2f}")
            self.category_label.config(text=f"Category: {category.upper()}")
            self.advice_label.config(text=description)
            
            # Color code the category
            colors = {
                'underweight': 'orange',
                'normal': 'green',
                'overweight': 'orange',
                'obese': 'red'
            }
            self.category_label.config(foreground=colors.get(category, 'black'))
            
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def save_to_history(self):
        """Save current BMI calculation to history."""
        try:
            weight = self.weight_var.get()
            height = self.height_var.get()
            bmi = calculate_bmi(weight, height)
            category, _ = categorize_bmi(bmi)
            
            # Create record
            record = {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'weight': weight,
                'height': height,
                'bmi': round(bmi, 2),
                'category': category
            }
            
            # Save to database
            self.data_manager.save_record(record)
            messagebox.showinfo("Success", "BMI record saved to history!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Save error: {str(e)}")
    
    def load_data(self):
        """Load existing data from database."""
        try:
            self.data_manager.load_data()
        except Exception as e:
            print(f"Warning: Could not load data: {e}")
    
    def view_history(self):
        """View history and generate charts."""
        history_window = tk.Toplevel(self.root)
        history_window.title("BMI History & Charts")
        history_window.geometry("700x500")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(history_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # History Tab
        history_frame = ttk.Frame(notebook)
        notebook.add(history_frame, text="History")
        
        # Create treeview for history
        columns = ('Date', 'Weight', 'Height', 'BMI', 'Category')
        tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load data into treeview
        records = self.data_manager.get_all_records()
        for record in records:
            tree.insert('', 'end', values=(
                record['date'],
                record['weight'],
                record['height'],
                record['bmi'],
                record['category']
            ))
        
        # Charts Tab
        charts_frame = ttk.Frame(notebook)
        notebook.add(charts_frame, text="Charts")
        
        # Create visualization
        viz = BMIVisualization(charts_frame)
        viz.create_charts(records)
        viz.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Export Button
        export_btn = ttk.Button(
            history_window, 
            text="Export to CSV", 
            command=lambda: self.data_manager.export_to_csv()
        )
        export_btn.pack(pady=10)
    
    def clear_all(self):
        """Clear all data."""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all data?"):
            self.data_manager.clear_all()
            messagebox.showinfo("Success", "All data cleared!")
            self.result_label.config(text="BMI will be displayed here")
            self.category_label.config(text="")
            self.advice_label.config(text="")

# ==========================================
# MAIN FUNCTION
# ==========================================
def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = BMICalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()