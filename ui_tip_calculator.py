from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QCheckBox,
    QSlider
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

from logic import calculate_tip_per_person, CalculationError


class TipCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tip Calculator")
        self.setFixedSize(380, 320)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)

        # --- Title ---
        title_label = QLabel("💸 Tip Calculator")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # --- Bill amount ---
        bill_layout = QHBoxLayout()
        bill_label = QLabel("Total bill:")
        self.bill_input = QLineEdit()
        self.bill_input.setPlaceholderText("e.g. 125.50")
        bill_layout.addWidget(bill_label)
        bill_layout.addWidget(self.bill_input)
        main_layout.addLayout(bill_layout)

        # --- Tip slider + label ---
        tip_layout = QVBoxLayout()
        tip_label_row = QHBoxLayout()
        self.tip_text_label = QLabel("Tip: 10%")
        tip_label_row.addWidget(self.tip_text_label)
        tip_label_row.addStretch()
        tip_layout.addLayout(tip_label_row)

        self.tip_slider = QSlider(Qt.Horizontal)
        self.tip_slider.setRange(0, 30)
        self.tip_slider.setValue(10)
        self.tip_slider.setTickInterval(5)
        self.tip_slider.setTickPosition(QSlider.TicksBelow)
        self.tip_slider.valueChanged.connect(self.on_tip_slider_changed)
        tip_layout.addWidget(self.tip_slider)

        main_layout.addLayout(tip_layout)

        # --- Number of people ---
        people_layout = QHBoxLayout()
        people_label = QLabel("Number of people:")
        self.people_input = QLineEdit()
        self.people_input.setPlaceholderText("e.g. 2")
        people_layout.addWidget(people_label)
        people_layout.addWidget(self.people_input)
        main_layout.addLayout(people_layout)

        # --- Dark mode checkbox ---
        theme_layout = QHBoxLayout()
        self.dark_mode_checkbox = QCheckBox("Dark mode")
        self.dark_mode_checkbox.stateChanged.connect(self.on_dark_mode_toggled)
        theme_layout.addWidget(self.dark_mode_checkbox)
        theme_layout.addStretch()
        main_layout.addLayout(theme_layout)

        # --- Calculate button ---
        self.calc_button = QPushButton("Calculate")
        self.calc_button.clicked.connect(self.on_calculate_clicked)
        main_layout.addWidget(self.calc_button)

        # --- Result label ---
        self.result_label = QLabel("Each person should pay: ₺0.00")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 8px;")
        main_layout.addWidget(self.result_label)

        self.setLayout(main_layout)

    # ===================== Slots / Logic =====================

    def on_tip_slider_changed(self, value: int):
        self.tip_text_label.setText(f"Tip: {value}%")

    def on_dark_mode_toggled(self, state: int):
        enabled = state == Qt.Checked
        self.apply_dark_theme(enabled)

    def apply_dark_theme(self, enabled: bool):
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if not app:
            return

        if enabled:
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(30, 30, 30))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(45, 45, 45))
            palette.setColor(QPalette.AlternateBase, QColor(60, 60, 60))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(45, 45, 45))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Highlight, QColor(100, 149, 237))
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            palette = app.style().standardPalette()

        app.setPalette(palette)

    def on_calculate_clicked(self):
        bill_str = self.bill_input.text()
        people_str = self.people_input.text()
        tip_percent = self.tip_slider.value()

        try:
            per_person = calculate_tip_per_person(bill_str, people_str, tip_percent)
            self.result_label.setText(f"Each person should pay: ₺{per_person}")
        except CalculationError as e:
            self.show_error(str(e))
        except Exception:
            self.show_error("Unknown error, please check your inputs.")

    def show_error(self, message: str):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec_()
