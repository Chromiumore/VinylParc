# main_window.py
from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from records_view import RecordsView
from musicians_view import MusiciansView
from ensembles_view import EnsemblesView
from compositions_view import CompositionsView
from performances_view import PerformancesView
from api import logout

class MainWindow(QMainWindow):
    def __init__(self, role: str, username: str):
        super().__init__()
        self.role = role
        self.username = username
        self.setWindowTitle(f"VinylParc — {username} ({role})")
        self.resize(1100, 700)

        central = QWidget()
        main_layout = QVBoxLayout()
        header = QHBoxLayout()

        self.lbl_user = QLabel(f"Пользователь: <b>{username}</b> ({role})")
        header.addWidget(self.lbl_user)
        header.addStretch()

        if self.role != "guest":
            self.btn_logout = QPushButton("Выйти")
            self.btn_logout.clicked.connect(self.handle_logout)
            header.addWidget(self.btn_logout)

        main_layout.addLayout(header)

        self.tabs = QTabWidget()

        # Records (catalog)
        self.records_tab = RecordsView(role=self.role)
        self.tabs.addTab(self.records_tab, "Records")

        # Musicians
        self.musicians_tab = MusiciansView(role=self.role)
        self.tabs.addTab(self.musicians_tab, "Musicians")

        # Ensembles
        self.ensembles_tab = EnsemblesView(role=self.role)
        self.tabs.addTab(self.ensembles_tab, "Ensembles")

        # Compositions
        self.compositions_tab = CompositionsView(role=self.role)
        self.tabs.addTab(self.compositions_tab, "Compositions")

        # Performances
        self.performances_tab = PerformancesView(role=self.role)
        self.tabs.addTab(self.performances_tab, "Performances")

        main_layout.addWidget(self.tabs)
        central.setLayout(main_layout)
        self.setCentralWidget(central)

    def handle_logout(self):
        logout()
        self.close()
