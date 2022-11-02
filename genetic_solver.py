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
        len_half_list = len(self.list_chromosome)
        index = 0
        while index < len_half_list - 1:
            len_dna = len(self.list_chromosome[index].DNA)
            split_point = random.randint(0, len_dna)
            first_dna = (self.list_chromosome[index].DNA[0:split_point] +
                         self.list_chromosome[index + 1].DNA[split_point:len_dna])
            second_dna = (self.list_chromosome[index].DNA[split_point:len_dna] +
                          self.list_chromosome[index + 1].DNA[0:split_point])

            self.list_chromosome[index].DNA = first_dna
            self.list_chromosome[index + 1].DNA = second_dna
            index += 2

    def update_best_fitness_score(self, fitness_score):
        if self.fitness_objective == "MINIMIZE" and fitness_score < self.best_fitness_score:
            self.best_fitness_score = fitness_score
        elif self.fitness_objective == "MAXIMIZE" and fitness_score > self.best_fitness_score:
            self.best_fitness_score = fitness_score


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
