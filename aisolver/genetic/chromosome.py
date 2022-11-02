import random


class Chromosome:
    DNA: list
    fitness_score: int
    available_node_type: list

    def __init__(self, dna, available_node_type):
        self.DNA = dna
        self.calculate_fitness()
        self.available_node_type = available_node_type

    def __str__(self) -> str:
        return f"Fitness score: {self.fitness_score} -> [ " + ", ".join([str(ele) for ele in self.DNA]) + " ]"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Chromosome):
            return self.fitness_score == o.fitness_score
        else:
            raise Exception("This object is not a Chromosome!")

    def __lt__(self, o: object) -> bool:
        if isinstance(o, Chromosome):
            return self.fitness_score < o.fitness_score
        else:
            raise Exception("This object is not a Chromosome!")

    def mutation(self):
        random_index = random.randint(0, len(self.DNA) - 1)
        random_node = self.available_node_type[random.randint(0, len(self.available_node_type) - 1)]
        self.DNA[random_index] = random_node

    def calculate_fitness(self) -> int:
        pass


