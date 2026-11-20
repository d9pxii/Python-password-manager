import customtkinter as ctk
import func
from PIL import Image
import os


class PasswordManagerApp():
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("700x490")
        self.root.title("Менеджер паролей")

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        current_dir = os.path.dirname(os.path.abspath(__file__))

        int_path = os.path.join(current_dir, "img", "int_img.png")
        apps_path = os.path.join(current_dir, "img", "apps_img.png")
        pers_path = os.path.join(current_dir, "img", "pers_img.png")
        notes_path = os.path.join(current_dir, "img", "notes_img.png")

        int_icon = ctk.CTkImage(light_image=Image.open(int_path), dark_image=Image.open(int_path), size=(20, 20))
        apps_icon = ctk.CTkImage(light_image=Image.open(apps_path), dark_image=Image.open(apps_path), size=(20, 20))
        pers_icon = ctk.CTkImage(light_image=Image.open(pers_path), dark_image=Image.open(pers_path), size=(20, 20))
        notes_icon = ctk.CTkImage(light_image=Image.open(notes_path), dark_image=Image.open(notes_path), size=(20, 20))

        self.info_lbl = ctk.CTkLabel(
            master=self.root,
            text="Менеджер паролей",
            font=("Segoe UI", 22, "bold")
        )
        self.info_lbl.grid(row=0, column=0, columnspan=2, pady=3, padx=5, sticky="w")

        self.sep = ctk.CTkFrame(
            master=self.root,
            height=2,
            width=800,
            fg_color="#383838",
            corner_radius=0
        )
        self.sep.grid(row=1, column=0, columnspan=2, sticky="ew", padx=0, pady=5)

        self.btn_frame = ctk.CTkFrame(
            master=self.root,
            fg_color="transparent"
        )
        self.btn_frame.grid(row=2, column=0, pady=5, sticky="nw")

        self.content_frame = ctk.CTkFrame(
            master=self.root,
            fg_color="#2E2D2D",
        )
        self.content_frame.grid(row=2, column=1, pady=5, padx=5, sticky="nsew")

        self.pers_btn = ctk.CTkButton(
            master=self.btn_frame,
            text="Личные данные",
            fg_color="#383838",
            hover_color="#464646",
            image=pers_icon,
            font=("Segoe UI", 16, "bold"),
            command=lambda: self.start_page("Личные данные", "Введите тип данных: ", "Введите логин: ", "Введите пин-код/пароль/код: ", "personal", "Личные данные"),
            width=190,
            anchor="w"
        )
        self.pers_btn.grid(row=0, column=0, pady=3, padx=3, sticky="w")

        self.int_btn = ctk.CTkButton(
            master=self.btn_frame,
            text="Интернет",
            fg_color="#383838",
            hover_color="#464646",
            image=int_icon,
            font=("Segoe UI", 16, "bold"),
            command=lambda: self.start_page("Интернет", "Введите сайт или сервис: ", "Введите логин: ", "Введите пароль: ", "internet", "Интернет"),
            width=190,
            anchor="w"
        )
        self.int_btn.grid(row=1, column=0, pady=3, padx=3, sticky="w")

        self.apps_btn = ctk.CTkButton(
            master=self.btn_frame,
            text="Приложения",
            fg_color="#383838",
            hover_color="#464646",
            image=apps_icon,
            font=("Segoe UI", 16, "bold"),
            command=lambda: self.start_page("Приложения", "Введите приложение/программу: ", "Введите логин: ", "Введите пароль: ", "apps", "Приложения и программы"),
            width=190,
            anchor="w"
        )
        self.apps_btn.grid(row=2, column=0, pady=3, padx=3, sticky="w")

        self.notes_btn = ctk.CTkButton(
            master=self.btn_frame,
            text="Заметки",
            fg_color="#383838",
            hover_color="#464646",
            image=notes_icon,
            font=("Segoe UI", 16, "bold"),
            command=lambda: self.start_notes_page("Заметки", "Введите название заметки: ", "Введите содержание заметки: ", None, "Заметки"),
            width=190,
            anchor="w"
        )
        self.notes_btn.grid(row=3, column=0, pady=3, padx=3, sticky="w")

        self.start_page("Интернет", "Введите сайт или сервис: ", "Введите логин: ", "Введите пароль: ", "internet", "Интернет")

        self.root.mainloop()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def start_page(self, header_text, name_ph, login_ph, pass_ph, category, title_text):
        self.clear_content()
        self.page_header_lbl = ctk.CTkLabel(
            master=self.content_frame,
            text=header_text,
            font=("Segoe UI", 20, "bold")
        )
        self.page_header_lbl.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        self.name_entry = ctk.CTkEntry(
            master=self.content_frame,
            placeholder_text=name_ph,
            width=300,
            font=("Segoe UI", 16)
        )
        self.name_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.login_entry = ctk.CTkEntry(
            master=self.content_frame,
            placeholder_text=login_ph,
            width=300,
            font=("Segoe UI", 16)
        )
        self.login_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.password_entry = ctk.CTkEntry(
            master=self.content_frame,
            placeholder_text=pass_ph,
            width=300,
            font=("Segoe UI", 16)
        )
        self.password_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.add_btn = ctk.CTkButton(
            master=self.content_frame,
            text="Добавить данные",
            fg_color="#424242",
            hover_color="#464646",
            font=("Segoe UI", 16, "bold"),
            command=lambda: func.add_account(category, self.name_entry, self.login_entry, self.password_entry)
        )
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=5, padx=10, sticky="w")

        self.show_data_btn = ctk.CTkButton(
            master=self.content_frame,
            text="Показать данные",
            fg_color="#424242",
            hover_color="#464646",
            command=lambda: func.open_data_window(self.root, "accounts", category, title_text),
            font=("Segoe UI", 16, "bold"),
        )
        self.show_data_btn.grid(row=5, column=0, columnspan=2, pady=5, padx=10, sticky="w")

    def start_notes_page(self, header_text, name_ph, content_ph, category, title_text):
        self.clear_content()
        self.notes_header_lbl = ctk.CTkLabel(
            master=self.content_frame,
            text=header_text,
            font=("Segoe UI", 20, "bold")
        )
        self.notes_header_lbl.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        self.notes_name_entry = ctk.CTkEntry(
            master=self.content_frame,
            placeholder_text=name_ph,
            width=300,
            font=("Segoe UI", 16)
        )
        self.notes_name_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.notes_content_entry = ctk.CTkEntry(
            master=self.content_frame,
            placeholder_text=content_ph,
            width=300,
            font=("Segoe UI", 16)
        )
        self.notes_content_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.add_note_btn = ctk.CTkButton(
            master=self.content_frame,
            text="Добавить данные",
            fg_color="#424242",
            hover_color="#464646",
            font=("Segoe UI", 16, "bold"),
            command=lambda: func.add_note(self.notes_name_entry, self.notes_content_entry)
        )
        self.add_note_btn.grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky="w")

        self.show_notes_data_btn = ctk.CTkButton(
            master=self.content_frame,
            text="Показать заметки",
            fg_color="#424242",
            hover_color="#464646",
            command=lambda: func.open_data_window(self.root, "notes", category, title_text),
            font=("Segoe UI", 16, "bold"),
        )
        self.show_notes_data_btn.grid(row=4, column=0, columnspan=2, pady=5, padx=10, sticky="w")

if __name__ == "__main__":
    PasswordManagerApp()
