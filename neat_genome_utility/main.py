from PyQt6.QtWidgets import QApplication

from neat_genome_utility.creation_dialog import CreationDialog
from neat_genome_utility.genome_window import GenomeWindow


def main() -> None:
    app = QApplication([])
    w = CreationDialog()

    if w.exec() == 0:
        gw = GenomeWindow()
        gw.show()

    app.exec()


if __name__ == '__main__':
    main()