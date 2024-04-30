from neat_genome_utility.genome_window import GenomeWindow


class WindowList(list):
    """Subclass of built-in list that automatically shows new windows and removes
    windows when they are closed."""


    def append(self, gw: GenomeWindow) -> None:
        super().append(gw)
        gw.show()

    def extend(self, gws: list[GenomeWindow]) -> None:
        super().extend(gws)
        for gw in gws:
            gw.show()

    def insert(self, i: int, gw: GenomeWindow) -> None:
        super().insert(i, gw)
        gw.show()

    def remove(self, gw: GenomeWindow) -> None:
        super().remove(gw)
        gw.close()

    def pop(self, i: int) -> None:
        gw = self[i]
        super().pop(i)
        gw.close()