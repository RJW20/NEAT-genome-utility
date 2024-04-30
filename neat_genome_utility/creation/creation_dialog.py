from PyQt6.QtWidgets import (
    QDialog, QWidget, QPushButton,
    QLabel, QHBoxLayout, QVBoxLayout,
)
from PyQt6.QtCore import Qt

class CreationDialog(QDialog):
    """Dialog box that enables the user to choose a method for creating a GenomeWidget."""

    def __init__(self, crossover: bool, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Genome Creation")

        message = QLabel("Choose Genome creation method:", alignment=Qt.AlignmentFlag.AlignTop)

        self.new = QPushButton("New")
        self.new.clicked.connect(self.new_clicked)

        self.load = QPushButton("Load")
        self.load.clicked.connect(self.load_clicked)

        self.crossover = QPushButton("Crossover")
        self.crossover.clicked.connect(self.crossover_clicked)
        if not crossover:
            self.crossover.setEnabled(False)

        layout1 = QVBoxLayout()
        layout1.addWidget(message)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.new)
        layout2.addWidget(self.load)
        layout2.addWidget(self.crossover)
        layout1.addLayout(layout2)
        self.setLayout(layout1)

        self.setFixedSize(250, 100)

    def new_clicked(self) -> None:
        self.done(1)

    def load_clicked(self) -> None:
        self.done(2)

    def crossover_clicked(self) -> None:
        self.done(3)