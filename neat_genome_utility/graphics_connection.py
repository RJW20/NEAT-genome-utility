from PyQt6.QtWidgets import QGraphicsLineItem
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt

from neat_genome_utility.graphics_node import GraphicsNode
from neat.genome import connection  


class GraphicsConnection(QGraphicsLineItem):
    """A representation of a Connection in a Genome that also can be placed in a QGraphicsScene and 
    automatically controls its length, thickness and endpoints."""

    def __init__(self, from_node: GraphicsNode, to_node: GraphicsNode, connection: connection.Connection) -> None:

        # Retrive information from the original Connection
        self.from_node: GraphicsNode = from_node
        self.to_node: GraphicsNode = to_node
        self.weight: float = connection.weight
        self.innovation_number: int = connection.innovation_number
        self.enabled: bool = connection.enabled

        super().__init__(0, 0, 0, 0)

        # Set the colour and width (if disabled width = 0) of the line
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
        """Move the endpoints of the Connection using the Nodes it connects."""

        self.setLine(self.from_node.x_pos, self.from_node.y_pos, self.to_node.x_pos, self.to_node.y_pos)