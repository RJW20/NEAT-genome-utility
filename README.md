# NEAT Genome Utility
An application that enables easy creation, editing and viewing of Genomes used in my implementation of NEAT https://github.com/RJW20/NEAT.

## Screenshots
A red line signifies a connection with negative weight and a blue line is for positive. \
A thicker line corresponds to a connection with weight that has higher magnitude (with 1 being the thickest). \
Only enabled connections are visible.

![Example](https://github.com/RJW20/NEAT-genome-utility/assets/99192767/44b8ce1e-c2bd-4783-85a9-6aa1bfefbe07)

![ExampleLarge](https://github.com/RJW20/NEAT-genome-utility/assets/99192767/6ea9d7bb-121d-4092-901e-22a3d81c3fa7)

## Basic Usage
There are 3 options for creating/loading Genomes.

![CreationDialog](https://github.com/RJW20/NEAT-genome-utility/assets/99192767/fc513625-aa3e-4fdb-9e4d-8c35c2c76cb7)

### New
Choose how many input and output nodes you want and a neural network will be created with one connection (note that a bias node will always be added on top of the number of inputs specified).

![NewDialog](https://github.com/RJW20/NEAT-genome-utility/assets/99192767/7685c6f9-86fe-41a2-ba3f-76927dae20b0)

### Load
Select the Location of a Genome created during a run of the NEAT algorithm and it will be loaded.

![LoadDialog](https://github.com/RJW20/NEAT-genome-utility/assets/99192767/dc5b0830-d1b6-41f1-97fb-1c7dcdf1b7c3)


### Crossover
If there are 2 or more windows open that have Genomes with the same number inputs and outputs they will be able to be crossed over to create another Genome.

![CrossoverDialog](https://github.com/RJW20/NEAT-genome-utility/assets/99192767/6f109046-10db-48f9-9e5c-509218c4f534)

### Editing the Genome
The add node and add connection buttons will add a random new node or (enabled) connection to the shown Genome.
