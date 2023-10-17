import tkinter as tk
from tkinter import ttk
import sqlite3

# Создаем SQLite базу данных и таблицу сотрудников
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        full_name TEXT,
        phone_number TEXT,
        email TEXT,
        salary REAL
    )
''')
conn.commit()

# Функции для управления сотрудниками
def add_employee():
    full_name = name_entry.get()
    phone_number = phone_entry.get()
    email = email_entry.get()
    salary = float(salary_entry.get())
    cursor.execute('INSERT INTO employees (full_name, phone_number, email, salary) VALUES (?, ?, ?, ?)',
                   (full_name, phone_number, email, salary))
    conn.commit()
    clear_entries()
    display_employees()

def update_employee():
    selected_item = treeview.selection()
    if selected_item:
        selected_id = treeview.item(selected_item)['values'][0]
        full_name = name_entry.get()
        phone_number = phone_entry.get()
        email = email_entry.get()
        salary = float(salary_entry.get())
        cursor.execute('UPDATE employees SET full_name=?, phone_number=?, email=?, salary=? WHERE id=?',
                       (full_name, phone_number, email, salary, selected_id))
        conn.commit()
        clear_entries()
        display_employees()

def delete_employee():
    selected_item = treeview.selection()
    if selected_item:
        selected_id = treeview.item(selected_item)['values'][0]
        cursor.execute('DELETE FROM employees WHERE id=?', (selected_id,))
        conn.commit()
        clear_entries()
        display_employees()

def search_employee():
    search_name = search_entry.get()
    cursor.execute('SELECT * FROM employees WHERE full_name LIKE ?', (f'%{search_name}%',))
    employees = cursor.fetchall()
    display_employees(employees)

def clear_entries():
    name_entry.delete(0, 'end')
    phone_entry.delete(0, 'end')
    email_entry.delete(0, 'end')
    salary_entry.delete(0, 'end')
    search_entry.delete(0, 'end')

def display_employees(employees=None):
    for row in treeview.get_children():
        treeview.delete(row)
    
    if employees is None:
        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()
    
    for employee in employees:
        treeview.insert('', 'end', values=employee)

# Создаем графический интерфейс
root = tk.Tk()
root.title("Список сотрудников компании")

frame = ttk.LabelFrame(root, text="Добавление/Изменение сотрудника")
frame.grid(row=0, column=0, padx=10, pady=10)

name_label = ttk.Label(frame, text="ФИО:")
name_label.grid(row=0, column=0)
name_entry = ttk.Entry(frame)
name_entry.grid(row=0, column=1)

phone_label = ttk.Label(frame, text="Номер телефона:")
phone_label.grid(row=1, column=0)
phone_entry = ttk.Entry(frame)
phone_entry.grid(row=1, column=1)

email_label = ttk.Label(frame, text="Email:")
email_label.grid(row=2, column=0)
email_entry = ttk.Entry(frame)
email_entry.grid(row=2, column=1)

salary_label = ttk.Label(frame, text="Заработная плата:")
salary_label.grid(row=3, column=0)
salary_entry = ttk.Entry(frame)
salary_entry.grid(row=3, column=1)

add_button = ttk.Button(frame, text="Добавить", command=add_employee)
add_button.grid(row=4, column=0, columnspan=2)

update_button = ttk.Button(frame, text="Изменить", command=update_employee)
update_button.grid(row=4, column=2, columnspan=2)

delete_button = ttk.Button(frame, text="Удалить", command=delete_employee)
delete_button.grid(row=4, column=4, columnspan=2)

search_label = ttk.Label(root, text="Поиск по ФИО:")
search_label.grid(row=1, column=0, padx=10, pady=10)
search_entry = ttk.Entry(root)
search_entry.grid(row=1, column=1)
search_button = ttk.Button(root, text="Искать", command=search_employee)
search_button.grid(row=1, column=2)

treeview = ttk.Treeview(root, columns=("ID", "ФИО", "Номер телефона", "Email", "Заработная плата"))
treeview.heading("#1", text="ID")
treeview.heading("#2", text="ФИО")
treeview.heading("#3", text="Номер телефона")
treeview.heading("#4", text="Email")
treeview.heading("#5", text="Заработная плата")
treeview.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Добавляем сортировку данных в виджет Treeview
def sort_treeview(col, descending):
    data = [(treeview.set(child, col), child) for child in treeview.get_children('')]
    data.sort(reverse=descending)
    for i, item in enumerate(data):
        treeview.move(item[1], '', i)
    treeview.heading(col, command=lambda: sort_treeview(col, not descending))

for col in ("ID", "ФИО", "Номер телефона", "Email", "Заработная плата"):
    treeview.heading(col, text=col, command=lambda c=col: sort_treeview(c, False))

# Улучшим интерфейс и обработку ошибок
def show_error_message(message):
    error_window = tk.Toplevel()
    error_window.title("Ошибка")
    error_label = ttk.Label(error_window, text=message)
    error_label.pack(padx=10, pady=10)
    ok_button = ttk.Button(error_window, text="OK", command=error_window.destroy)
    ok_button.pack()

root.mainloop()
