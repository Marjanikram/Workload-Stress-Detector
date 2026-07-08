import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
import matplotlib.pyplot as plt

FILE_NAME = "employees.csv"

# Create CSV file if it doesn't exist
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=[
        "Employee",
        "Working Hours",
        "Meetings",
        "Break Hours",
        "Overtime",
        "Stress Score",
        "Stress Level"
    ])
    df.to_csv(FILE_NAME, index=False)


def analyze():
    try:
        # Get user input
        name = name_entry.get().strip()

        if name == "":
            messagebox.showerror("Error", "Please enter the employee name.")
            return

        hours = float(hours_entry.get())
        meetings = int(meeting_entry.get())
        breaks = float(break_entry.get())
        overtime = float(overtime_entry.get())

        # Calculate stress score
        score = hours + (meetings * 2) + (overtime * 3) - breaks

        # Determine stress level
        if score <= 10:
            level = "Low Stress"
            recommendation = "Keep maintaining a healthy schedule."

        elif score <= 18:
            level = "Moderate Stress"
            recommendation = "Take short breaks and avoid unnecessary meetings."

        elif score <= 25:
            level = "High Stress"
            recommendation = "Reduce workload and increase rest."

        else:
            level = "Burnout Risk"
            recommendation = "Take leave and talk to your manager."

        # Display result
        result.config(
            text=f"Stress Score: {score:.1f}\n\n"
                 f"Stress Level: {level}\n\n"
                 f"Recommendation:\n{recommendation}"
        )

        # Read CSV safely
        if os.path.getsize(FILE_NAME) == 0:
            df = pd.DataFrame(columns=[
                "Employee",
                "Working Hours",
                "Meetings",
                "Break Hours",
                "Overtime",
                "Stress Score",
                "Stress Level"
            ])
        else:
            df = pd.read_csv(FILE_NAME)

        # Add new employee
        new_row = {
            "Employee": name,
            "Working Hours": hours,
            "Meetings": meetings,
            "Break Hours": breaks,
            "Overtime": overtime,
            "Stress Score": score,
            "Stress Level": level
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(FILE_NAME, index=False)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def show_graph():
    try:
        if not os.path.exists(FILE_NAME):
            messagebox.showinfo("No Data", "No employee data found.")
            return

        df = pd.read_csv(FILE_NAME)

        if df.empty:
            messagebox.showinfo("No Data", "No employee data available.")
            return

        plt.figure(figsize=(8, 5))
        plt.bar(df["Employee"], df["Stress Score"])
        plt.title("Employee Stress Scores")
        plt.xlabel("Employee")
        plt.ylabel("Stress Score")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Graph Error", str(e))


def clear():
    name_entry.delete(0, tk.END)
    hours_entry.delete(0, tk.END)
    meeting_entry.delete(0, tk.END)
    break_entry.delete(0, tk.END)
    overtime_entry.delete(0, tk.END)

    result.config(text="")


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Workload Stress Detector")
root.geometry("500x600")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Workload Stress Detector",
    font=("Arial", 18, "bold")
)
title.pack(pady=15)

tk.Label(root, text="Employee Name").pack()
name_entry = tk.Entry(root, width=30)
name_entry.pack()

tk.Label(root, text="Working Hours").pack()
hours_entry = tk.Entry(root, width=30)
hours_entry.pack()

tk.Label(root, text="Number of Meetings").pack()
meeting_entry = tk.Entry(root, width=30)
meeting_entry.pack()

tk.Label(root, text="Break Hours").pack()
break_entry = tk.Entry(root, width=30)
break_entry.pack()

tk.Label(root, text="Overtime Hours").pack()
overtime_entry = tk.Entry(root, width=30)
overtime_entry.pack(pady=(0, 15))

tk.Button(
    root,
    text="Analyze",
    command=analyze,
    width=20,
    bg="green",
    fg="white"
).pack(pady=5)

tk.Button(
    root,
    text="Show Graph",
    command=show_graph,
    width=20
).pack(pady=5)

tk.Button(
    root,
    text="Clear",
    command=clear,
    width=20
).pack(pady=5)

result = tk.Label(
    root,
    text="",
    font=("Arial", 12),
    justify="left"
)
result.pack(pady=20)

root.mainloop()