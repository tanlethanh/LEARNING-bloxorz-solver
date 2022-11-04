import random

from aisolver.genetic.chromosome import Chromosome


class Population:
    list_chromosome: list[Chromosome]
    best_fitness_score: int

    def __init__(self, fitness_objective, list_chromosome):
        self.fitness_objective = fitness_objective
        self.list_chromosome = list_chromosome
        if self.fitness_objective == "MINIMIZE":
            self.best_fitness_score = 99999
        elif self.fitness_objective == "MAXIMIZE":
            self.best_fitness_score = -1

    def __str__(self) -> str:
        population_str = "Population: \n"
        for ele in self.list_chromosome:
            population_str += f"\t{ele}\n"
        return population_str

    def selection(self):
        if self.fitness_objective == "MINIMIZE":
            self.list_chromosome.sort()
        elif self.fitness_objective == "MAXIMIZE":
            self.list_chromosome.sort(reverse=True)

        self.best_fitness_score = self.list_chromosome[0].fitness_score

    def cross_over(self):
        len_half_list = int(len(self.list_chromosome) / 2)
        index = 0
        while index < len_half_list:
            len_dna = len(self.list_chromosome[index].DNA)
            split_point = random.randint(0, len_dna)
            first_dna = (self.list_chromosome[index].DNA[0:split_point] +
                         self.list_chromosome[index + 1].DNA[split_point:len_dna])
            second_dna = (self.list_chromosome[index].DNA[split_point:len_dna] +
                          self.list_chromosome[index + 1].DNA[0:split_point])

            self.list_chromosome[index].DNA = first_dna
            self.list_chromosome[index + len_half_list].DNA = second_dna
            index += 1

    def update_best_fitness_score(self, fitness_score):
        if self.fitness_objective == "MINIMIZE" and fitness_score < self.best_fitness_score:
            self.best_fitness_score = fitness_score
        elif self.fitness_objective == "MAXIMIZE" and fitness_score > self.best_fitness_score:
            self.best_fitness_score = fitness_score
