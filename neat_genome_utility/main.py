from functools import partial

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout

from neat_genome_utility.genome_widget import GenomeWidget
from neat.genome import Genome
from neat.history import History


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("NEAT Genome Utility")

        history = History()
        self.genome_widget = GenomeWidget(Genome.new(4, 2, history))

        self.new_node_button = QPushButton("Add Node")
        self.new_node_button.clicked.connect(partial(self.genome_widget.add_random_node, history))

        self.new_connection_button = QPushButton("Add Connection")
        self.new_connection_button.clicked.connect(partial(self.genome_widget.add_random_connection, history))

        layout = QVBoxLayout()
        layout.addWidget(self.new_node_button)
        layout.addWidget(self.new_connection_button)
        layout.addWidget(self.genome_widget)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.resize(
            min(250 * self.genome_widget.genome.layers, 1200),
            min(100 * max(self.genome_widget.nodes_per_layer.values()), 800)
            )



if __name__ == '__main__':
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()