# import sys
# from PySide6.QtWidgets import QApplication
# from login import LoginWindow

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     login = LoginWindow()
#     login.show()
#     sys.exit(app.exec())


# main.py
import sys
from PySide6.QtWidgets import QApplication
from login import LoginWindow
from api import load_local_profile

if __name__ == "__main__":
    app = QApplication(sys.argv)
    profile = load_local_profile()
    win = LoginWindow(start_profile=profile)
    win.show()
    sys.exit(app.exec())
