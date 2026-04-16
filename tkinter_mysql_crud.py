import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

connection = None
db_connected = False

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='college_db'
    )
    if connection.is_connected():
        db_connected = True
except Error as e:
    db_connected = False
    messagebox.showerror("Database Error", f"Cannot connect to MySQL: {e}\n\nPlease ensure MySQL is running and credentials are correct.")

def connect_db():
    global connection, db_connected
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='college_db'
        )
        if connection.is_connected():
            db_connected = True
            create_table()
            messagebox.showinfo("Success", "Connected to MySQL Database!")
            return True
    except Error as e:
        db_connected = False
        messagebox.showerror("Database Error", f"Cannot connect to MySQL: {e}")
        return False

def create_table():
    global connection
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                roll_no VARCHAR(20),
                email VARCHAR(100),
                phone VARCHAR(15),
                course VARCHAR(50)
            )
        """)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror("Error", f"Failed to create table: {e}")

def insert_record():
    global connection
    name = entry_name.get()
    roll = entry_roll.get()
    email = entry_email.get()
    phone = entry_phone.get()
    course = entry_course.get()
    
    if not name or not roll:
        messagebox.showwarning("Warning", "Name and Roll No are required!")
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO students (name, roll_no, email, phone, course)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, roll, email, phone, course))
        connection.commit()
        cursor.close()
        messagebox.showinfo("Success", "Record inserted successfully!")
        clear_form()
        show_records()
    except Error as e:
        messagebox.showerror("Error", f"Failed to insert: {e}")

def show_records():
    global connection
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()
        cursor.close()
        
        for row in tree.get_children():
            tree.delete(row)
        
        for row in records:
            tree.insert('', 'end', values=row)
    except Error as e:
        messagebox.showerror("Error", f"Failed to fetch records: {e}")

def delete_record():
    global connection
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a record to delete!")
        return
    
    values = tree.item(selected[0])['values']
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s", (values[0],))
        connection.commit()
        cursor.close()
        messagebox.showinfo("Success", "Record deleted successfully!")
        show_records()
    except Error as e:
        messagebox.showerror("Error", f"Failed to delete: {e}")

def update_record():
    global connection
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a record to update!")
        return
    
    values = tree.item(selected[0])['values']
    entry_name.insert(0, values[1])
    entry_roll.insert(0, values[2])
    entry_email.insert(0, values[3])
    entry_phone.insert(0, values[4])
    entry_course.insert(0, values[5])
    
    def save_update():
        global connection
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE students SET name=%s, roll_no=%s, email=%s, phone=%s, course=%s
                WHERE id=%s
            """, (entry_name.get(), entry_roll.get(), entry_email.get(), entry_phone.get(), entry_course.get(), values[0]))
            connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "Record updated successfully!")
            clear_form()
            show_records()
            btn_update.config(state='normal')
            btn_save_update.pack_forget()
        except Error as e:
            messagebox.showerror("Error", f"Failed to update: {e}")
    
    btn_save_update.pack(after=btn_update, side='left', padx=5)
    btn_update.config(state='disabled')

def clear_form():
    entry_name.delete(0, 'end')
    entry_roll.delete(0, 'end')
    entry_email.delete(0, 'end')
    entry_phone.delete(0, 'end')
    entry_course.delete(0, 'end')

root = tk.Tk()
root.title("Student Management System with MySQL")
root.geometry("800x600")

frame_form = tk.Frame(root, padx=10, pady=10)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Name:").grid(row=0, column=0, sticky='w', pady=5)
entry_name = tk.Entry(frame_form, width=30)
entry_name.grid(row=0, column=1, pady=5)

tk.Label(frame_form, text="Roll No:").grid(row=1, column=0, sticky='w', pady=5)
entry_roll = tk.Entry(frame_form, width=30)
entry_roll.grid(row=1, column=1, pady=5)

tk.Label(frame_form, text="Email:").grid(row=2, column=0, sticky='w', pady=5)
entry_email = tk.Entry(frame_form, width=30)
entry_email.grid(row=2, column=1, pady=5)

tk.Label(frame_form, text="Phone:").grid(row=3, column=0, sticky='w', pady=5)
entry_phone = tk.Entry(frame_form, width=30)
entry_phone.grid(row=3, column=1, pady=5)

tk.Label(frame_form, text="Course:").grid(row=4, column=0, sticky='w', pady=5)
entry_course = tk.Entry(frame_form, width=30)
entry_course.grid(row=4, column=1, pady=5)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_insert = tk.Button(frame_buttons, text="INSERT", command=insert_record, bg='green', fg='white', width=10)
btn_insert.pack(side='left', padx=5)

btn_show = tk.Button(frame_buttons, text="SHOW ALL", command=show_records, bg='blue', fg='white', width=10)
btn_show.pack(side='left', padx=5)

btn_update = tk.Button(frame_buttons, text="UPDATE", command=update_record, bg='gray', fg='white', width=10)
btn_update.pack(side='left', padx=5)

btn_delete = tk.Button(frame_buttons, text="DELETE", command=delete_record, bg='gray', fg='white', width=10)
btn_delete.pack(side='left', padx=5)

btn_clear = tk.Button(frame_buttons, text="CLEAR", command=clear_form, bg='gray', fg='white', width=10)
btn_clear.pack(side='left', padx=5)

btn_save_update = tk.Button(frame_buttons, text="SAVE UPDATE", bg='purple', fg='white', width=12)

columns = ('ID', 'Name', 'Roll No', 'Email', 'Phone', 'Course')
tree = ttk.Treeview(root, columns=columns, show='headings', height=12)
tree.pack(pady=20)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack()

if db_connected:
    show_records()

root.mainloop()

if connection.is_connected():
    connection.close()
