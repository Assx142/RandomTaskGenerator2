import random
import json
import tkinter as tk
from tkinter import messagebox, ttk

tasks = {
    "учёба": ["Прочитать статью", "Выучить 10 новых слов", "Решить 5 задач", "Посмотреть лекцию", "Написать конспект"],
    "спорт": ["Сделать зарядку", "Пробежать 2 км", "Отжаться 20 раз", "Присесть 30 раз", "Поплавать 30 минут"],
    "работа": ["Ответить на письма", "Сделать отчёт", "Провести встречу", "Назначить дедлайн", "Разобрать задачи"]
}

history_file = "task_history.json"
history = []

def load_history():
    global history
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

def save_history():
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_task_to_history(task, category):
    history.append({"task": task, "category": category})
    save_history()
    update_history_display()

def update_history_display():
    history_listbox.delete(0, tk.END)
    filter_category = filter_var.get()
    for item in history:
        if filter_category == "все" or item["category"] == filter_category:
            history_listbox.insert(tk.END, f"[{item['category']}] {item['task']}")

def generate_task():
    category = category_var.get()
    if category not in tasks:
        messagebox.showerror("Ошибка", "Выберите категорию")
        return
    if not tasks[category]:
        messagebox.showerror("Ошибка", f"Нет задач в категории '{category}'")
        return
    task = random.choice(tasks[category])
    task_label.config(text=task)
    add_task_to_history(task, category)

def add_custom_task():
    task_text = new_task_entry.get().strip()
    category = category_var.get()
    if not task_text:
        messagebox.showerror("Ошибка", "Задача не может быть пустой")
        return
    if category not in tasks:
        messagebox.showerror("Ошибка", "Выберите категорию")
        return
    tasks[category].append(task_text)
    add_task_to_history(task_text, category)
    new_task_entry.delete(0, tk.END)
    messagebox.showinfo("Успех", "Задача добавлена")

def filter_history():
    update_history_display()

def clear_history():
    global history
    if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
        history = []
        save_history()
        update_history_display()

load_history()

root = tk.Tk()
root.title("Random Task Generator")
root.geometry("600x500")
root.resizable(False, False)

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(main_frame, text="Генератор случайных задач", font=("Arial", 16, "bold")).pack(pady=10)

filter_frame = tk.Frame(main_frame)
filter_frame.pack(pady=5)
tk.Label(filter_frame, text="Категория:").pack(side=tk.LEFT, padx=5)
category_var = tk.StringVar(value="учёба")
category_menu = ttk.Combobox(filter_frame, textvariable=category_var, values=["учёба", "спорт", "работa"])
category_menu.pack(side=tk.LEFT, padx=5)

generate_btn = tk.Button(main_frame, text="Сгенерировать задачу", command=generate_task, bg="green", fg="white", font=("Arial", 12), padx=20, pady=10)
generate_btn.pack(pady=15)

task_label = tk.Label(main_frame, text="Нажмите кнопку", font=("Arial", 14), wraplength=500)
task_label.pack(pady=10)

tk.Label(main_frame, text="Добавить свою задачу:").pack(pady=5)
add_frame = tk.Frame(main_frame)
add_frame.pack(pady=5)
new_task_entry = tk.Entry(add_frame, width=40)
new_task_entry.pack(side=tk.LEFT, padx=5)
add_btn = tk.Button(add_frame, text="Добавить", command=add_custom_task)
add_btn.pack(side=tk.LEFT)

tk.Label(main_frame, text="История задач:").pack(pady=(15, 5))
filter_history_frame = tk.Frame(main_frame)
filter_history_frame.pack(pady=5)
tk.Label(filter_history_frame, text="Фильтр по категории:").pack(side=tk.LEFT, padx=5)
filter_var = tk.StringVar(value="все")
filter_menu = ttk.Combobox(filter_history_frame, textvariable=filter_var, values=["все", "учёба", "спорт", "работа"])
filter_menu.pack(side=tk.LEFT, padx=5)
filter_menu.bind("<<ComboboxSelected>>", lambda e: filter_history())

history_frame = tk.Frame(main_frame)
history_frame.pack(fill=tk.BOTH, expand=True, pady=5)
scrollbar = tk.Scrollbar(history_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
history_listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set, height=10)
history_listbox.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=history_listbox.yview)

clear_btn = tk.Button(main_frame, text="Очистить историю", command=clear_history, bg="red", fg="white")
clear_btn.pack(pady=10)

update_history_display()

root.mainloop()
