import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class ExpenseTracker:
    def __init__(self, file_path="expenses.csv"):
        self.file_path = file_path
        self.categories = ["Food", "Transport", "Utilities", "Entertainment"]
        self.df = None
        self.load_data()
    
    def load_data(self):
        try:
            self.df = pd.read_csv(self.file_path)
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            invalid_rows = len(self.df)
            self.df = self.df[(self.df['Amount'] > 0) & (self.df['Category'].isin(self.categories))]
            invalid_rows -= len(self.df)
            if invalid_rows:
                print(f"Removed {invalid_rows} invalid rows")
        except FileNotFoundError:
            print("File not found. Starting with empty data.")
            self.df = pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Description'])
    
    def add_expense(self, date, amount, category, description):
        try:
            parsed_date = pd.to_datetime(date)
            amount = float(amount)
            if amount <= 0:
                print("Error: Amount must be positive")
                return
            if category not in self.categories:
                print(f"Error: Category must be one of {self.categories}")
                return
            if not description:
                description = "No description"
        except ValueError:
            print("Error: Invalid date or amount")
            return
        
        new_expense = pd.DataFrame({
            'Date': [parsed_date],
            'Amount': [amount],
            'Category': [category],
            'Description': [description]
        })
        self.df = pd.concat([self.df, new_expense], ignore_index=True)
        self.df.to_csv(self.file_path, index=False)
        print("Expense added!")
    
    def get_summary(self):
        if self.df.empty:
            print("No expenses recorded.")
            return
        
        total = np.sum(self.df['Amount'])
        avg = np.mean(self.df['Amount'])
        category_totals = self.df.groupby('Category')['Amount'].sum()
        
        summary_lines = [
            "Expense Summary:",
            f"Total Expenses: ${total:.2f}",
            f"Average Expense: ${avg:.2f}",
            "",
            "Expenses by Category:"
        ]
        for category, amount in category_totals.items():
            summary_lines.append(f"{category}: ${amount:.2f}")
        
        for line in summary_lines:
            print(line)
    
    def filter_expenses(self, category=None, start_date=None, end_date=None, min_amount=None):
        filtered_df = self.df.copy()
        
        if category:
            filtered_df = filtered_df[filtered_df['Category'] == category]
        if start_date:
            try:
                start = pd.to_datetime(start_date)
                filtered_df = filtered_df[filtered_df['Date'] >= start]
            except ValueError:
                print("Error: Invalid start date")
                return
        if end_date:
            try:
                end = pd.to_datetime(end_date)
                filtered_df = filtered_df[filtered_df['Date'] <= end]
            except ValueError:
                print("Error: Invalid end date")
                return
        if min_amount:
            try:
                min_amt = float(min_amount)
                filtered_df = filtered_df[filtered_df['Amount'] >= min_amt]
            except ValueError:
                print("Error: Invalid minimum amount")
                return
        
        if filtered_df.empty:
            print("No expenses found.")
            return
        print(filtered_df.to_string(index=False))
    
    def generate_report(self):
        if self.df.empty:
            print("No expenses to report.")
            return
        
        total = np.sum(self.df['Amount'])
        category_totals = self.df.groupby('Category')['Amount'].sum()
        top_category = category_totals.idxmax()
        monthly_totals = self.df.groupby(self.df['Date'].dt.to_period('M'))['Amount'].sum()
        
        report_lines = [
            "Expense Report",
            "=" * 30,
            f"Total Expenses: ${total:.2f}",
            f"Top Spending Category: {top_category}",
            "",
            "Monthly Spending:"
        ]
        for month, amount in monthly_totals.items():
            report_lines.append(f"{month}: ${amount:.2f}")
        
        for line in report_lines:
            print(line)
    
    def visualize_expenses(self):
        if self.df.empty:
            print("No data to visualize.")
            return
        
        sns.set_style("whitegrid")
        plt.figure(figsize=(12, 8))
        
        soft_teal = '#4DB6AC'
        warm_coral = '#FF7043'
        muted_purple = '#9575CD'
        light_gold = '#FFD54F'
        slate_blue = '#78909C'
        
        plt.subplot(2, 2, 1)
        category_totals = self.df.groupby('Category')['Amount'].sum()
        bars = plt.bar(category_totals.index, category_totals.values, color=soft_teal)
        for i, v in enumerate(category_totals.values):
            plt.text(i, v + 5, f"${v:.2f}", ha='center', va='bottom')
        plt.title("Total Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount ($)")
        
        plt.subplot(2, 2, 2)
        monthly_sums = self.df.groupby(self.df['Date'].dt.to_period('M'))['Amount'].sum()
        months = [str(m) for m in monthly_sums.index]
        plt.plot(months, monthly_sums.values, marker='o', color=warm_coral)
        for i, v in enumerate(monthly_sums.values):
            plt.text(i, v + 5, f"${v:.2f}", ha='center', va='bottom')
        plt.title("Spending Over Time")
        plt.xlabel("Month")
        plt.ylabel("Amount ($)")
        plt.xticks(rotation=45)
        
        plt.subplot(2, 2, 3)
        plt.pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%',
                colors=[soft_teal, warm_coral, muted_purple, light_gold])
        plt.title("Spending by Category")
        
        plt.subplot(2, 2, 4)
        plt.hist(self.df['Amount'], bins=10, color=slate_blue, edgecolor='black')
        plt.title("Expense Amount Distribution")
        plt.xlabel("Amount ($)")
        plt.ylabel("Count")
        
        plt.tight_layout()
        plt.savefig('expense_dashboard.png')
        plt.close()
        print("Charts saved as expense_dashboard.png")

def main():
    tracker = ExpenseTracker()
    
    while True:
        print("\nWelcome to Expense Tracker")
        print("1. Add New Expense")
        print("2. Show Summary")
        print("3. Filter Expenses")
        print("4. Show Report")
        print("5. Create Charts")
        print("6. Exit")
        
        choice = input("Enter choice (1-6): ")
        
        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            amount = input("Enter amount: ")
            category = input("Enter category (Food/Transport/Utilities/Entertainment): ")
            description = input("Enter description: ")
            tracker.add_expense(date, amount, category, description)
        
        elif choice == '2':
            tracker.get_summary()
        
        elif choice == '3':
            category = input("Enter category (or press Enter to skip): ")
            start_date = input("Enter start date (YYYY-MM-DD, or Enter to skip): ")
            end_date = input("Enter end date (YYYY-MM-DD, or Enter to skip): ")
            min_amount = input("Enter minimum amount (or Enter to skip): ")
            tracker.filter_expenses(category, start_date, end_date, min_amount)
        
        elif choice == '4':
            tracker.generate_report()
        
        elif choice == '5':
            tracker.visualize_expenses()
        
        elif choice == '6':
            print("Exiting program...")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()