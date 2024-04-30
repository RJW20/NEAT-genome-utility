from functools import partial

from PyQt6.QtWidgets import (
    QDialog, QWidget, QPushButton, QSpinBox,
    QLabel, QCheckBox, QHBoxLayout, QVBoxLayout,
)
from PyQt6.QtCore import Qt


class NewDialog(QDialog):
    """Dialog box that enables the user to create a new GenomeWidget."""

    def __init__(self, enforced: bool, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("New Genome")

        self.input_label = QLabel("Inputs:", alignment=Qt.AlignmentFlag.AlignLeft)
        self.output_label = QLabel("Outputs:", alignment=Qt.AlignmentFlag.AlignLeft)

        self.inputs = QSpinBox()
        self.inputs.setMinimum(1)
        self.inputs.setGeometry(70, 0, 50, 50)
        self.outputs = QSpinBox()
        self.outputs.setMinimum(1)
        self.outputs.setGeometry(70, 0, 50, 50)

        self.new_window = QCheckBox("Create in new window")
        self.new_window.setChecked(True)
        self.new_window.toggled.connect(partial(self.new_window_toggle, enforced))

        self.cancel = QPushButton("Cancel")
        self.cancel.clicked.connect(self.cancel_clicked)
        self.create_b = QPushButton("Create")
        self.create_b.clicked.connect(self.create_clicked)

        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.inputs)
        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.outputs)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel)
        button_layout.addWidget(self.create_b)
        layout.addLayout(input_layout)
        layout.addLayout(output_layout)
        layout.addWidget(self.new_window)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.setFixedSize(200, 150)

    def new_window_toggle(self, enforced: bool) -> None:
        """Allow the user to create the new GenomeWidget in the same window only if it wasn't enforced
        that it had to be a new window."""

        if enforced and not self.new_window.isChecked():
            self.new_window.setChecked(True)

    def cancel_clicked(self) -> None:
        self.done(0)

    def create_clicked(self) -> None:
        self.done(1)