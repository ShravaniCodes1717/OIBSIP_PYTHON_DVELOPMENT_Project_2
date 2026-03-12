"""
Beginner Version: Command-Line BMI Calculator
Author: Your Name
Date: 2026
"""

import sys
import io

# Force UTF-8 encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

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
# INPUT VALIDATION
# ==========================================
def get_valid_float(prompt, min_value=0, max_value=500):
    """Get and validate float input from user."""
    while True:
        try:
            value = float(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Please enter a value between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
            exit()

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
# DISPLAY RESULTS
# ==========================================
def display_bmi_result(weight, height, bmi, category, description):
    """Display BMI calculation results."""
    print("\n" + "=" * 50)
    print("BMI CALCULATION RESULTS")
    print("=" * 50)
    print(f"Weight: {weight:.2f} kg")
    print(f"Height: {height:.2f} m")
    print(f"BMI: {bmi:.2f}")
    print(f"Category: {category.upper()}")
    print(f"Health Advice: {description}")
    print("=" * 50)

# ==========================================
# MAIN PROGRAM
# ==========================================
def main():
    """Main function to run the BMI calculator."""
    print("\n" + "=" * 50)
    print("BMI CALCULATOR - BEGINNER VERSION")
    print("=" * 50)
    
    try:
        # Get user input
        weight = get_valid_float("Enter your weight in kilograms (kg): ")
        height = get_valid_float("Enter your height in meters (m): ")
        
        # Calculate BMI
        bmi = calculate_bmi(weight, height)
        
        # Categorize BMI
        category, description = categorize_bmi(bmi)
        
        # Display results
        display_bmi_result(weight, height, bmi, category, description)
        
        # Ask if user wants to calculate again
        while True:
            choice = input("\nWould you like to calculate another BMI? (yes/no): ").lower()
            if choice in ['yes', 'y']:
                main()
                break
            elif choice in ['no', 'n']:
                print("\nThank you for using BMI Calculator! Stay healthy!")
                break
            else:
                print("Please enter 'yes' or 'no'.")
                
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()