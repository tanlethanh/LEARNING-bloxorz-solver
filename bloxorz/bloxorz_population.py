from aisolver.genetic.population import Population
from bloxorz.bloxorz_chromosome import BloxorzChromosome


class BloxorzPopulation(Population):

    list_chromosome: list[BloxorzChromosome]
    CROSS_OVER_TYPES = ["default", "custom"]

    def __init__(self, list_chromosome, cross_over_type="default"):
        self.number_generation = 1
        self.cross_over_type = cross_over_type

        super().__init__(fitness_objective="MINIMIZE", list_chromosome=list_chromosome)

    def cross_over(self):
        self.number_generation += 1
        if self.cross_over_type == "default":
            super().cross_over()

        elif self.cross_over_type == "custom":
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
                index += 1

    @staticmethod
    def is_valid_cross_over_type(cross_over_type):
        return cross_over_type in BloxorzPopulation.CROSS_OVER_TYPES

    @staticmethod
    def all_cross_over_types():
        return BloxorzPopulation.CROSS_OVER_TYPES[:]

