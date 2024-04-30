from collections import Counter

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsSimpleTextItem
from PyQt6.QtGui import QPainter, QResizeEvent
from PyQt6.QtCore import QSize

from neat_genome_utility.genome.graphics_node import GraphicsNode
from neat_genome_utility.genome.graphics_connection import GraphicsConnection
from neat.genome import Genome
from neat.genome.activation_functions import sigmoid
from neat.history import History
from neat.evolution.mutation import add_node, add_connection


class GenomeWidget(QWidget):
    """Widget displaying a Genome."""

    def __init__(self, genome: Genome) -> None:
        super().__init__()

        self.genome = genome

        # Set up the scene/view
        self.scene = QGraphicsScene(0, 0, 0, 0)
        self.create_scene()
        view = QGraphicsView(self.scene)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        layout = QVBoxLayout()
        layout.addWidget(view)
        self.setLayout(layout)

    def create_scene(self) -> None:
        """Add all the Nodes and Connections in this Widget's Genome to a QGraphicsScene using their Graphics versions."""

        # Create the GraphicsNodes
        self.nodes = dict()
        self.nodes_per_layer = Counter()
        self.node_labels = []
        for node in self.genome.nodes:
            g_node = GraphicsNode(node, self.nodes_per_layer)
            self.nodes[node.number] = g_node
            self.scene.addItem(g_node)
            node_label = QGraphicsSimpleTextItem(str(node.number))
            node_label.setZValue(2)
            self.node_labels.append(node_label)
            self.scene.addItem(node_label)

        #Create the GraphicsConnections
        self.connections = set()
        for connection in self.genome.connections:
            from_node = self.nodes[connection.from_node.number]
            to_node = self.nodes[connection.to_node.number]
            g_connection = GraphicsConnection(from_node, to_node, connection)
            self.connections.add(g_connection)
            self.scene.addItem(g_connection)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        """Overload the QWidget.resizeEvent method to correctly size and position all the items in the QGraphicsScene."""

        self.scene.setSceneRect(0, 0, self.width() * 0.9, self.height() * 0.9)

        diameter = max(min(self.scene.width() // (1.5 * self.genome.layers), self.scene.height() // (2 * max(self.nodes_per_layer.values()))), 20)
        radius = diameter // 2
        x_padding = self.scene.width() // self.genome.layers
        for node in self.nodes.values():
            y_padding = self.scene.height() // self.nodes_per_layer[node.layer]
            node.resize(x_padding, y_padding, radius)

        for connection in self.connections:
            if connection.enabled:
                connection.resize()

        for node_label in self.node_labels:
            label = node_label.text()
            node = self.nodes[int(label)]
            font = node_label.font()
            font.setPointSize(int(radius))
            node_label.setFont(font)
            node_label.setPos(node.x_pos - len(label) * diameter / 6, node.y_pos - radius)

        return super().resizeEvent(a0)
    
    def refresh_scene(self) -> None:
        """Update the scene to show changes to the Genome."""

        for item in self.scene.items():
            self.scene.removeItem(item)
        self.create_scene()
        self.resizeEvent(QResizeEvent(QSize(self.width(), self.height()), QSize(0,0)))
    
    def add_random_node(self, history: History) -> None:
        """Add a random Node to this Widget's Genome and update the scene to reflect the change."""

        add_node(self.genome, sigmoid, history)
        self.refresh_scene()

    def add_random_connection(self, history: History) -> None:
        """Add a random Connection to this Widget's Genome (if possible) and update the scene to reflect the change."""

        add_connection(self.genome, history)
        self.refresh_scene()

    def new_genome(self, genome: Genome) -> None:
        """Change this GenomeWidget's Genome."""

        self.genome = genome
        self.refresh_scene()