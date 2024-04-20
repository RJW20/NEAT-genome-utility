from neat.history import History
from neat.genome import Genome


def main() -> None:

    history = History()
    genome = Genome.new(4, 2, history)

    print(genome)


if __name__ == '__main__':
    main()