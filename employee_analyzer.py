import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Handle UTF-8 output if needed
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def fmt_num(val):
    """Format numbers without trailing decimal if whole number."""
    try:
        fval = float(val)
        return str(int(fval)) if fval.is_integer() else f"{fval:.2f}"
    except (ValueError, TypeError):
        return str(val)


def load_and_clean_data(filepath="employees.csv"):
    """Load employees CSV and clean duplicates and missing salaries."""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None

    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()

    # Drop duplicates
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        df = df.drop_duplicates()
        print(f"Duplicates removed: {dup_count}")

    # Convert Salary to numeric and impute missing values with mean
    if 'Salary' in df.columns:
        df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')
        missing_count = df['Salary'].isna().sum()
        if missing_count > 0:
            mean_val = df['Salary'].mean()
            df['Salary'] = df['Salary'].fillna(mean_val)
            print(f"Missing Salary filled with mean: {mean_val:.2f}")
            print(f"Cleaned rows: {len(df)}")

    return df


def show_summary(df):
    """Option 1: Display overall summary."""
    if df is None or df.empty:
        print("No data available.")
        return

    total = len(df)
    avg_sal = df['Salary'].mean()
    max_idx = df['Salary'].idxmax()
    highest_row = df.loc[max_idx]
    highest_name = highest_row['Name']
    highest_sal = fmt_num(highest_row['Salary'])
    payroll = fmt_num(df['Salary'].sum())

    print(f"Employees: {total} | Average salary: {avg_sal:.2f}")
    print(f"Highest paid: {highest_name} ({highest_sal})")
    print(f"Total payroll: {payroll}")


def department_and_filter(df, limit=None, show_chart=True):
    """Option 2: Department breakdown, filter above limit, and bar chart."""
    if df is None or df.empty:
        print("No data available.")
        return

    # Department grouping preserving order
    dept_group = df.groupby('Department', sort=False)
    for dept, group in dept_group:
        count = len(group)
        mean_sal = group['Salary'].mean()
        unit = "employees" if count > 1 else "employee"
        print(f"{dept}: {count} {unit} | Avg salary: {mean_sal:.2f}")

    # Prompt for limit if not supplied
    if limit is None:
        val = input("Enter salary limit: ").strip()
        try:
            limit = float(val) if val else 45000.0
        except ValueError:
            limit = 45000.0

    # Boolean indexing for employees above salary limit
    above = df[df['Salary'] > limit]
    if not above.empty:
        items = [f"{row['Name']} ({fmt_num(row['Salary'])})" for _, row in above.iterrows()]
        print(f"Above {fmt_num(limit)}: " + " | ".join(items))
    else:
        print(f"Above {fmt_num(limit)}: None")

    # Bar chart
    if show_chart:
        plot_chart(df)


def plot_chart(df, block=True, save_path=None):
    """Plot Matplotlib bar chart for Department-wise Average Salary."""
    dept_avg = df.groupby('Department', sort=False)['Salary'].mean()
    plt.figure(figsize=(6, 4))
    plt.bar(dept_avg.index, dept_avg.values, color='steelblue', edgecolor='black')
    plt.title('Department-wise Average Salary')
    plt.xlabel('Department')
    plt.ylabel('Average Salary')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)

    print("Bar chart 'Department-wise Average Salary' displayed")
    plt.show(block=block)


def main():
    df = load_and_clean_data("employees.csv")

    while True:
        print("\n--- Menu ---")
        print("1. Summary")
        print("2. Department & Filter")
        print("3. Exit")

        choice = input("Enter choice: ").strip()
        if choice == '1':
            show_summary(df)
        elif choice == '2':
            department_and_filter(df)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
