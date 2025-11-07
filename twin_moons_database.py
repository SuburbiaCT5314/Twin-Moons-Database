import tkinter as tk
from tkinter import messagebox
import sqlite3

# =============== DATABASE SETUP ===============

def connect_db():
    """Connect to SQLite database and create table if not exists."""
    conn = sqlite3.connect("characters.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        species TEXT,
        age INTEGER,
        role TEXT,
        description TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_character(name, species, age, role, description):
    """Insert a new character into the database."""
    conn = sqlite3.connect("characters.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO characters (name, species, age, role, description)
    VALUES (?, ?, ?, ?, ?)
    """, (name, species, age, role, description))
    conn.commit()
    conn.close()

def fetch_characters():
    """Retrieve all characters from the database."""
    conn = sqlite3.connect("characters.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters")
    rows = cursor.fetchall()
    conn.close()
    return rows


# =============== GUI SETUP ===============

root = tk.Tk()
root.title("Twin Moons Database")
root.geometry("600x600")

# Connect database when app starts
connect_db()


# =============== FUNCTIONS ===============

def load_characters():
    """Load all characters from the database into the listbox."""
    characters_listbox.delete(0, tk.END)
    rows = fetch_characters()
    for row in rows:
        # Format: ID - Name (Species, Age) - Role
        entry_text = f"{row[0]} - {row[1]} ({row[2]}, {row[3]}) - {row[4]}"
        characters_listbox.insert(tk.END, entry_text)

def add_character():
    """Take input and save to database."""
    name = name_entry.get().strip()
    species = species_entry.get().strip()
    age = age_entry.get().strip()
    role = role_entry.get().strip()
    description = desc_entry.get("1.0", tk.END).strip()

    if not name:
        messagebox.showwarning("Missing Data", "Character name is required!")
        return

    insert_character(name, species, age, role, description)
    messagebox.showinfo("Success", f"{name} added successfully!")
    clear_inputs()
    load_characters()

def clear_inputs():
    """Clear all text fields."""
    name_entry.delete(0, tk.END)
    species_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    role_entry.delete(0, tk.END)
    desc_entry.delete("1.0", tk.END)


# =============== GUI ELEMENTS ===============

tk.Label(root, text="Name:").pack()
name_entry = tk.Entry(root, width=40)
name_entry.pack()

tk.Label(root, text="Species:").pack()
species_entry = tk.Entry(root, width=40)
species_entry.pack()

tk.Label(root, text="Age:").pack()
age_entry = tk.Entry(root, width=40)
age_entry.pack()

tk.Label(root, text="Role:").pack()
role_entry = tk.Entry(root, width=40)
role_entry.pack()

tk.Label(root, text="Description:").pack()
desc_entry = tk.Text(root, height=4, width=40)
desc_entry.pack()

tk.Button(root, text="Add Character", command=add_character).pack(pady=10)

tk.Label(root, text="Character List:").pack()

characters_listbox = tk.Listbox(root, width=80, height=12)
characters_listbox.pack(pady=10)

# Load characters at startup
load_characters()

root.mainloop()
