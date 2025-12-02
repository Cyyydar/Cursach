# main.py

import sys
from PyQt5.QtWidgets import QApplication
from gui import mainWindow


def main():
    app = QApplication(sys.argv)
    window = mainWindow.MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
