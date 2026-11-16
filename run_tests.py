import io
import os
import sys
import warnings

# Suppress Agg canvas non-interactive warning during automated tests
warnings.filterwarnings('ignore')

# Non-interactive backend for automated tests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from employee_analyzer import (
    load_and_clean_data,
    show_summary,
    department_and_filter,
    plot_chart
)

def run_all_tests():
    tc1_data = (
        "Emp_ID,Name,Department,Salary,Experience\n"
        "E1,Aman,IT,50000,3\n"
        "E2,Riya,HR,40000,2\n"
        "E3,Karan,IT,70000,5\n"
    )

    tc2_data = (
        "Emp_ID,Name,Department,Salary,Experience\n"
        "E1,Aman,IT,50000,3\n"
    )

    tc3_data = (
        "Emp_ID,Name,Department,Salary,Experience\n"
        "E1,Aman,IT,50000,3\n"
        "E2,Riya,HR,40000,2\n"
        "E3,Karan,IT,70000,5\n"
        "E1,Aman,IT,50000,3\n"
        "E4,Neha,HR,,4\n"
    )

    print("============================================================")
    print("RUNNING AUTOMATED TEST CASES FOR PS No. 24")
    print("============================================================\n")

    # --- Test Case 1: Normal Input ---
    print("--- Test Case 1: Normal Input ---")
    with open("temp_employees.csv", "w", encoding="utf-8") as f:
        f.write(tc1_data)
    df1 = load_and_clean_data("temp_employees.csv")
    show_summary(df1)
    print()

    # --- Test Case 2: Boundary / Minimum Input (1 row) ---
    print("--- Test Case 2: Boundary / Minimum Input (1 row only) ---")
    with open("temp_employees.csv", "w", encoding="utf-8") as f:
        f.write(tc2_data)
    df2 = load_and_clean_data("temp_employees.csv")
    show_summary(df2)
    print()

    # --- Test Case 3: Invalid Input (Duplicate row & Missing Salary) ---
    print("--- Test Case 3: Invalid Input (1 Duplicate + 1 Missing Salary) ---")
    with open("temp_employees.csv", "w", encoding="utf-8") as f:
        f.write(tc3_data)
    df3 = load_and_clean_data("temp_employees.csv")
    show_summary(df3)
    print()

    # --- Test Case 4: Department-wise and filter above 45000 ---
    print("--- Test Case 4: Department-wise and filter above 45000 ---")
    with open("temp_employees.csv", "w", encoding="utf-8") as f:
        f.write(tc1_data)
    df4 = load_and_clean_data("temp_employees.csv")
    department_and_filter(df4, limit=45000.0, show_chart=False)
    plot_chart(df4, block=False, save_path="dept_avg_salary.png")
    print()

    # Cleanup temp test file
    if os.path.exists("temp_employees.csv"):
        os.remove("temp_employees.csv")

    # Restore employees.csv to exact 3-row Test Case 1 dataset
    with open("employees.csv", "w", encoding="utf-8") as f:
        f.write(tc1_data)
    print("Restored employees.csv to 3-row Test Case 1 dataset.")
    print("\n============================================================")
    print("ALL TEST CASES EXECUTED SUCCESSFULLY")
    print("============================================================")

if __name__ == "__main__":
    run_all_tests()
