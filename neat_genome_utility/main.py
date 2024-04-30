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
    """Remove the given GenomeWindow from the WindowList (which will close it)"""
    
    gws.remove(gw)


def create(history: History, gws: WindowList, gw: GenomeWindow | None = None) -> None:
    """Create a new GenomeWidget either in the given GenomeWindow or in a new GenomeWindow which
    wil be added to the WindowList."""

    c_dlg = CreationDialog()

    match(c_dlg.exec()):

        # Window closed
        case 0:
            return
        
        # New
        case 1:
            enforced = (len(gws) == 0)
            n_dlg = NewDialog(enforced)

            match(n_dlg.exec()):
                
                # Cancel/window closed
                case 0:
                    return

                # Create
                case 1:
                    genome = Genome.new(n_dlg.inputs.value(), n_dlg.outputs.value(), history)

                    # Generate in new window if chosen
                    if n_dlg.new_window.isChecked():
                        gw = GenomeWindow(genome, history)
                        gw.plus_button.clicked.connect(partial(create, history, gws, gw))
                        gws.append(gw)
                        gw.closeEvent = partial(close, gws, gw)

                    # Change the current windows genome (only possible to select if a window exists)
                    else:
                        gw.new_genome(genome)


def main() -> None:
    history = History()
    gws = WindowList()

    app = QApplication([])

    # Prompt the user to create a new GenomeWindow else terminate
    create(history, gws)
    if len(gws) == 0:
        exit()

    app.exec()


if __name__ == '__main__':
    main()