import sys

from PyQt5 import QtWidgets
from app import OllamaAssistant


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = OllamaAssistant()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
