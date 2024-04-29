from PyQt6.QtWidgets import (
    QDialog, QWidget, QPushButton,
    QLabel, QHBoxLayout, QVBoxLayout,
)

class CreationDialog(QDialog):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Genome Creation")

        message = QLabel("Choose Genome creation method:")

        self.new = QPushButton("New")
        self.new.clicked.connect(self.new_clicked)

        self.load = QPushButton("Load")

        self.crossover = QPushButton("Crossover")

        layout1 = QVBoxLayout()

        layout1.addWidget(message)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.new)
        layout2.addWidget(self.load)
        layout2.addWidget(self.crossover)
        
        layout1.addLayout(layout2)
        self.setLayout(layout1)

    def new_clicked(self) -> None:
        self.done(0)