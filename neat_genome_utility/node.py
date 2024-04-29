from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtGui import QBrush, QPen
from PyQt6.QtCore import Qt

from neat.genome import node    

class Node(QGraphicsEllipseItem):

    def __init__(self, base_node: node.Node, nodes_per_layer: dict) -> None:

        self.number: int = base_node.number
        self.layer: int = base_node.layer
        self.intra_layer_number: int = nodes_per_layer[self.layer]
        nodes_per_layer[self.layer] += 1

        super().__init__(0, 0, 0, 0)

        brush = QBrush(Qt.GlobalColor.gray)
        self.setBrush(brush)
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(2)
        self.setPen(pen)
        self.setZValue(1)

        self.x_pos = 0
        self.y_pos = 0

    def resize(self, x_padding: int, y_padding: int, radius: int) -> None:
        self.x_pos = (self.layer + 0.5)* x_padding
        self.y_pos = (self.intra_layer_number + 0.5) * y_padding
        diameter = radius * 2
        self.setRect(self.x_pos - radius, self.y_pos - radius, diameter, diameter)