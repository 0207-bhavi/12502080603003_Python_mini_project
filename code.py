import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
 
DATA_FILE = "websites.json"
websites = []
 
def load_data():
    global websites
    if not os.path.exists(DATA_FILE):
        websites = []
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        websites = data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        websites = []
        messagebox.showwarning("Data Warning",
            "Saved data could not be read. Starting with an empty list.")
 
def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(websites, file, indent=4, ensure_ascii=False)
    except OSError as error:
        messagebox.showerror("Save Error", str(error))
 
def refresh_table(records=None):
    for item in table.get_children():
        table.delete(item)
    shown = records if records is not None else list(enumerate(websites))
    for index, record in shown:
        table.insert("", "end", iid=str(index), values=(
            record.get("name", ""), record.get("url", ""),
            record.get("category", ""), record.get("notes", "")))
 
def clear_fields():
    name_var.set("")
    url_var.set("")
    category_var.set("")
    notes_var.set("")
    name_entry.focus_set()
 
def add_website():
    name = name_var.get().strip()
    url = url_var.get().strip()
    category = category_var.get().strip() or "General"
    notes = notes_var.get().strip()
    if not name or not url:
        messagebox.showwarning("Missing Information",
                               "Enter both website name and URL.")
        return
    websites.append({"name": name, "url": url,
                     "category": category, "notes": notes})
    save_data()
    refresh_table()
    clear_fields()
    messagebox.showinfo("Added", "Website record added successfully.")
 
def search_websites(*args):
    query = search_var.get().strip().lower()
    matches = []
    for index, record in enumerate(websites):
        if not query or any(query in str(value).lower()
                            for value in record.values()):
            matches.append((index, record))
    refresh_table(matches)
 
def delete_website():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("No Selection",
                               "Select a website record first.")
        return
    index = int(selected[0])
    if messagebox.askyesno("Confirm Delete",
                           "Delete the selected website?"):
        websites.pop(index)
        save_data()
        refresh_table()
        messagebox.showinfo("Deleted", "Website record deleted.")
 
root = tk.Tk()
root.title("Website Data Tracker")
root.geometry("980x620")
root.minsize(780, 500)
 
ttk.Label(root, text="WEBSITE DATA TRACKER",
          font=("Arial", 18, "bold")).pack(pady=12)
 
form = ttk.Frame(root, padding=10)
form.pack(fill="x")
name_var = tk.StringVar()
url_var = tk.StringVar()
category_var = tk.StringVar()
notes_var = tk.StringVar()
search_var = tk.StringVar()
search_var.trace_add("write", search_websites)
 
ttk.Label(form, text="Website Name").grid(row=0, column=0, sticky="w", padx=5, pady=5)
name_entry = ttk.Entry(form, textvariable=name_var, width=28)
name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
ttk.Label(form, text="Website URL").grid(row=0, column=2, sticky="w", padx=5, pady=5)
ttk.Entry(form, textvariable=url_var, width=35).grid(row=0, column=3, sticky="ew", padx=5, pady=5)
ttk.Label(form, text="Category").grid(row=1, column=0, sticky="w", padx=5, pady=5)
ttk.Entry(form, textvariable=category_var).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
ttk.Label(form, text="Notes").grid(row=1, column=2, sticky="w", padx=5, pady=5)
ttk.Entry(form, textvariable=notes_var).grid(row=1, column=3, sticky="ew", padx=5, pady=5)
form.columnconfigure(1, weight=1)
form.columnconfigure(3, weight=1)
 
buttons = ttk.Frame(root, padding=(10, 0))
buttons.pack(fill="x")
ttk.Button(buttons, text="Add Website", command=add_website).pack(side="left", padx=4)
ttk.Button(buttons, text="Delete Selected", command=delete_website).pack(side="left", padx=4)
ttk.Button(buttons, text="Clear Fields", command=clear_fields).pack(side="left", padx=4)
 
search_frame = ttk.Frame(root, padding=10)
search_frame.pack(fill="x")
ttk.Label(search_frame, text="Search records:").pack(side="left", padx=5)
ttk.Entry(search_frame, textvariable=search_var).pack(side="left", fill="x", expand=True)
 
table_frame = ttk.Frame(root, padding=10)
table_frame.pack(fill="both", expand=True)
columns = ("name", "url", "category", "notes")
table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
for col, label, width in [
    ("name", "Website Name", 180), ("url", "URL", 280),
    ("category", "Category", 120), ("notes", "Notes", 250)]:
    table.heading(col, text=label)
    table.column(col, width=width)
scroll = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scroll.set)
table.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")
 
load_data()
refresh_table()
root.mainloop()
