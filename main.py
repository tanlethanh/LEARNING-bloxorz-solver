import json
import random
import sys
import time

from aisolver.blind.frontier import StackFrontier, QueueFrontier
from aisolver.blind.solver import Solver
from bloxorz.block import DoubleBlock
from bloxorz_population import BloxorzPopulation
from bloxorz_state import BloxorzState
from bloxorz_chromosome import BlockAction, BloxorzChromosome
from bloxorz.game_board import GameBoard
from aisolver.genetic.solver import Population, GeneticSolver
import argparse


def parse_input():
    parser = argparse.ArgumentParser()
    msg = "Bloxorz solver"
    #     print("arguments: [input file name] [algorithm]")
    #     print("algorithm: dfs/bfs/genetic")
    #     print("algorithm == genetic, we need more parameter: [chromosome length] [population size] [mutation chance]")
    parser.add_argument("-l", "--Level", help="Game level: [1,33]", type=int, required=True)
    parser.add_argument("-a", "--Algorithm", help="Algorithm: dfs/bfs/genetic", type=str, required=True)
    parser.add_argument("-s", "--Size", help="Genetic population size, default: 100", type=int, default=100)
    parser.add_argument("-t", "--Type", help="Genetic population type trigger, default: 0", type=int, default=0)
    parser.add_argument("-m", "--Move", help="Genetic chromosome size, default: 20", type=int, default=20)
    parser.add_argument("-v", "--Version", help="Genetic distance calculation version: 1/2, default: 1", type=int,
                        default=1)
    parser.add_argument("-c", "--Mutation", help="Genetic mutation chance, default: 0.1", type=float, default=0.1)
    args = parser.parse_args()
    return args


# if len(sys.argv) != 3 and len(sys.argv) != 8:
#     print("arguments: [input file name] [algorithm]")
#     print("algorithm: dfs/bfs/genetic")
#     print("algorithm == genetic, we need more parameter: [chromosome length] [population size] [mutation chance]")
#     print("exit")
#     sys.exit()


def process_input(args):
    input_file = "./input/" + "input{}.JSON".format(args.Level)
    # Get data from json input file
    #     input_file = "./input/" + sys.argv[1]

    # Get AI algorithm
    algorithm = args.Algorithm.upper()
    result = {"algorithm": algorithm}
    result.update({"input_file": input_file})
    if result["algorithm"] == "DFS" or algorithm == "BFS":
        return result
    elif result["algorithm"] == "GENETIC":
        # result = {"Name": "GENETIC"}
        result.update({"population_size": args.Size})
        result.update({"population_type": args.Type})
        result.update({"chromosome_size": args.Move})
        result.update({"chromosome_distance_type": args.Version})
        result.update({"mutation_chance": args.Mutation})
        return result
    else:
        print("Invalid input")
        sys.exit()


input = parse_input()
input = process_input(input)

algorithm = input["algorithm"]
input_file = input["input_file"]

with open(input_file) as f:
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

# input = process_input(parse_input())
if algorithm == "DFS" or algorithm == "BFS":
    frontier = None
    if algorithm == "DFS":
        frontier = StackFrontier()

    elif algorithm == "BFS":
        frontier = QueueFrontier()
    initial_state = BloxorzState(DoubleBlock(initial_position), state_bridges, game_board)
    print("Hello")

    game_solver = Solver(frontier, initial_state)
    res = game_solver.solve()
    if res is not None:
        print(f"Number of discovered state: {len(game_solver.explored)}")
        print(f"Number of step: {len(res)}")
        print(res)
    else:
        print("Cannot solve!")

elif algorithm == "GENETIC":
    population_size = input["population_size"]
    population_type = input["population_type"]
    chromosome_size = input["chromosome_size"]
    chromosome_distance_type = input["chromosome_distance_type"]

    list_chromosome = []
    for i in range(0, population_size):
        dna = []
        print(i)
        for j in range(0, chromosome_size):
            index_action = random.randint(0, BlockAction.__len__() - 1)
            dna.append(list(BlockAction)[index_action])
        a = time.time()
        new_chromosome = BloxorzChromosome(dna, game_board, initial_position, state_bridges, chromosome_distance_type)
        b = time.time()
        print(b - a)
        list_chromosome.append(new_chromosome)
    if population_type == 0:
        initial_population = Population("MINIMIZE", list_chromosome)
    elif population_type == 1:
        initial_population = BloxorzPopulation("MINIMIZE", list_chromosome)
    mutation_chance = input["mutation_chance"]
    print("He")
    genetic_solver = GeneticSolver(mutation_chance, 0, initial_population)

    start = time.time()
    goal_chromosome = genetic_solver.solve()
    end = time.time()

    print(f"Algorithm: {algorithm} \t Input: {input_file}")
    print(f"Population size: {population_size}"
          f"\t- Chromosome length: {chromosome_size}"
          f"\t - Mutation chance: {mutation_chance}")
    print(f"Time to solve: {end - start}")
    for ele in goal_chromosome:
        print(ele)
    # print(f"Number of generation: {initial_population.number_generation}")
