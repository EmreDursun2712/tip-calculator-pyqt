import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from ui_tip_calculator import TipCalculator


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 11))
    app.setStyle("Fusion")

    window = TipCalculator()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
