from neat_genome_utility.genome.genome_window import GenomeWindow


class WindowList(list):
    """Subclass of built-in list that automatically shows new windows and removes
    windows when they are closed.
    
    Also automatically sets the names of the windows for easy tracking when doing 
    crossovers.
    """

    genome_id = 0

    def append(self, gw: GenomeWindow) -> None:
        super().append(gw)
        self.genome_id += 1
        gw.setWindowTitle(f"Genome {self.genome_id}")
        gw.show()

    def extend(self, gws: list[GenomeWindow]) -> None:
        super().extend(gws)
        for gw in gws:
            self.genome_id += 1
            gw.setWindowTitle(f"Genome {self.genome_id}")
            gw.show()

    def insert(self, i: int, gw: GenomeWindow) -> None:
        super().insert(i, gw)
        self.genome_id += 1
        gw.setWindowTitle(f"Genome {self.genome_id}")
        gw.show()

    def remove(self, gw: GenomeWindow) -> None:
        super().remove(gw)
        gw.close()

    def pop(self, i: int) -> None:
        gw = self[i]
        super().pop(i)
        gw.close()