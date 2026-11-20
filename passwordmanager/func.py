import sqlite3
import customtkinter as ctk
import os
from tkinter import messagebox
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "passdb.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        login TEXT,
        password TEXT NOT NULL
    )
""")
conn.commit()

cur.execute("""
    CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        date TEXT NOT NULL
    )
""")
conn.commit()
    
def add_account(category, title_entry, login_entry, password_entry):
    title = title_entry.get()
    login = login_entry.get()
    password = password_entry.get().strip()

    if not title or not login or not password:
        messagebox.showerror("Ошибка", "Все поля ввода обязательны для ввода!")
        return

    cur.execute(
        "INSERT INTO accounts (category, title, login, password) VALUES (?, ?, ?, ?)",
        (category, title, login, password)    
    )
    conn.commit()

    title_entry.delete(0, "end")
    login_entry.delete(0, "end")
    password_entry.delete(0, "end")
    messagebox.showinfo("Успех", "Данные сохранены!")

def show_accounts_data(category):
    cur.execute("SELECT id, title, login, password FROM accounts WHERE category = ?", (category,))
    return cur.fetchall()

def add_note(title_entry, content_entry):
    title = title_entry.get()
    content = content_entry.get()
    date = datetime.now().strftime("%y-%m-%d %H:%M:%S")

    if not title or not content or not date:
        messagebox.showerror("Ошибка", "Все поля ввода обязательны для ввода!")
        return

    cur.execute(
        "INSERT INTO notes (title, content, date) VALUES (?, ?, ?)",
        (title, content, date)
    )
    conn.commit()

    title_entry.delete(0, "end")
    content_entry.delete(0, "end")
    messagebox.showinfo("Успех", "Данные сохранены!")

def show_notes():
    cur.execute("SELECT id, title, content, date FROM notes")
    return cur.fetchall()

def delete_acc(acc_id, frame, parent):
    answer = messagebox.askyesno("Подтверждение", "Вы точно хотите удалить эту запись?", parent=parent)
    if answer:
        cur.execute("DELETE FROM accounts WHERE id = ?", (acc_id,))
        conn.commit()
        frame.destroy()
    else:
        return

def delete_note(note_id, frame, parent):
    answer = messagebox.askyesno("Подтверждение", "Вы точно хотите удалить эту запись?", parent=parent)
    if answer:
        cur.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        frame.destroy()
    else:
        return

def open_data_window(parent, mode, category, title_text):
    data_root = ctk.CTkToplevel(parent)
    data_root.geometry("500x450")
    data_root.title(title_text)
    data_root.attributes("-topmost", True)

    header = ctk.CTkLabel(
        master=data_root,
        text=title_text,
        font=("Segoe UI", 20, "bold")
    )

    header.pack(pady=5, padx=5)

    scroll_frame = ctk.CTkScrollableFrame(data_root, width=460, height=360, fg_color="#2E2D2D")
    scroll_frame.pack(pady=5, padx=5, fill="both", expand=True)

    if mode == "accounts":
        rows = show_accounts_data(category)
    elif mode == "notes":
        rows = show_notes()

    if not rows:
        no_data_lbl = ctk.CTkLabel(
            master=scroll_frame,
            text="Пока ничего нет",
            font=("Segoe UI", 16, "bold")
        )
        no_data_lbl.pack(pady=10, padx=5)
        return

    for row in rows:
        content_frame = ctk.CTkFrame(
            master=scroll_frame,
            fg_color="#2E2D2D",
        )
        content_frame.pack(fill="x", pady=5, padx=5)

        if mode == "accounts":
            id, title, login, password = row
            info_text = f"📌 {title}\nЛогин: {login}   |   Пароль: {password}"

            lbl = ctk.CTkLabel(
                master=content_frame,
                text=info_text,
                font=("Segoe UI", 16),
                justify="left",
                anchor="w",
                wraplength=270
            )
            lbl.pack(side="left", padx=12, pady=8, fill="x", expand=True)

            delete_btn = ctk.CTkButton(
                master=content_frame,
                text="Удалить аккаунт",
                font=("Segoe UI", 16),
                fg_color="#424242",
                hover_color="#464646",
                command=lambda cur_id=id, frame=content_frame: delete_acc(cur_id, frame, data_root)
            )
            delete_btn.pack(side="right", padx=10, pady=8)

        elif mode == "notes":
            id, title, content, date = row
            info_text = f"📝 {title}  ({date})\n{content}"

            lbl = ctk.CTkLabel(
                master=content_frame,
                text=info_text,
                font=("Segoe UI", 16),
                justify="left",
                anchor="w",
                wraplength=270
            )
            lbl.pack(side="left", padx=12, pady=8, fill="x", expand=True)

            delete_btn = ctk.CTkButton(
                master=content_frame,
                text="Удалить заметку",
                font=("Segoe UI", 16),
                fg_color="#424242",
                hover_color="#464646",
                command=lambda cur_id=id, frame=content_frame: delete_note(cur_id, frame, data_root)
            )
            delete_btn.pack(side="right", padx=10, pady=8)