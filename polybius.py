from tkinter import *
import hashlib
import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)
        self.sql = self.db.cursor()
        self.create_table()

    def create_table(self):
        self.sql.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.db.commit()

    def register_user(self, username, password):
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        self.sql.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        self.db.commit()

    def check_user_exists(self, username):
        self.sql.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.sql.fetchone() is not None

    def login_user(self, username, password):
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        self.sql.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        return self.sql.fetchone() is not None

class PolybiusCipher:
    def __init__(self):
        self.polybius_table_ru = {
            'А': '11', 'Б': '12', 'В': '13', 'Г': '14', 'Д': '15',
            'Е': '21', 'Ё': '21', 'Ж': '22', 'З': '23', 'И': '24',
            'Й': '24', 'К': '25', 'Л': '31', 'М': '32', 'Н': '33',
            'О': '34', 'П': '35', 'Р': '41', 'С': '42', 'Т': '43',
            'У': '44', 'Ф': '45', 'Х': '51', 'Ц': '52', 'Ч': '53',
            'Ш': '54', 'Щ': '55', 'Ъ': '61', 'Ы': '62', 'Ь': '63',
            'Э': '64', 'Ю': '65', 'Я': '66', ' ': '00'
        }

        self.polybius_table_en = {
            'A': '11', 'B': '12', 'C': '13', 'D': '14', 'E': '15',
            'F': '21', 'G': '22', 'H': '23', 'I': '24', 'J': '24',
            'K': '25', 'L': '31', 'M': '32', 'N': '33', 'O': '34',
            'P': '35', 'Q': '41', 'R': '42', 'S': '43', 'T': '44',
            'U': '45', 'V': '51', 'W': '52', 'X': '53', 'Y': '54',
            'Z': '55', ' ': '00'
        }

    def polybius_cipher(self, text, table):
        encrypted_text = ''
        for char in text.upper():
            if char in table:
                encrypted_text += table[char]
        return encrypted_text

    def polybius_decipher(self, text, table):
        deciphered_text = ''
        for i in range(0, len(text), 2):
            pair = text[i:i + 2]
            for key, value in table.items():
                if value == pair:
                    deciphered_text += key
                    break
        return deciphered_text

class TkinterUI:
    def __init__(self, db_manager, cipher_manager):
        self.db_manager = db_manager
        self.cipher_manager = cipher_manager
        self.login_window = Tk()
        self.login_window.title("Вход")
        self.create_login_interface()

    def create_login_interface(self):
        Label(self.login_window, text="Регистрация").grid(row=0, column=0, columnspan=2)
        Label(self.login_window, text="Логин").grid(row=1, column=0)
        Label(self.login_window, text="Пароль").grid(row=2, column=0)
        self.reg_username = Entry(self.login_window)
        self.reg_password = Entry(self.login_window, show="*")
        self.reg_username.grid(row=1, column=1)
        self.reg_password.grid(row=2, column=1)
        Button(self.login_window, text="Регистрация", command=self.register_user).grid(row=3, column=0, columnspan=2)

        Label(self.login_window, text="Вход").grid(row=4, column=0, columnspan=2)
        Label(self.login_window, text="Логин").grid(row=5, column=0)
        Label(self.login_window, text="Пароль").grid(row=6, column=0)
        self.login_username = Entry(self.login_window)
        self.login_password = Entry(self.login_window, show="*")
        self.login_username.grid(row=5, column=1)
        self.login_password.grid(row=6, column=1)
        Button(self.login_window, text="Вход", command=self.handle_login).grid(row=7, column=0, columnspan=2)

        self.registration_status_label = Label(self.login_window, text="")
        self.registration_status_label.grid(row=4, column=0, columnspan=2)

        self.login_status_label = Label(self.login_window, text="")
        self.login_status_label.grid(row=8, column=0, columnspan=2)

        self.login_window.mainloop()

    def register_user(self):
        username = self.reg_username.get()
        password = self.reg_password.get()
        if not self.db_manager.check_user_exists(username):
            self.db_manager.register_user(username, password)
            self.registration_status_label.config(text="Регистрация успешна")
        else:
            self.registration_status_label.config(text="Пользователь уже существует")

    def handle_login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        if self.db_manager.login_user(username, password):
            self.login_window.destroy()
            self.open_polybius_cipher()

    def open_polybius_cipher(self):

        def polybius_cipher(text, table):
            encrypted_text = ''
            for char in text.upper():
                if char in table:
                    encrypted_text += table[char]
            return encrypted_text
        
        def polybius_decipher(text, table):
            deciphered_text = ''
            for i in range(0, len(text), 2):
                pair = text[i:i + 2]
                for key, value in table.items():
                    if value == pair:
                        deciphered_text += key
                        break
            return deciphered_text

        def encrypt_text():
            language = language_var.get()
            if language == "русский":
                table = self.cipher_manager.polybius_table_ru
            else:
                table = self.cipher_manager.polybius_table_en
            text = input_text.get("1.0", END).strip()
            encrypted_text = self.cipher_manager.polybius_cipher(text, table)
            output_text.delete("1.0", END)
            output_text.insert(END, encrypted_text)

        def decrypt_text():
            language = language_var.get()
            if language == "русский":
                table = self.cipher_manager.polybius_table_ru
            else:
                table = self.cipher_manager.polybius_table_en
            text = input_text.get("1.0", END).strip()
            decrypted_text = self.cipher_manager.polybius_decipher(text, table)
            output_text.delete("1.0", END)
            output_text.insert(END, decrypted_text)

        # Создание окна
        window = Tk()
        window.title("Шифр Полибия")

        # Выбор языка
        language_var = StringVar(window)
        language_var.set("русский")
        language_option = OptionMenu(window, language_var, "русский", "английский")
        language_option.pack()

        # Поле для ввода текста
        input_label = Label(window, text="Введите текст:")
        input_label.pack()
        input_text = Text(window, height=5, width=40)
        input_text.pack()

        # Кнопки для шифрования и дешифрования
        encrypt_button = Button(window, text="Зашифровать", command=encrypt_text)
        encrypt_button.pack()
        decrypt_button = Button(window, text="Расшифровать", command=decrypt_text)
        decrypt_button.pack()

        # Поле для вывода результата
        output_label = Label(window, text="Результат:")
        output_label.pack()
        output_text = Text(window, height=5, width=40)
        output_text.pack()

if __name__ == "__main__":
    db_manager = DatabaseManager("users.db")
    cipher_manager = PolybiusCipher()
    ui = TkinterUI(db_manager, cipher_manager)
