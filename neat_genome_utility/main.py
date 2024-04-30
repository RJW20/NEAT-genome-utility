from functools import partial

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QCloseEvent

from neat_genome_utility.creation_dialog import CreationDialog
from neat_genome_utility.genome_window import GenomeWindow
from neat_genome_utility.new_dialog import NewDialog
from neat_genome_utility.window_list import WindowList
from neat.genome import Genome
from neat.history import History


def close(gws: WindowList, gw: GenomeWindow, a0: QCloseEvent | None) -> None:
    gws.remove(gw)


def new(history: History, gws: WindowList, gw: GenomeWindow | None = None) -> None:

    c_dlg = CreationDialog()

    match(c_dlg.exec()):

        case 0:
            return
        case 1:
            enforced = (len(gws) == 0)
            n_dlg = NewDialog(enforced)

            match(n_dlg.exec()):
                
                case 0:
                    return

                case 1:
                    genome = Genome.new(n_dlg.inputs.value(), n_dlg.outputs.value(), history)
                    if n_dlg.new_window.isChecked():
                        gw = GenomeWindow(genome, history)
                        gw.plus_button.clicked.connect(partial(new, history, gws, gw))
                        gws.append(gw)
                        gw.closeEvent = partial(close, gws, gw)
                    else:
                        gw.new_genome(genome)


def main() -> None:
    history = History()
    gws = WindowList()

    app = QApplication([])

    new(history, gws)
    if len(gws) == 0:
        exit()

    app.exec()


if __name__ == '__main__':
    main()