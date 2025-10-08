# ensembles_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QInputDialog
)
from api import get_ensembles, add_ensemble, update_ensemble, remove_ensemble, get_musicians

class EnsemblesView(QWidget):
    def __init__(self, role="guest"):
        super().__init__()
        self.role = role
        layout = QVBoxLayout()
        header = QHBoxLayout()
        header.addWidget(QLabel("Ensembles"))
        header.addStretch()
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.clicked.connect(self.load_data)
        header.addWidget(self.btn_refresh)

        if self.role in ("employee", "admin"):
            self.btn_add = QPushButton("Добавить ансамбль")
            self.btn_add.clicked.connect(self.add_ensemble_dialog)
            header.addWidget(self.btn_add)

        layout.addLayout(header)

        self.table = QTableWidget()
        # ID(hidden), Name, Type, About, #Musicians, Action
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Type", "About", "Musicians", "Действие"])
        self.table.setColumnHidden(0, True)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        try:
            ensembles = get_ensembles()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить ансамбли: {e}")
            ensembles = []
        for row, e in enumerate(ensembles):
            self.table.insertRow(row)
            eid = e.get("id")
            self.table.setItem(row, 0, QTableWidgetItem(str(eid)))
            self.table.setItem(row, 1, QTableWidgetItem(str(e.get("name", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(e.get("ensemble_type", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(e.get("about", ""))))
            musicians = e.get("musicians") or []
            # musicians may be list of objects or ids
            if musicians and isinstance(musicians[0], dict):
                mus_count = len(musicians)
                mus_display = ", ".join([m.get("name","") for m in musicians])
            else:
                mus_count = len(musicians)
                mus_display = ", ".join([str(x) for x in musicians])
            self.table.setItem(row, 4, QTableWidgetItem(f"{mus_count} ({mus_display})"))

            if self.role in ("employee", "admin"):
                actions = QWidget()
                h = QHBoxLayout(); h.setContentsMargins(0,0,0,0)
                btn_edit = QPushButton("Редактировать")
                btn_edit.clicked.connect(lambda _, eid=eid: self.edit_ensemble_dialog(eid))
                btn_del = QPushButton("Удалить")
                btn_del.clicked.connect(lambda _, eid=eid: self.delete_ensemble(eid))
                h.addWidget(btn_edit); h.addWidget(btn_del)
                actions.setLayout(h)
                self.table.setCellWidget(row, 5, actions)
        self.table.resizeColumnsToContents()

    def add_ensemble_dialog(self):
        name, ok = QInputDialog.getText(self, "Добавить ансамбль", "Name:")
        if not ok or not name.strip():
            return
        about, ok = QInputDialog.getText(self, "Добавить ансамбль", "About:")
        if not ok:
            return
        ensemble_type, ok = QInputDialog.getInt(self, "Добавить ансамбль", "Ensemble type (1=orchestra,2=quartet...):", 1, 1, 10, 1)
        if not ok:
            return
        # ask for musician IDs comma-separated
        mus_ids_text, ok = QInputDialog.getText(self, "Добавить ансамбль", "Musician IDs (comma-separated):")
        if not ok:
            return
        mus_ids = [int(x.strip()) for x in mus_ids_text.split(",") if x.strip().isdigit()] if mus_ids_text.strip() else []
        payload = {"name": name.strip(), "about": about.strip(), "ensemble_type": ensemble_type, "musicians_id": mus_ids}
        try:
            add_ensemble(payload)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def edit_ensemble_dialog(self, eid: int):
        ensembles = get_ensembles()
        e = next((x for x in ensembles if x.get("id") == eid), None)
        if not e:
            QMessageBox.warning(self, "Ошибка", "Ансамбль не найден")
            return
        name, ok = QInputDialog.getText(self, "Редактировать ансамбль", "Name:", text=str(e.get("name","")))
        if not ok:
            return
        about, ok = QInputDialog.getText(self, "Редактировать ансамбль", "About:", text=str(e.get("about","")))
        if not ok:
            return
        ensemble_type, ok = QInputDialog.getInt(self, "Редактировать ансамбль", "Ensemble type:", int(e.get("ensemble_type",1)), 1, 10, 1)
        if not ok:
            return
        # current musician ids
        cur_mus = e.get("musicians") or []
        if cur_mus and isinstance(cur_mus[0], dict):
            cur_ids = ",".join([str(m.get("id")) for m in cur_mus])
        else:
            cur_ids = ",".join([str(x) for x in cur_mus])
        mus_ids_text, ok = QInputDialog.getText(self, "Редактировать ансамбль", "Musician IDs (comma-separated):", text=cur_ids)
        if not ok:
            return
        mus_ids = [int(x.strip()) for x in mus_ids_text.split(",") if x.strip().isdigit()] if mus_ids_text.strip() else []
        payload = {"name": name.strip(), "about": about.strip(), "ensemble_type": ensemble_type, "musicians_id": mus_ids}
        try:
            update_ensemble(eid, payload)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def delete_ensemble(self, eid: int):
        confirm = QMessageBox.question(self, "Удалить", "Удалить ансамбль?")
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                remove_ensemble(eid)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
