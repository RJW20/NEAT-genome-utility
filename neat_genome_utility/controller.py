from functools import partial

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QCloseEvent

from neat_genome_utility.window_list import WindowList
from neat_genome_utility.creation.creation_dialog import CreationDialog
from neat_genome_utility.creation.new_dialog import NewDialog
from neat_genome_utility.creation.load_dialog import LoadDialog
from neat_genome_utility.creation.crossover_dialog import CrossoverDialog
from neat_genome_utility.genome.genome_window import GenomeWindow
from neat.history import History
from neat.genome import Genome
from neat.evolution import crossover


class Controller:
    """Class controlling the creation and removal of GenomeWindows."""

    def __init__(self) -> None:

        self.history = History()
        self.gws = WindowList()

        app = QApplication([])

        # Prompt the user to create a new GenomeWindow else terminate
        self.create()
        if self.gws.length == 0:
            exit()

        app.exec()

    def new_window(self, genome: Genome) -> None:
        """Start a new GenomeWindow showing the given Genome."""

        gw = GenomeWindow(genome, self.history)
        gw.plus_button.clicked.connect(partial(self.create, gw))
        gw.closeEvent = partial(self.close_window, gw)
        self.gws.add(gw)

    def close_window(self, gw: GenomeWindow, a0: QCloseEvent | None) -> None:
        """Remove the given GenomeWindow from self.gws (which will close it)."""

        self.gws.remove(gw)

    def new_genome(self, gw: GenomeWindow | None = None) -> None:
        """Open a NewDialog box and create a new GenomeWidget using the user's inputs."""

        enforced = (self.gws.length == 0)
        new_dlg = NewDialog(enforced)

        match(new_dlg.exec()):
            
            # Cancel/window closed
            case 0:
                return

            case 1:
                genome = Genome.new(new_dlg.inputs.value(), new_dlg.outputs.value(), self.history)

                # Generate in new window if chosen
                if new_dlg.new_window.isChecked():
                    self.new_window(genome)

                # Change the current window's genome (only possible to select if a window exists)
                else:
                    gw.new_genome(genome)

    def load_genome(self, gw: GenomeWindow | None = None) -> None:
        """Open a LoadDialog box and load the chosen Genome dump in a new GenomeWidget."""

        enforced = (self.gws.length == 0)
        load_dlg = LoadDialog(enforced)

        match(load_dlg.exec()):

            # Cancel/window closed
            case 0:
                return
            
            case 1:
                genome = load_dlg.loaded_genome

                # Generate in new window if chosen
                if load_dlg.new_window.isChecked():
                    self.new_window(genome)

                # Change the current window's genome (only possible to select if a window exists)
                else:
                    gw.new_genome(genome)

    def crossover(self) -> None:
        """Create a new GenomeWindow containing the Genome that is the result of crossing over two Genomes 
        in currently open GenomeWindows."""

        crossover_dlg = CrossoverDialog(self.gws.compatible_windows)

        match(crossover_dlg.exec()):
            
            # Cancel/window closed
            case 0:
                return

            case 1:
                parent1_id = int(crossover_dlg.parent1.currentText()[7:])
                parent2_id = int(crossover_dlg.parent2.currentText()[7:])
                parent1_genome = self.gws[parent1_id].genome_widget.genome
                parent2_genome = self.gws[parent2_id].genome_widget.genome
                genome = crossover(parent1_genome, parent2_genome, 0.75)
                self.new_window(genome)

    def create(self, gw: GenomeWindow | None = None) -> None:
        """Create a new GenomeWidget either in the given GenomeWindow or in a new GenomeWindow which
        wil be added to the WindowList self.gws."""

        c_dlg = CreationDialog(self.gws.can_crossover)

        match(c_dlg.exec()):

            # Window closed
            case 0:
                return
            
            case 1:
                self.new_genome(gw)

            case 2:
                self.load_genome(gw)

            case 3:
                self.crossover()