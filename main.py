import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="feedback_db"
)
cursor = conn.cursor()

def fetch_data():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM feedback")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

def submit_feedback():
    name = name_var.get()
    subject = subject_var.get()
    message = message_var.get()
    if name and subject and message:
        cursor.execute("INSERT INTO feedback (name, subject, message) VALUES (%s, %s, %s)", (name, subject, message))
        conn.commit()
        fetch_data()
        name_var.set("")
        subject_var.set("")
        message_var.set("")
    else:
        messagebox.showwarning("Input Error", "All fields are required.")

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showinfo("No Selection", "Please select a row to delete.")
        return
    for sel in selected:
        values = tree.item(sel, "values")
        cursor.execute("DELETE FROM feedback WHERE id = %s", (values[0],))
    conn.commit()
    fetch_data()

def reset_all():
    if messagebox.askyesno("Confirm Reset", "Delete all feedback entries?"):
        cursor.execute("DELETE FROM feedback")
        conn.commit()
        fetch_data()

# GUI setup
root = tk.Tk()
root.title("Student Feedback System")

name_var = tk.StringVar()
subject_var = tk.StringVar()
message_var = tk.StringVar()

tk.Label(root, text="Name").grid(row=0, column=0)
tk.Entry(root, textvariable=name_var).grid(row=0, column=1)

tk.Label(root, text="Subject").grid(row=1, column=0)
tk.Entry(root, textvariable=subject_var).grid(row=1, column=1)

tk.Label(root, text="Feedback").grid(row=2, column=0)
tk.Entry(root, textvariable=message_var).grid(row=2, column=1)

tk.Button(root, text="Submit", command=submit_feedback).grid(row=3, column=0, columnspan=2)
tk.Button(root, text="Delete Selected", command=delete_selected).grid(row=4, column=0, columnspan=2)
tk.Button(root, text="Reset All", command=reset_all).grid(row=5, column=0, columnspan=2)

cols = ("ID", "Name", "Subject", "Message")
tree = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.grid(row=6, column=0, columnspan=2)

fetch_data()
root.mainloop()