import json
import random
import sys
import time

from aisolver.blind.frontier import StackFrontier, QueueFrontier
from aisolver.blind.solver import Solver
from bloxorz.block import DoubleBlock
from bloxorz_state import BloxorzState
from bloxorz_chromosome import BlockAction, BloxorzChromosome
from bloxorz.game_board import GameBoard
from genetic_solver import Population, GeneticSolver

if len(sys.argv) != 3 and len(sys.argv) != 6:
    print("arguments: [input file name] [algorithm]")
    print("algorithm: dfs/bfs/genetic")
    print("algorithm == genetic, we need more parameter: [chromosome length] [population size] [mutation chance]")
    print("exit")
    sys.exit()

# Get data from json input file
input_file = "./input/" + sys.argv[1]
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

# Get AI algorithm
algorithm = sys.argv[2].upper()

if algorithm == "DFS" or algorithm == "BFS":
    frontier = None
    if algorithm == "DFS":
        frontier = StackFrontier()

    elif algorithm == "BFS":
        frontier = QueueFrontier()
    initial_state = BloxorzState(DoubleBlock(initial_position), state_bridges, game_board)
    game_solver = Solver(frontier, initial_state)
    res = game_solver.solve()
    if res is not None:
        print(f"Number of discovered state: {len(game_solver.explored)}")
        print(f"Number of step: {len(res)}")
        print(res)
    else:
        print("Cannot solve!")

elif algorithm == "GENETIC":
    population_size = int(sys.argv[3])
    chromosome_size = int(sys.argv[4])

    list_chromosome = []
    for i in range(0, population_size):
        dna = []
        for j in range(0, chromosome_size):
            index_action = random.randint(0, BlockAction.__len__() - 1)
            dna.append(list(BlockAction)[index_action])
        new_chromosome = BloxorzChromosome(dna, game_board, initial_position, state_bridges)
        list_chromosome.append(new_chromosome)

    initial_population = Population("MINIMIZE", list_chromosome)
    mutation_chance = float(sys.argv[5])

    genetic_solver = GeneticSolver(mutation_chance, 0, initial_population)

    start = time.time()
    goal_chromosome = genetic_solver.solve()
    end = time.time()

    print(f"Algorithm: {algorithm} \t Input: {input_file}")
    print(f"Population size: {population_size} \t- Chromosome length: {chromosome_size}\t - Mutation chance: {mutation_chance}")
    print(f"Time to solve: {end - start}")
    for ele in goal_chromosome:
        print(ele)
