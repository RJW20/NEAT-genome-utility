from collections import Counter

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsSimpleTextItem
from PyQt6.QtGui import QPainter, QResizeEvent
from PyQt6.QtCore import QSize

from neat_genome_utility.node import Node
from neat_genome_utility.connection import Connection
from neat.genome import Genome
from neat.genome.activation_functions import sigmoid
from neat.history import History
from neat.evolution.mutation import add_node, add_connection


class GenomeWidget(QWidget):

    def __init__(self, genome: Genome) -> None:
        super().__init__()

        self.genome = genome

        self.scene = QGraphicsScene(0, 0, 0, 0)
        self.create_scene()
        
        view = QGraphicsView(self.scene)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        layout = QVBoxLayout()
        layout.addWidget(view)
        self.setLayout(layout)

    def create_scene(self) -> None:

        self.nodes = dict()
        self.nodes_per_layer = Counter()
        self.node_labels = []
        self.connections = set()

        for connection in self.genome.connections:

            try:
                from_node = self.nodes[connection.from_node.number]
            except KeyError:
                from_node = Node(connection.from_node, self.nodes_per_layer)
                self.nodes[connection.from_node.number] = from_node
                self.scene.addItem(from_node)
                node_label = QGraphicsSimpleTextItem(str(connection.from_node.number))
                node_label.setZValue(2)
                self.node_labels.append(node_label)
                self.scene.addItem(node_label)

            try:
                to_node = self.nodes[connection.to_node.number]
            except KeyError:
                to_node = Node(connection.to_node, self.nodes_per_layer)
                self.nodes[connection.to_node.number] = to_node
                self.scene.addItem(to_node)
                node_label = QGraphicsSimpleTextItem(str(connection.to_node.number))
                node_label.setZValue(2)
                self.node_labels.append(node_label)
                self.scene.addItem(node_label)
                
            viewable_connection = Connection(from_node, to_node, connection)
            if viewable_connection not in self.connections:
                self.connections.add(viewable_connection)
                self.scene.addItem(viewable_connection)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
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
    
    def add_random_node(self, history: History) -> None:
        add_node(self.genome, sigmoid, history)
        for item in self.scene.items():
            self.scene.removeItem(item)
        self.create_scene()
        self.resizeEvent(QResizeEvent(QSize(self.width(), self.height()), QSize(0,0)))

    def add_random_connection(self, history: History) -> None:
        add_connection(self.genome, history)
        for item in self.scene.items():
            self.scene.removeItem(item)
        self.create_scene()
        self.resizeEvent(QResizeEvent(QSize(self.width(), self.height()), QSize(0,0)))