import sys

from PyQt5.QtWidgets import QApplication
from control import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
