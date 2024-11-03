import tkinter as tk
from tkinter import messagebox
import json
import os


# Funkcja do wczytywania zadań z pliku JSON
def load_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            return json.load(file)
    return []


# Funkcja do zapisywania zadań do pliku JSON
def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)


# Funkcja do dodawania zadania
def add_task():
    task_text = entry_task.get()
    task_priority = priority_var.get()
    if task_priority == "Brak":
        task_priority = ""  # Ustaw pusty priorytet dla "Brak"
    if task_text:
        tasks.append({"text": task_text, "completed": False, "priority": task_priority})
        save_tasks()
        update_task_list()
        entry_task.delete(0, tk.END)
    else:
        messagebox.showwarning("Uwaga", "Wpisz treść zadania")


# Funkcja do usuwania zaznaczonego zadania
def delete_task():
    selected_task_index = listbox_tasks.curselection()
    if selected_task_index:
        original_index = displayed_tasks[selected_task_index[0]]
        del tasks[original_index]
        save_tasks()
        update_task_list()
    else:
        messagebox.showwarning("Uwaga", "Wybierz zadanie do usunięcia")


# Funkcja do oznaczania zadania jako ukończonego
def complete_task():
    selected_task_index = listbox_tasks.curselection()
    if selected_task_index:
        original_index = displayed_tasks[selected_task_index[0]]
        task = tasks[original_index]
        task["completed"] = not task["completed"]
        if task["completed"]:
            task["priority"] = ""  # Usuń priorytet po oznaczeniu jako ukończone
        save_tasks()
        update_task_list()
    else:
        messagebox.showwarning("Uwaga", "Wybierz zadanie do oznaczenia")


# Funkcja do odświeżania listy zadań
def update_task_list():
    listbox_tasks.delete(0, tk.END)
    global displayed_tasks
    displayed_tasks = sorted(range(len(tasks)),
                             key=lambda i: ["Wysoki", "Średni", "Niski", ""].index(tasks[i]["priority"]))

    for index in displayed_tasks:
        task = tasks[index]
        if task["completed"]:
            task_text = f"{task['text']} ✅"  # Wyświetl tylko treść zadania i ikonę ukończenia
        else:
            task_text = f"{task['text']} ({task['priority']})" if task["priority"] else task['text']
        listbox_tasks.insert(tk.END, task_text)


# Inicjalizacja głównego okna aplikacji
root = tk.Tk()
root.title("Menadżer zadań")

# Lista zadań
tasks = load_tasks()
displayed_tasks = []  # Lista do śledzenia wyświetlanych indeksów zadań

# Pole tekstowe do wpisywania zadań
entry_task = tk.Entry(root, width=40)
entry_task.grid(row=0, column=0, padx=10, pady=10)

# Lista rozwijana do wyboru priorytetu
priority_var = tk.StringVar(value="Brak")
priority_menu = tk.OptionMenu(root, priority_var, "Wysoki", "Średni", "Niski", "Brak")
priority_menu.grid(row=0, column=1, padx=10, pady=10)

# Przyciski
button_add = tk.Button(root, text="Dodaj zadanie", command=add_task)
button_add.grid(row=0, column=2, padx=10, pady=10)

button_delete = tk.Button(root, text="Usuń zadanie", command=delete_task)
button_delete.grid(row=1, column=2, padx=10, pady=10)

button_complete = tk.Button(root, text="Oznacz jako ukończone", command=complete_task)
button_complete.grid(row=2, column=2, padx=10, pady=10)

# Lista zadań (Listbox)
listbox_tasks = tk.Listbox(root, width=50, height=15)
listbox_tasks.grid(row=1, column=0, columnspan=2, rowspan=3, padx=10, pady=10)

# Wyświetlenie zadań przy uruchomieniu aplikacji
update_task_list()

# Uruchomienie aplikacji
root.mainloop()
