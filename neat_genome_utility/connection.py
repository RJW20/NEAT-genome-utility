from PyQt6.QtWidgets import QGraphicsLineItem
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt

from neat_genome_utility.node import Node
from neat.genome import connection  


class Connection(QGraphicsLineItem):

    def __init__(self, from_node: Node, to_node: Node, connection: connection.Connection) -> None:

        self.from_node: Node = from_node
        self.to_node: Node = to_node
        self.weight: float = connection.weight
        self.innovation_number: int = connection.innovation_number
        self.enabled: bool = connection.enabled

        super().__init__(0, 0, 0, 0)

        if self.weight >= 0:
            pen = QPen(Qt.GlobalColor.blue)
        else:
            pen = QPen(Qt.GlobalColor.red)
        if self.enabled:
            pen.setWidth(int(5 * abs(self.weight)) + 1)
        else:
            pen.setWidth(0)
        self.setPen(pen)
        self.setZValue(0)

    def resize(self) -> None:
        self.setLine(self.from_node.x_pos, self.from_node.y_pos, self.to_node.x_pos, self.to_node.y_pos)