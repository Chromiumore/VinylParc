# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget
# from api import get_users

# class UsersView(QWidget):
#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout()
#         self.list = QListWidget()
#         layout.addWidget(QLabel("Управление пользователями"))
#         layout.addWidget(self.list)
#         self.setLayout(layout)
#         self.load_data()

#     def load_data(self):
#         users = get_users()
#         for u in users:
#             self.list.addItem(f"{u['username']} ({u['role']})")

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QInputDialog, QMessageBox
from api import get_users, add_user, remove_user

class UsersView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        header = QHBoxLayout()
        header.addWidget(QLabel("Управление пользователями (администратор)"))
        header.addStretch()
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(self.add_user_dialog)
        header.addWidget(self.btn_refresh)
        header.addWidget(self.btn_add)
        layout.addLayout(header)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Логин", "Роль", "Действие"])
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        users = get_users()
        for row, u in enumerate(users):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(u.get("username", "")))
            self.table.setItem(row, 1, QTableWidgetItem(u.get("role", "")))
            btn = QPushButton("Удалить")
            btn.clicked.connect(lambda checked, username=u.get("username"): self.delete_user(username))
            self.table.setCellWidget(row, 2, btn)
        self.table.resizeColumnsToContents()

    def add_user_dialog(self):
        username, ok = QInputDialog.getText(self, "Добавить пользователя", "Логин:")
        if not ok or not username.strip():
            return
        password, ok = QInputDialog.getText(self, "Добавить пользователя", "Пароль (в демо хранится в открытом виде):")
        if not ok or not password:
            return
        role, ok = QInputDialog.getItem(self, "Добавить пользователя", "Роль:", ["employee", "admin"], 0, False)
        if not ok:
            return
        try:
            add_user(username.strip(), password, role)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def delete_user(self, username):
        if username == "admin":
            QMessageBox.warning(self, "Отказ", "Удаление admin запрещено в демо")
            return
        confirm = QMessageBox.question(self, "Удалить", f"Удалить пользователя {username}?")
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                remove_user(username)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
