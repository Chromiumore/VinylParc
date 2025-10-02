# from PySide6.QtWidgets import QMainWindow, QTabWidget
# from catalog_view import CatalogView
# from sales_view import SalesView
# from users_view import UsersView

# class MainWindow(QMainWindow):
#     def __init__(self, role):
#         super().__init__()
#         self.setWindowTitle("VinylParc")
#         self.resize(900, 600)

#         tabs = QTabWidget()
#         tabs.addTab(CatalogView(), "Каталог")

#         if role in ("employee", "admin"):
#             tabs.addTab(SalesView(), "Продажи")

#         if role == "admin":
#             tabs.addTab(UsersView(), "Пользователи")

#         self.setCentralWidget(tabs)

from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from catalog_view import CatalogView
from users_view import UsersView
from api import logout

class MainWindow(QMainWindow):
    def __init__(self, role: str, username: str):
        super().__init__()
        self.role = role
        self.username = username
        self.setWindowTitle(f"VinylParc — {username} ({role})")
        self.resize(1000, 650)

        central = QWidget()
        main_layout = QVBoxLayout()
        header = QHBoxLayout()

        self.lbl_user = QLabel(f"Пользователь: <b>{username}</b> ({role})")
        header.addWidget(self.lbl_user)
        header.addStretch()

        # Logout button visible только если роль не гость
        if self.role != "guest":
            self.btn_logout = QPushButton("Выйти")
            self.btn_logout.clicked.connect(self.handle_logout)
            header.addWidget(self.btn_logout)

        main_layout.addLayout(header)

        self.tabs = QTabWidget()
        # Каталог всегда
        self.catalog_tab = CatalogView(role=self.role)
        self.tabs.addTab(self.catalog_tab, "Каталог")

        # Для сотрудников/админов каталог поддерживает CRUD — в CatalogView это учитывается по роли
        if self.role == "admin":
            # Таблица пользователей только для админа
            self.users_tab = UsersView()
            self.tabs.addTab(self.users_tab, "Пользователи")

        main_layout.addWidget(self.tabs)
        central.setLayout(main_layout)
        self.setCentralWidget(central)

    def handle_logout(self):
        logout()
        self.close()
