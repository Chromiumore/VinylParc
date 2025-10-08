# records_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QInputDialog
)
from PySide6.QtCore import Qt
from api import get_records, add_record, update_record, remove_record

class RecordsView(QWidget):
    def __init__(self, role="guest"):
        super().__init__()
        self.role = role
        layout = QVBoxLayout()
        header = QHBoxLayout()
        header.addWidget(QLabel("Records (Каталог)"))
        header.addStretch()
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.clicked.connect(self.load_data)
        header.addWidget(self.btn_refresh)

        if self.role in ("employee", "admin"):
            self.btn_add = QPushButton("Добавить запись")
            self.btn_add.clicked.connect(self.add_record_dialog)
            header.addWidget(self.btn_add)

        layout.addLayout(header)

        self.table = QTableWidget()
        # columns: ID(hidden), Company, Retail price, Release date, Remaining, Actions
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Company", "Retail price", "Release date", "Remaining stock", "Действие"])
        self.table.setColumnHidden(0, True)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        try:
            records = get_records()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить записи: {e}")
            records = []
        for row, r in enumerate(records):
            self.table.insertRow(row)
            rid = r.get("id")
            self.table.setItem(row, 0, QTableWidgetItem(str(rid)))
            self.table.setItem(row, 1, QTableWidgetItem(str(r.get("company", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(r.get("retail_price", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(r.get("release_date", ""))))
            self.table.setItem(row, 4, QTableWidgetItem(str(r.get("remaining_stock", ""))))

            if self.role in ("employee", "admin"):
                actions = QWidget()
                h = QHBoxLayout()
                h.setContentsMargins(0, 0, 0, 0)
                btn_edit = QPushButton("Редактировать")
                btn_edit.clicked.connect(lambda _, rid=rid: self.edit_record_dialog(rid))
                h.addWidget(btn_edit)
                btn_delete = QPushButton("Удалить")
                btn_delete.clicked.connect(lambda _, rid=rid: self.delete_record(rid))
                h.addWidget(btn_delete)
                actions.setLayout(h)
                self.table.setCellWidget(row, 5, actions)

        self.table.resizeColumnsToContents()

    def add_record_dialog(self):
        company, ok = QInputDialog.getText(self, "Добавить запись", "Company:")
        if not ok or not company.strip():
            return
        wholesale_addr, ok = QInputDialog.getText(self, "Добавить запись", "Wholesale address:")
        if not ok:
            return
        retail_price, ok = QInputDialog.getInt(self, "Добавить запись", "Retail price:", 100, 0, 10_000_000, 1)
        if not ok:
            return
        wholesale_price, ok = QInputDialog.getInt(self, "Добавить запись", "Wholesale price:", 50, 0, 10_000_000, 1)
        if not ok:
            return
        release_date, ok = QInputDialog.getText(self, "Добавить запись", "Release date (YYYY-MM-DD):")
        if not ok:
            return
        current_sold, ok = QInputDialog.getInt(self, "Добавить запись", "Current year sold:", 0, 0, 1_000_000, 1)
        if not ok:
            return
        last_sold, ok = QInputDialog.getInt(self, "Добавить запись", "Last year sold:", 0, 0, 1_000_000, 1)
        if not ok:
            return
        remaining, ok = QInputDialog.getInt(self, "Добавить запись", "Remaining stock:", 0, 0, 1_000_000, 1)
        if not ok:
            return

        payload = {
            "company": company.strip(),
            "wholesale_company_address": wholesale_addr.strip(),
            "retail_price": float(retail_price),
            "wholesale_price": float(wholesale_price),
            "release_date": release_date.strip(),
            "current_year_sold": int(current_sold),
            "last_year_sold": int(last_sold),
            "remaining_stock": int(remaining),
            "performances_id": [],  # empty by default
        }
        try:
            add_record(payload)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def edit_record_dialog(self, record_id: int):
        records = get_records()
        rec = next((x for x in records if x.get("id") == record_id), None)
        if not rec:
            QMessageBox.warning(self, "Ошибка", "Запись не найдена")
            return
        company, ok = QInputDialog.getText(self, "Редактировать", "Company:", text=str(rec.get("company", "")))
        if not ok:
            return
        wholesale_addr, ok = QInputDialog.getText(self, "Редактировать", "Wholesale address:", text=str(rec.get("wholesale_company_address", "")))
        if not ok:
            return
        retail_price, ok = QInputDialog.getInt(self, "Редактировать", "Retail price:", int(rec.get("retail_price", 0)), 0, 10_000_000, 1)
        if not ok:
            return
        wholesale_price, ok = QInputDialog.getInt(self, "Редактировать", "Wholesale price:", int(rec.get("wholesale_price", 0)), 0, 10_000_000, 1)
        if not ok:
            return
        release_date, ok = QInputDialog.getText(self, "Редактировать", "Release date (YYYY-MM-DD):", text=str(rec.get("release_date", "")))
        if not ok:
            return
        current_sold, ok = QInputDialog.getInt(self, "Редактировать", "Current year sold:", int(rec.get("current_year_sold", 0)), 0, 1_000_000, 1)
        if not ok:
            return
        last_sold, ok = QInputDialog.getInt(self, "Редактировать", "Last year sold:", int(rec.get("last_year_sold", 0)), 0, 1_000_000, 1)
        if not ok:
            return
        remaining, ok = QInputDialog.getInt(self, "Редактировать", "Remaining stock:", int(rec.get("remaining_stock", 0)), 0, 1_000_000, 1)
        if not ok:
            return

        payload = {
            "company": company.strip(),
            "wholesale_company_address": wholesale_addr.strip(),
            "retail_price": float(retail_price),
            "wholesale_price": float(wholesale_price),
            "release_date": release_date.strip(),
            "current_year_sold": int(current_sold),
            "last_year_sold": int(last_sold),
            "remaining_stock": int(remaining),
            "performances_id": [p.get("id") for p in rec.get("performances", [])] if rec.get("performances") else [],
        }
        try:
            update_record(record_id, payload)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def delete_record(self, record_id: int):
        confirm = QMessageBox.question(self, "Удалить", "Удалить запись?")
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                remove_record(record_id)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
