# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
# from api import login, set_token
# from main_window import MainWindow

# class LoginWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("VinylParc - Авторизация")

#         layout = QVBoxLayout()
#         self.username = QLineEdit()
#         self.username.setPlaceholderText("Логин")
#         self.password = QLineEdit()
#         self.password.setPlaceholderText("Пароль")
#         self.password.setEchoMode(QLineEdit.Password)

#         self.status = QLabel("")
#         btn = QPushButton("Войти")
#         btn.clicked.connect(self.handle_login)

#         layout.addWidget(self.username)
#         layout.addWidget(self.password)
#         layout.addWidget(btn)
#         layout.addWidget(self.status)
#         self.setLayout(layout)

#     def handle_login(self):
#         data, code = login(self.username.text(), self.password.text())
#         if code == 200:
#             token = data["access_token"]
#             set_token(token)
#             self.status.setText("Успешный вход!")
#             self.main = MainWindow(data["role"])  # роль приходит с сервера
#             self.main.show()
#             self.close()
#         else:
#             self.status.setText("Ошибка входа")

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QComboBox
from PySide6.QtCore import Qt
from api import login, load_local_profile, set_base_url, set_online
from main_window import MainWindow

class LoginWindow(QWidget):
    def __init__(self, start_profile=None):
        super().__init__()
        self.setWindowTitle("VinylParc — Вход / Просмотр каталога")
        self.resize(480, 240)
        layout = QVBoxLayout()

        self.info = QLabel("Добро пожаловать в VinylParc")
        self.info.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info)

        # API config
        cfg = QHBoxLayout()
        cfg.addWidget(QLabel("API:"))
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("http://server:5000/api")
        cfg.addWidget(self.api_input)
        self.btn_set_api = QPushButton("Применить")
        self.btn_set_api.clicked.connect(self.apply_api)
        cfg.addWidget(self.btn_set_api)
        layout.addLayout(cfg)

        # Login fields
        self.username = QLineEdit()
        self.username.setPlaceholderText("Логин (сотрудник / админ)")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Пароль")
        self.password.setEchoMode(QLineEdit.Password)

        # Quick dev logins (only employee/admin)
        quick_layout = QHBoxLayout()
        quick_layout.addWidget(QLabel("Быстрый вход:"))
        self.quick = QComboBox()
        self.quick.addItems(["--", "employee1", "admin"])
        quick_layout.addWidget(self.quick)
        layout.addLayout(quick_layout)

        btns = QHBoxLayout()
        self.btn_login = QPushButton("Войти")
        self.btn_login.clicked.connect(self.handle_login)
        self.btn_guest = QPushButton("Просмотреть каталог без авторизации")
        self.btn_guest.clicked.connect(self.continue_as_guest)
        btns.addWidget(self.btn_login)
        btns.addWidget(self.btn_guest)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addLayout(btns)

        # quick login button
        self.btn_quick = QPushButton("Быстрый вход (выбранный профиль)")
        self.btn_quick.clicked.connect(self.handle_quick)
        layout.addWidget(self.btn_quick)

        self.status = QLabel("")
        layout.addWidget(self.status)
        self.setLayout(layout)

        if start_profile:
            try:
                self.username.setText(start_profile.get("username", ""))
                self.status.setText(f"Найден локальный профиль: {start_profile.get('username')}")
            except Exception:
                pass

    def apply_api(self):
        url = self.api_input.text().strip()
        if not url:
            self.status.setText("Введите URL API")
            return
        set_base_url(url)
        set_online(True)
        self.status.setText(f"API установлен: {url}")

    def handle_login(self):
        u = self.username.text().strip()
        p = self.password.text().strip()
        if not u or not p:
            self.status.setText("Введите логин и пароль")
            return
        data, code = login(u, p)
        if code in (200, 201):
            role = data.get("role", "employee")
            self.open_main(role=role, username=data.get("username", u))
        else:
            msg = data.get("message") if isinstance(data, dict) else str(data)
            self.status.setText(f"Ошибка входа: {msg} (код {code})")

    def handle_quick(self):
        chosen = self.quick.currentText()
        if chosen == "--":
            self.status.setText("Выберите профиль")
            return
        # quick login with default password 'pass' (offline dev)
        data, code = login(chosen, "pass")
        if code in (200, 201):
            self.open_main(role=data.get("role", "employee"), username=data.get("username", chosen))
        else:
            self.status.setText("Не удалось выполнить быстрый вход")

    def continue_as_guest(self):
        # Открыть главное окно в режиме гостя (без авторизации)
        self.open_main(role="guest", username="Гость")

    def open_main(self, role: str, username: str):
        self.main = MainWindow(role=role, username=username)
        self.main.show()
        self.close()

