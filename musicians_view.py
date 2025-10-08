# musicians_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QInputDialog
)
from api import get_musicians, add_musician, update_musician, remove_musician

class MusiciansView(QWidget):
    def __init__(self, role="guest"):
        super().__init__()
        self.role = role
        layout = QVBoxLayout()
        header = QHBoxLayout()
        header.addWidget(QLabel("Musicians"))
        header.addStretch()
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.clicked.connect(self.load_data)
        header.addWidget(self.btn_refresh)

        if self.role in ("employee", "admin"):
            self.btn_add = QPushButton("Добавить музыканта")
            self.btn_add.clicked.connect(self.add_musician_dialog)
            header.addWidget(self.btn_add)

        layout.addLayout(header)

        self.table = QTableWidget()
        # ID(hidden), Name, Type, About, Action
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Type", "About", "Действие"])
        self.table.setColumnHidden(0, True)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        try:
            musicians = get_musicians()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить музыкантов: {e}")
            musicians = []
        for row, m in enumerate(musicians):
            self.table.insertRow(row)
            mid = m.get("id")
            self.table.setItem(row, 0, QTableWidgetItem(str(mid)))
            self.table.setItem(row, 1, QTableWidgetItem(str(m.get("name", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(m.get("musician_type", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(m.get("about", ""))))
            if self.role in ("employee", "admin"):
                actions = QWidget()
                h = QHBoxLayout(); h.setContentsMargins(0,0,0,0)
                btn_edit = QPushButton("Редактировать")
                btn_edit.clicked.connect(lambda _, mid=mid: self.edit_musician_dialog(mid))
                btn_del = QPushButton("Удалить")
                btn_del.clicked.connect(lambda _, mid=mid: self.delete_musician(mid))
                h.addWidget(btn_edit); h.addWidget(btn_del)
                actions.setLayout(h)
                self.table.setCellWidget(row, 4, actions)
        self.table.resizeColumnsToContents()

    def add_musician_dialog(self):
        name, ok = QInputDialog.getText(self, "Добавить музыканта", "Name:")
        if not ok or not name.strip():
            return
        about, ok = QInputDialog.getText(self, "Добавить музыканта", "About:")
        if not ok:
            return
        musician_type, ok = QInputDialog.getInt(self, "Добавить музыканта", "Musician type (1=performer,2=composer,...):", 1, 1, 10, 1)
        if not ok:
            return
        payload = {"name": name.strip(), "about": about.strip(), "musician_type": musician_type}
        try:
            add_musician(payload)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def edit_musician_dialog(self, mid: int):
        musicians = get_musicians()
        m = next((x for x in musicians if x.get("id") == mid), None)
        if not m:
            QMessageBox.warning(self, "Ошибка", "Музыкант не найден")
            return
        name, ok = QInputDialog.getText(self, "Редактировать музыканта", "Name:", text=str(m.get("name", "")))
        if not ok:
            return
        about, ok = QInputDialog.getText(self, "Редактировать музыканта", "About:", text=str(m.get("about", "")))
        if not ok:
            return
        musician_type, ok = QInputDialog.getInt(self, "Редактировать музыканта", "Musician type:", int(m.get("musician_type", 1)), 1, 10, 1)
        if not ok:
            return
        payload = {"name": name.strip(), "about": about.strip(), "musician_type": musician_type}
        try:
            update_musician(mid, payload)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def delete_musician(self, mid: int):
        confirm = QMessageBox.question(self, "Удалить", "Удалить музыканта?")
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                remove_musician(mid)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
