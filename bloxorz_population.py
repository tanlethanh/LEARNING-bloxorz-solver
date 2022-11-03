from aisolver.genetic.population import Population
from bloxorz_chromosome import BloxorzChromosome


class BloxorzPopulation(Population):

    list_chromosome: list[BloxorzChromosome]

    def __init__(self, fitness_objective, list_chromosome):
        self.number_generation = 0
        super().__init__(fitness_objective, list_chromosome)

    def cross_over(self):
        len_half_list = int(len(self.list_chromosome) / 2)
        index = 0
        while index < len_half_list:
            len_dna = len(self.list_chromosome[index].DNA)
            split_point = self.list_chromosome[index].cross_index
            first_dna = (self.list_chromosome[index].DNA[0:split_point] +
                         self.list_chromosome[index + 1].DNA[split_point:len_dna])
            second_dna = (self.list_chromosome[index].DNA[split_point:len_dna] +
                          self.list_chromosome[index + 1].DNA[0:split_point])

            self.list_chromosome[index].DNA = first_dna
            self.list_chromosome[index + len_half_list].DNA = second_dna
            # print(f"Pair: {index} and {index + len_half_list}")
            index += 1

