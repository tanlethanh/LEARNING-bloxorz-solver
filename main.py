import sys
import argparse
import psutil
import os
import time

from bloxorz.bloxorz_solver import BloxorzSolver


def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--level",
                        help="Game level: [1,33]",
                        type=int,
                        required=True)
    parser.add_argument("-a", "--algorithm",
                        help="Algorithm: dfs/bfs/genetic",
                        type=str,
                        required=True)
    parser.add_argument("-ps", "--population_size",
                        help="Genetic population size, default: 100",
                        type=int,
                        default=100)
    parser.add_argument("-cl", "--chromosome_length",
                        help="Genetic chromosome length, default: 20",
                        type=int,
                        default=20)
    parser.add_argument("-ct", "--cross_type",
                        help="Genetic population type: default/custom",
                        type=str,
                        default="default")
    parser.add_argument("-dt", "--distance_type",
                        help="Genetic distance calculation type: manhattan/maze" + ", default: manhattan",
                        type=str,
                        default="manhattan")
    parser.add_argument("-mc", "--mutation_chance",
                        help="Genetic mutation chance: range(0, 1), default: 0.1",
                        type=float,
                        default=0.1)

    args = parser.parse_args()
    return args


def process_input(args):
    input_file = f"input{args.level}.JSON"
    algo = args.algorithm.upper()
    result = {"algorithm": algo}
    result.update({"input_file": input_file})
    if result["algorithm"] == "DFS" or result["algorithm"] == "BFS":
        return result
    elif result["algorithm"] == "GENETIC":
        result.update({"population_size": args.population_size})
        result.update({"cross_type": args.cross_type})
        result.update({"chromosome_length": args.chromosome_length})
        result.update({"distance_type": args.distance_type})
        result.update({"mutation_chance": args.mutation_chance})
        return result
    else:
        print("Invalid input")
        sys.exit(-1)


parsed_input = parse_input()
input_arguments = process_input(parsed_input)

algorithm = input_arguments["algorithm"]
input_file_name = input_arguments["input_file"]

game_result = "None"
start = time.time()
begin_mem = psutil.Process(os.getpid()).memory_info().rss
if algorithm == "DFS" or algorithm == "BFS":
    game_result = BloxorzSolver.blind_solve(input_file_name, algorithm)


elif algorithm == "GENETIC":

    game_result = BloxorzSolver.genetic_solve(
        input_file_name,
        input_arguments["population_size"],
        input_arguments["chromosome_length"],
        input_arguments["mutation_chance"],
        input_arguments["cross_type"],
        input_arguments["distance_type"]
    )
end_mem = psutil.Process(os.getpid()).memory_info().rss
end = time.time()

# print(game_result)
print("Level: {}".format(parsed_input.level))
print("Algorithm: {}".format(algorithm))
# print('Solution: {}'.format(game_result['solution']))
print("Memory usage: {:.3f}".format((end_mem - begin_mem) * 1e-6), "MB")
print("Time to solve: {:.3f}".format(
    game_result['report']['time_to_solve']), "second")
print("Number of explored states: {}".format(
    game_result['report']['number_of_explored_state']))
print("Number of steps: {}".format(game_result['report']['number_of_step']))
