from functools import partial

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QCloseEvent

from neat_genome_utility.creation.creation_dialog import CreationDialog
from neat_genome_utility.creation.new_dialog import NewDialog
from neat_genome_utility.creation.crossover_dialog import CrossoverDialog
from neat_genome_utility.genome.genome_window import GenomeWindow
from neat_genome_utility.window_list import WindowList
from neat.genome import Genome
from neat.history import History


def close(gws: WindowList, gw: GenomeWindow, a0: QCloseEvent | None) -> None:
    """Remove the given GenomeWindow from the WindowList (which will close it)"""
    
    gws.remove(gw)


def create(history: History, gws: WindowList, gw: GenomeWindow | None = None) -> None:
    """Create a new GenomeWidget either in the given GenomeWindow or in a new GenomeWindow which
    wil be added to the WindowList."""

    c_dlg = CreationDialog(gws.can_crossover)

    match(c_dlg.exec()):

        # Window closed
        case 0:
            return
        
        # New
        case 1:
            enforced = (gws.length == 0)
            new_dlg = NewDialog(enforced)

            match(new_dlg.exec()):
                
                # Cancel/window closed
                case 0:
                    return

                # Create
                case 1:
                    genome = Genome.new(new_dlg.inputs.value(), new_dlg.outputs.value(), history)

                    # Generate in new window if chosen
                    if new_dlg.new_window.isChecked():
                        gw = GenomeWindow(genome, history)
                        gw.plus_button.clicked.connect(partial(create, history, gws, gw))
                        gws.add(gw)
                        gw.closeEvent = partial(close, gws, gw)

                    # Change the current windows genome (only possible to select if a window exists)
                    else:
                        gw.new_genome(genome)

        # Load
        case 2:
            pass

        # Crossover
        case 3:
            crossover_dlg = CrossoverDialog(gws.compatible_windows)

            match(crossover_dlg.exec()):
                
                # Cancel/window closed
                case 0:
                    return

                # Create
                case 1:
                    return


def main() -> None:
    history = History()
    gws = WindowList()

    app = QApplication([])

    # Prompt the user to create a new GenomeWindow else terminate
    create(history, gws)
    if gws.length == 0:
        exit()

    app.exec()


if __name__ == '__main__':
    main()