# compositions_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QInputDialog
)
from api import get_compositions, add_composition, update_composition, remove_composition

class CompositionsView(QWidget):
    def __init__(self, role="guest"):
        super().__init__()
        self.role = role
        layout = QVBoxLayout()
        header = QHBoxLayout()
        header.addWidget(QLabel("Compositions"))
        header.addStretch()
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.clicked.connect(self.load_data)
        header.addWidget(self.btn_refresh)

        if self.role in ("employee", "admin"):
            self.btn_add = QPushButton("Добавить произведение")
            self.btn_add.clicked.connect(self.add_composition_dialog)
            header.addWidget(self.btn_add)

        layout.addLayout(header)
        self.table = QTableWidget()
        # ID(hidden), Name, About, Action
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "About", "Действие"])
        self.table.setColumnHidden(0, True)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        try:
            comps = get_compositions()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить произведения: {e}")
            comps = []
        for row, c in enumerate(comps):
            self.table.insertRow(row)
            cid = c.get("id")
            self.table.setItem(row, 0, QTableWidgetItem(str(cid)))
            self.table.setItem(row, 1, QTableWidgetItem(str(c.get("name",""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(c.get("about",""))))
            if self.role in ("employee", "admin"):
                actions = QWidget(); h = QHBoxLayout(); h.setContentsMargins(0,0,0,0)
                btn_edit = QPushButton("Редактировать"); btn_edit.clicked.connect(lambda _, cid=cid: self.edit_composition_dialog(cid))
                btn_del = QPushButton("Удалить"); btn_del.clicked.connect(lambda _, cid=cid: self.delete_composition(cid))
                h.addWidget(btn_edit); h.addWidget(btn_del)
                actions.setLayout(h); self.table.setCellWidget(row, 3, actions)
        self.table.resizeColumnsToContents()

    def add_composition_dialog(self):
        name, ok = QInputDialog.getText(self, "Добавить произведение", "Name:")
        if not ok or not name.strip(): return
        about, ok = QInputDialog.getText(self, "Добавить произведение", "About:")
        if not ok: return
        payload = {"name": name.strip(), "about": about.strip()}
        try:
            add_composition(payload)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def edit_composition_dialog(self, cid: int):
        comps = get_compositions()
        c = next((x for x in comps if x.get("id") == cid), None)
        if not c:
            QMessageBox.warning(self, "Ошибка", "Произведение не найдено"); return
        name, ok = QInputDialog.getText(self, "Редактировать", "Name:", text=str(c.get("name","")))
        if not ok: return
        about, ok = QInputDialog.getText(self, "Редактировать", "About:", text=str(c.get("about","")))
        if not ok: return
        payload = {"name": name.strip(), "about": about.strip()}
        try:
            update_composition(cid, payload)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def delete_composition(self, cid: int):
        confirm = QMessageBox.question(self, "Удалить", "Удалить произведение?")
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                remove_composition(cid)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
