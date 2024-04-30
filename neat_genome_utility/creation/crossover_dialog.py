from PyQt6.QtWidgets import (
    QDialog, QWidget, QLabel, QComboBox,
    QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt


class CrossoverDialog(QDialog):
    """Dialog box that enables the user to create a new GenomeWidget via valid crossover."""

    def __init__(self, compatible_ids: dict, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Crossover")

        self.compatible_groups = {i+1: value for i, value in enumerate(compatible_ids.values())}

        self.group_label = QLabel("Group:", alignment=Qt.AlignmentFlag.AlignLeft)
        self.groups = QComboBox()
        self.groups.addItems(
            ['-'] + [f'Inputs: {key[0]}, Outputs: {key[1]} (Genomes {",".join([str(v) for v in value])})' for key, value in compatible_ids.items()]
        )
        self.groups.currentIndexChanged.connect(self.group_changed)

        self.parent1_label = QLabel("Parent 1:", alignment=Qt.AlignmentFlag.AlignLeft)
        self.parent1 = QComboBox()
        self.parent1.addItems(['-'])
        self.parent1.currentIndexChanged.connect(self.parent1_changed)

        self.parent2_label = QLabel("Parent 2:", alignment=Qt.AlignmentFlag.AlignLeft)
        self.parent2 = QComboBox()
        self.parent2.addItems(['-'])
        self.parent2.currentIndexChanged.connect(self.parent2_changed)

        self.cancel = QPushButton("Cancel")
        self.cancel.clicked.connect(self.cancel_clicked)
        self.crossover = QPushButton("Crossover")
        self.crossover.clicked.connect(self.crossover_clicked)
        self.crossover.setEnabled(False)

        layout = QVBoxLayout()
        group_layout = QHBoxLayout()
        group_layout.addWidget(self.group_label)
        group_layout.addWidget(self.groups)
        parent1_layout = QHBoxLayout()
        parent1_layout.addWidget(self.parent1_label)
        parent1_layout.addWidget(self.parent1)
        parent2_layout = QHBoxLayout()
        parent2_layout.addWidget(self.parent2_label)
        parent2_layout.addWidget(self.parent2)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel)
        button_layout.addWidget(self.crossover)
        layout.addLayout(group_layout)
        layout.addLayout(parent1_layout)
        layout.addLayout(parent2_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.setFixedSize(300, 250)

    def group_changed(self, id: int) -> None:
        """Set parent1 and parent2 ComboBoxes possible options."""
        
        self.parent1.clear()
        self.parent2.clear()
        self.parent1.addItems(['-'])
        self.parent2.addItems(['-'])

        if id == 0:
            return
        
        self.parent1.addItems([f'Genome {i}' for i in self.compatible_groups[id]])
        self.parent2.addItems([f'Genome {i}' for i in self.compatible_groups[id]])

    def parent1_changed(self, id: int) -> None:
        """Set crossover button to enabled parent1 and parent2 are not the same."""

        if id != self.parent2.currentIndex() and not (id == 0 or self.parent2.currentIndex() == 0):
            self.crossover.setEnabled(True)
        else:
            self.crossover.setEnabled(False)


    def parent2_changed(self, id: int) -> None:
        """Remove the chosen option from parent1, and set crossover button to enabled if possible."""

        if id != self.parent1.currentIndex()and not (id == 0 or self.parent1.currentIndex() == 0):
            self.crossover.setEnabled(True)
        else:
            self.crossover.setEnabled(False)

    def cancel_clicked(self) -> None:
        self.done(0)

    def crossover_clicked(self) -> None:
        self.done(1)