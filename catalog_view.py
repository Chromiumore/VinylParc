# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget
# from api import get_catalog

# class CatalogView(QWidget):
#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout()
#         self.list = QListWidget()
#         layout.addWidget(QLabel("Каталог пластинок"))
#         layout.addWidget(self.list)
#         self.setLayout(layout)
#         self.load_data()

#     def load_data(self):
#         catalog = get_catalog()
#         for item in catalog:
#             self.list.addItem(f"{item['artist']} - {item['album']} ({item['price']} руб.)")

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox, QInputDialog
from PySide6.QtCore import Qt
from api import get_catalog, add_product, update_product, remove_product

class CatalogView(QWidget):
    def __init__(self, role="guest"):
        super().__init__()
        self.role = role
        layout = QVBoxLayout()
        header = QHBoxLayout()
        header.addWidget(QLabel("Каталог"))
        header.addStretch()
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.clicked.connect(self.load_data)
        header.addWidget(self.btn_refresh)

        # Add button for employee/admin
        if self.role in ("employee", "admin"):
            self.btn_add = QPushButton("Добавить товар")
            self.btn_add.clicked.connect(self.add_product_dialog)
            header.addWidget(self.btn_add)

        layout.addLayout(header)

        # Configure table: if guest -> no action column; else -> action column
        if self.role == "guest":
            self.table = QTableWidget()
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(["ID", "Исполнитель", "Альбом", "Цена", "Остаток"])
            self.table.setColumnHidden(0, True)
        else:
            self.table = QTableWidget()
            self.table.setColumnCount(6)
            self.table.setHorizontalHeaderLabels(["ID", "Исполнитель", "Альбом", "Цена", "Остаток", "Действие"])
            self.table.setColumnHidden(0, True)

        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        try:
            catalog = get_catalog()
        except Exception:
            catalog = []
        for row, item in enumerate(catalog):
            self.table.insertRow(row)
            pid = item.get("id", "")
            self.table.setItem(row, 0, QTableWidgetItem(str(pid)))
            self.table.setItem(row, 1, QTableWidgetItem(item.get("artist", "")))
            self.table.setItem(row, 2, QTableWidgetItem(item.get("album", "")))
            self.table.setItem(row, 3, QTableWidgetItem(str(item.get("price", ""))))
            self.table.setItem(row, 4, QTableWidgetItem(str(item.get("stock", 0))))
            if self.role in ("employee", "admin"):
                actions = QWidget()
                h = QHBoxLayout()
                h.setContentsMargins(0, 0, 0, 0)
                btn_edit = QPushButton("Редактировать")
                btn_edit.clicked.connect(lambda checked, pid=pid: self.edit_product_dialog(pid))
                h.addWidget(btn_edit)
                btn_delete = QPushButton("Удалить")
                btn_delete.clicked.connect(lambda checked, pid=pid: self.delete_product(pid))
                h.addWidget(btn_delete)
                actions.setLayout(h)
                self.table.setCellWidget(row, 5, actions)
        self.table.resizeColumnsToContents()

    def add_product_dialog(self):
        artist, ok = QInputDialog.getText(self, "Добавить товар", "Исполнитель:")
        if not ok or not artist.strip():
            return
        album, ok = QInputDialog.getText(self, "Добавить товар", "Альбом:")
        if not ok or not album.strip():
            return
        price, ok = QInputDialog.getInt(self, "Добавить товар", "Цена (руб):", 100, 0, 1000000, 1)
        if not ok:
            return
        stock, ok = QInputDialog.getInt(self, "Добавить товар", "Остаток:", 1, 0, 1000000, 1)
        if not ok:
            return
        try:
            add_product(artist.strip(), album.strip(), price, stock)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def edit_product_dialog(self, product_id):
        catalog = get_catalog()
        prod = next((p for p in catalog if p.get("id") == product_id), None)
        if not prod:
            QMessageBox.warning(self, "Ошибка", "Товар не найден")
            return
        artist, ok = QInputDialog.getText(self, "Редактировать", "Исполнитель:", text=prod.get("artist", ""))
        if not ok:
            return
        album, ok = QInputDialog.getText(self, "Редактировать", "Альбом:", text=prod.get("album", ""))
        if not ok:
            return
        price, ok = QInputDialog.getInt(self, "Редактировать", "Цена (руб):", prod.get("price", 100), 0, 1000000, 1)
        if not ok:
            return
        stock, ok = QInputDialog.getInt(self, "Редактировать", "Остаток:", prod.get("stock", 0), 0, 1000000, 1)
        if not ok:
            return
        try:
            update_product(product_id, artist.strip(), album.strip(), price, stock)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def delete_product(self, product_id):
        confirm = QMessageBox.question(self, "Удалить", "Удалить товар?")
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                remove_product(product_id)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
