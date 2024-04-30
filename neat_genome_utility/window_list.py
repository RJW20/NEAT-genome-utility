from collections import Counter

from neat_genome_utility.genome.genome_window import GenomeWindow


class WindowList():
    """Object containing the open GenomeWindows that automatically shows new windows and removes
    windows when they are closed.
    
    Also automatically sets the names of the windows for easy tracking when doing 
    crossovers.
    """

    genome_id = 0
    windows = dict()

    def set_up_new_window(self, gw: GenomeWindow) -> None:
        gw.setWindowTitle(f"Genome {self.genome_id}")
        gw.show()

    def add(self, gw: GenomeWindow) -> None:
        self.genome_id += 1
        self.windows[self.genome_id] = gw 
        self.set_up_new_window(gw)

    def remove(self, gw: GenomeWindow) -> None:
        genome_id = int(gw.windowTitle()[7:])
        self.windows.pop(genome_id)
        gw.close()

    def __getitem__(self, id: int) -> GenomeWindow:
        return self.windows[id]

    @property
    def length(self) -> int:
        return len(self.windows.keys())
    
    @property
    def compatible_windows(self) -> dict[tuple[int,int], list[GenomeWindow]]:
        """Return a dictionary containing GenomeWindows which contain Genome's which 
        have the same number of inputs and outputs."""

        compatibility_dict = dict()
        for id, window in self.windows.items():
            genome = window.genome_widget.genome
            try:
                compatibility_dict[(genome.input_count, genome.output_count)].append(id)
            except KeyError:
                compatibility_dict[(genome.input_count, genome.output_count)] = [id]

        return compatibility_dict
    
    @property
    def can_crossover(self) -> bool:
        """Return True if there is at least one compatibile Genome pair."""

        counter = Counter()
        for id, window in self.windows.items():
            genome = window.genome_widget.genome
            counter[(genome.input_count, genome.output_count)] += 1
            if counter[(genome.input_count, genome.output_count)] == 2:
                return True
            
        return False