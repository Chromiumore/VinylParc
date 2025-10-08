# performances_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QInputDialog
)
from api import get_performances, add_performance, update_performance, remove_performance

class PerformancesView(QWidget):
    def __init__(self, role="guest"):
        super().__init__()
        self.role = role
        layout = QVBoxLayout()
        header = QHBoxLayout()
        header.addWidget(QLabel("Performances"))
        header.addStretch()
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.clicked.connect(self.load_data)
        header.addWidget(self.btn_refresh)

        if self.role in ("employee", "admin"):
            self.btn_add = QPushButton("Добавить исполнение")
            self.btn_add.clicked.connect(self.add_performance_dialog)
            header.addWidget(self.btn_add)

        layout.addLayout(header)
        self.table = QTableWidget()
        # ID(hidden), Date, Composition ID, Ensemble ID, Action
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Composition ID", "Ensemble ID", "Действие"])
        self.table.setColumnHidden(0, True)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        try:
            perf = get_performances()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить исполнения: {e}")
            perf = []
        for row, p in enumerate(perf):
            self.table.insertRow(row)
            pid = p.get("id")
            self.table.setItem(row, 0, QTableWidgetItem(str(pid)))
            self.table.setItem(row, 1, QTableWidgetItem(str(p.get("performance_date",""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(p.get("composition_id",""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(p.get("ensemble_id",""))))
            if self.role in ("employee", "admin"):
                actions = QWidget(); h = QHBoxLayout(); h.setContentsMargins(0,0,0,0)
                btn_edit = QPushButton("Редактировать"); btn_edit.clicked.connect(lambda _, pid=pid: self.edit_performance_dialog(pid))
                btn_del = QPushButton("Удалить"); btn_del.clicked.connect(lambda _, pid=pid: self.delete_performance(pid))
                h.addWidget(btn_edit); h.addWidget(btn_del)
                actions.setLayout(h); self.table.setCellWidget(row, 4, actions)
        self.table.resizeColumnsToContents()

    def add_performance_dialog(self):
        perf_date, ok = QInputDialog.getText(self, "Добавить исполнение", "Date (YYYY-MM-DD):")
        if not ok or not perf_date.strip(): return
        comp_id, ok = QInputDialog.getInt(self, "Добавить исполнение", "Composition ID:", 1, 1, 1_000_000, 1)
        if not ok: return
        ensemble_id, ok = QInputDialog.getInt(self, "Добавить исполнение", "Ensemble ID:", 1, 1, 1_000_000, 1)
        if not ok: return
        payload = {"performance_date": perf_date.strip(), "composition_id": int(comp_id), "ensemble_id": int(ensemble_id)}
        try:
            add_performance(payload)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def edit_performance_dialog(self, pid: int):
        perfs = get_performances()
        p = next((x for x in perfs if x.get("id") == pid), None)
        if not p:
            QMessageBox.warning(self, "Ошибка", "Исполнение не найдено"); return
        perf_date, ok = QInputDialog.getText(self, "Редактировать", "Date (YYYY-MM-DD):", text=str(p.get("performance_date","")))
        if not ok: return
        comp_id, ok = QInputDialog.getInt(self, "Редактировать", "Composition ID:", int(p.get("composition_id",1)), 1, 1_000_000, 1)
        if not ok: return
        ensemble_id, ok = QInputDialog.getInt(self, "Редактировать", "Ensemble ID:", int(p.get("ensemble_id",1)), 1, 1_000_000, 1)
        if not ok: return
        payload = {"performance_date": perf_date.strip(), "composition_id": int(comp_id), "ensemble_id": int(ensemble_id)}
        try:
            update_performance(pid, payload)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def delete_performance(self, pid: int):
        confirm = QMessageBox.question(self, "Удалить", "Удалить исполнение?")
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                remove_performance(pid)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
