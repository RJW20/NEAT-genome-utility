from functools import partial

from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt

from neat_genome_utility.genome.genome_widget import GenomeWidget
from neat.genome import Genome
from neat.history import History


class GenomeWindow(QMainWindow):
    """Window containing a GenomeWidget and buttons to manipulate it."""

    def __init__(self, genome: Genome, history: History):

        super().__init__()

        self.genome_widget = GenomeWidget(genome)

        self.new_node_button = QPushButton("Add Node")
        self.new_node_button.clicked.connect(partial(self.genome_widget.add_random_node, history))

        self.new_connection_button = QPushButton("Add Connection")
        self.new_connection_button.clicked.connect(partial(self.genome_widget.add_random_connection, history))

        self.plus_button = QPushButton("+")
        self.plus_button.setFixedWidth(50)
        font = self.plus_button.font()
        font.setPointSize(12)
        self.plus_button.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(self.new_node_button)
        layout.addWidget(self.new_connection_button)
        layout.addWidget(self.genome_widget)
        layout.addWidget(self.plus_button, alignment=Qt.AlignmentFlag.AlignRight)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.resize(
            max(min(250 * self.genome_widget.genome.layers, 1200), 300),
            max(min(100 * max(self.genome_widget.nodes_per_layer.values()), 800), 300)
        )

    def new_genome(self, genome: Genome) -> None:
        """Replace the genome contained in this window."""
        
        self.genome_widget.new_genome(genome)
        self.resize(
            max(min(250 * self.genome_widget.genome.layers, 1200), 300),
            max(min(100 * max(self.genome_widget.nodes_per_layer.values()), 800), 300)
        )