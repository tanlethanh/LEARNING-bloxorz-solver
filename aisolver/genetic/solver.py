import random

from aisolver.genetic.population import Population


class GeneticSolver:
    population: Population

    def __init__(self, mutation_chance, goal_fitness_score, initial_population: Population):
        self.MUTATION_CHANCE = mutation_chance
        self.goal_fitness_score = goal_fitness_score
        self.population = initial_population

    def solve(self):
        while self.population.best_fitness_score != self.goal_fitness_score:
            self.population.selection()
            print(f"Best fitness score: {self.population.best_fitness_score}")
            self.population.cross_over()
            chance_random = random.Random()

            for chromosome in self.population.list_chromosome:
                if self.MUTATION_CHANCE > chance_random.random():
                    chromosome.mutation()
                fitness_score = chromosome.calculate_fitness()
                self.population.update_best_fitness_score(fitness_score)
        return [chromosome for chromosome in self.population.list_chromosome
                if chromosome.fitness_score == self.goal_fitness_score]
