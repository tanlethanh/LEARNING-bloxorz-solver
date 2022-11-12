import json
import os
import random
import time
from pathlib import Path

import psutil

from aisolver.blind.frontier import StackFrontier, QueueFrontier
from aisolver.blind.solver import Solver
from aisolver.genetic.population import Population
from aisolver.genetic.solver import GeneticSolver
from bloxorz.bloxorz_chromosome import BlockAction, BloxorzChromosome
from bloxorz.bloxorz_population import BloxorzPopulation
from bloxorz.element.block import DoubleBlock
from bloxorz.element.game_board import GameBoard
from bloxorz.bloxorz_state import BloxorzState


class BloxorzSolver:

    @staticmethod
    def blind_solve(input_file_name, algorithm):
        """
        This function solve bloxorz game by blind search algorithm
        :param input_file_name
        :param algorithm is DFS (Depth first search) or BFS (Breadth first search)
        :return: list step of solution
        """
        game_board, state_bridges, initial_position = BloxorzSolver.parse_input_data(input_file_name)

        frontier = None
        if algorithm == "DFS":
            frontier = StackFrontier()

        elif algorithm == "BFS":
            frontier = QueueFrontier()

        initial_state = BloxorzState(DoubleBlock(initial_position), state_bridges, game_board)
        game_solver = Solver(frontier, initial_state)

        start = time.time()
        begin_mem = psutil.Process(os.getpid()).memory_info().rss
        res = game_solver.solve()
        end = time.time()
        end_mem = psutil.Process(os.getpid()).memory_info().rss

        report = dict({
            "time_to_solve": end - start,
            "number_of_explored_state": len(game_solver.explored),
            "number_of_remain_state": game_solver.frontier.length(),
            "number_of_step": len(res),
            "consumption_memory": "{:.3f} B".format((end_mem - begin_mem) * 1e-3)
        })

        if res is not None:
            return dict({
                "solution": [action.name for action in res],
                "report": report
            })
        else:
            print("Cannot solve!")
            return None

    @staticmethod
    def genetic_solve(input_file_name, population_size, chromosome_length,
                      mutation_chance, cross_over_type, distance_fitness_type):

        game_board, state_bridges, initial_position = BloxorzSolver.parse_input_data(input_file_name)
        list_chromosome = []

        if not BloxorzChromosome.is_valid_distance_calculation_type(distance_fitness_type):
            raise Exception("Type of distance fitness calculation is invalid")
        if not BloxorzPopulation.is_valid_cross_over_type(cross_over_type):
            raise Exception("Type of cross over implementation is invalid")

        for i in range(0, population_size):
            dna = []
            for j in range(0, chromosome_length):
                index_action = random.randint(0, BlockAction.__len__() - 1)
                dna.append(list(BlockAction)[index_action])
            new_chromosome = BloxorzChromosome(dna, game_board, initial_position, state_bridges, distance_fitness_type)
            list_chromosome.append(new_chromosome)

        initial_population = BloxorzPopulation(list_chromosome, cross_over_type)
        genetic_solver = GeneticSolver(
            mutation_chance=mutation_chance,
            goal_fitness_score=0,
            initial_population=initial_population
        )

        start = time.time()
        goal_chromosomes = genetic_solver.solve()
        end = time.time()

        report_goal_chromosomes = []
        for chromosome in goal_chromosomes:
            if isinstance(chromosome, BloxorzChromosome):
                result = chromosome.get_valid_action()
                report_goal_chromosomes.append(
                    dict({
                        "number_of_step": len(result),
                        "steps": result
                    })
                )

        report = dict({
            "time_to_solve": end - start,
            "number_of_generation": initial_population.number_generation,
            "population_size": population_size,
            "chromosome_length": chromosome_length,
            "mutation_chance": mutation_chance,
            "cross_over_type": cross_over_type,
            "distance_fitness_type": distance_fitness_type,
            "report_all_goal_chromosomes": report_goal_chromosomes
        })

        if goal_chromosomes is not None:
            return dict({
                "solution": report_goal_chromosomes[0]["steps"],
                "report": report
            })
        else:
            print("Cannot solve!")
            return None

    @staticmethod
    def parse_input_data(input_file_name):
        """
        This function parses data from input file
        :param input_file_name:
        :return: game_board, state_bridges, initial_position
        """

        CURRENT_PATH = Path(__file__).parent
        with open(CURRENT_PATH.joinpath(f"./input/{input_file_name}")) as f:
            input_data = json.load(f)

        # Create bloxorz game board and initial position
        game_board = GameBoard(input_data["map"], input_data["bridges"])
        initial_position = input_data["initial_position"]
        initial_position = initial_position.split(" ")
        initial_position = tuple(int(pos) for pos in initial_position)

        try:
            state_bridges = input_data["state_bridges"]
            state_bridges = [bool(state) for state in state_bridges]
        except Exception as e:
            print(e)
            state_bridges = [False] * len(game_board.bridges)

        return game_board, state_bridges, initial_position
