import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog

# ---------- DATABASE SETUP ----------
conn = sqlite3.connect("twinmoons.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    species TEXT,
    description TEXT
)
""")
conn.commit()


# ---------- FUNCTIONS ----------
def save_character():
    name = entry_name.get()
    age = entry_age.get()
    species = entry_species.get()
    description = text_description.get("1.0", tk.END).strip()

    if not name:
        messagebox.showwarning("Missing Info", "Character must have a name!")
        return

    cursor.execute("INSERT INTO characters (name, age, species, description) VALUES (?, ?, ?, ?)",
                   (name, age, species, description))
    conn.commit()
    messagebox.showinfo("Saved", f"{name} has been added to the database.")
    clear_fields()
    load_characters()


def clear_fields():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_species.delete(0, tk.END)
    text_description.delete("1.0", tk.END)
    global selected_id
    selected_id = None


def load_characters(search_term=""):
    listbox_characters.delete(0, tk.END)
    if search_term:
        cursor.execute("SELECT id, name FROM characters WHERE name LIKE ? OR species LIKE ?",
                       (f"%{search_term}%", f"%{search_term}%"))
    else:
        cursor.execute("SELECT id, name FROM characters")
    for row in cursor.fetchall():
        listbox_characters.insert(tk.END, f"{row[0]} - {row[1]}")


def show_character(event):
    global selected_id
    try:
        selection = listbox_characters.get(listbox_characters.curselection())
        selected_id = selection.split(" - ")[0]
        cursor.execute("SELECT * FROM characters WHERE id = ?", (selected_id,))
        char = cursor.fetchone()

        if char:
            entry_name.delete(0, tk.END)
            entry_name.insert(0, char[1])
            entry_age.delete(0, tk.END)
            entry_age.insert(0, char[2] if char[2] else "")
            entry_species.delete(0, tk.END)
            entry_species.insert(0, char[3] if char[3] else "")
            text_description.delete("1.0", tk.END)
            text_description.insert(tk.END, char[4] if char[4] else "")
    except:
        pass


def search_characters():
    search_term = entry_search.get()
    load_characters(search_term)


def update_character():
    global selected_id
    if not selected_id:
        messagebox.showwarning("No Selection", "Select a character to update.")
        return

    name = entry_name.get()
    age = entry_age.get()
    species = entry_species.get()
    description = text_description.get("1.0", tk.END).strip()

    cursor.execute("UPDATE characters SET name=?, age=?, species=?, description=? WHERE id=?",
                   (name, age, species, description, selected_id))
    conn.commit()
    messagebox.showinfo("Updated", f"{name}'s information has been updated.")
    clear_fields()
    load_characters()


def delete_character():
    global selected_id
    if not selected_id:
        messagebox.showwarning("No Selection", "Select a character to delete.")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this character?")
    if confirm:
        cursor.execute("DELETE FROM characters WHERE id=?", (selected_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Character removed from the database.")
        clear_fields()
        load_characters()
        reset_autoincrement()


def reset_autoincrement():
    """Reset the auto-increment ID counter when the table is empty."""
    cursor.execute("SELECT COUNT(*) FROM characters")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='characters'")
        conn.commit()


def export_characters():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")],
        title="Export Character Data"
    )

    if not file_path:
        return

    cursor.execute("SELECT * FROM characters")
    rows = cursor.fetchall()

    with open(file_path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(f"ID: {r[0]}\nName: {r[1]}\nAge: {r[2]}\nSpecies: {r[3]}\nDescription: {r[4]}\n{'-'*40}\n")

    messagebox.showinfo("Export Successful", f"Character data exported to {file_path}")


# ---------- GUI SETUP ----------
window = tk.Tk()
window.title("Twin Moons Database")
window.geometry("1000x700")

# Set global font
app_font = ("Segoe UI", 10)
window.option_add("*Font", app_font)

try:
    window.iconbitmap("icon.ico")
except Exception as e:
    print(f"Icon not found or couldn't load: {e}")

# --- Moonlit Theme Colors ---
bg_color = "#0f1a2b"       # midnight blue
fg_color = "#e0e6f8"       # pale silver
button_color = "#243b55"   # darker blue-gray
highlight_color = "#3e5c76"  # accent for active widgets
hover_color = "#51759c"     # moonlit blue for hover effect

window.configure(bg=bg_color)

# --- Configure columns/rows for resizing ---
window.columnconfigure(1, weight=1)
window.rowconfigure(7, weight=1)

# --- Entry Section ---
def label(text, r, c):
    tk.Label(window, text=text, bg=bg_color, fg=fg_color, font=("Segoe UI", 10, "bold")).grid(row=r, column=c, sticky="e", padx=10, pady=5)

label("Name:", 0, 0)
entry_name = tk.Entry(window, width=60, bg=highlight_color, fg=fg_color, insertbackground=fg_color)
entry_name.grid(row=0, column=1, sticky="ew", padx=15, pady=8)

label("Age:", 1, 0)
entry_age = tk.Entry(window, width=60, bg=highlight_color, fg=fg_color, insertbackground=fg_color)
entry_age.grid(row=1, column=1, sticky="ew", padx=15, pady=8)

label("Species:", 2, 0)
entry_species = tk.Entry(window, width=60, bg=highlight_color, fg=fg_color, insertbackground=fg_color)
entry_species.grid(row=2, column=1, sticky="ew", padx=15, pady=8)

label("Description:", 3, 0)
text_description = tk.Text(window, width=60, height=8, wrap="word", bg=highlight_color, fg=fg_color, insertbackground=fg_color, font=("Segoe UI", 10))
text_description.grid(row=3, column=1, sticky="nsew", padx=15, pady=8)

# --- Buttons ---
button_frame = tk.Frame(window, bg=bg_color)
button_frame.grid(row=4, column=1, sticky="w", padx=15, pady=8)

def styled_button(parent, text, command):
    btn = tk.Button(parent, text=text, command=command, bg=button_color, fg=fg_color, relief="flat", width=10, activebackground=highlight_color)
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
    btn.bind("<Leave>", lambda e: btn.config(bg=button_color))
    return btn

styled_button(button_frame, "Save", save_character).pack(side="left", padx=5)
styled_button(button_frame, "Update", update_character).pack(side="left", padx=5)
styled_button(button_frame, "Delete", delete_character).pack(side="left", padx=5)
styled_button(button_frame, "Clear", clear_fields).pack(side="left", padx=5)
styled_button(button_frame, "Export", export_characters).pack(side="left", padx=5)  # Export last

# --- Search and List Section ---
label("Search:", 5, 0)
entry_search = tk.Entry(window, width=60, bg=highlight_color, fg=fg_color, insertbackground=fg_color)
entry_search.grid(row=5, column=1, sticky="ew", padx=10, pady=5)

styled_button(window, "Search", search_characters).grid(row=6, column=1, sticky="e", padx=10, pady=5)

listbox_characters = tk.Listbox(window, width=80, height=15, bg=highlight_color, fg=fg_color, selectbackground=button_color)
listbox_characters.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
listbox_characters.bind("<<ListboxSelect>>", show_character)

scrollbar = tk.Scrollbar(window, orient="vertical", command=listbox_characters.yview)
scrollbar.grid(row=7, column=2, sticky="ns")
listbox_characters.config(yscrollcommand=scrollbar.set)

load_characters()

window.mainloop()
conn.close()
