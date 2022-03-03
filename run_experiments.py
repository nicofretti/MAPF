#!/usr/bin/python
import argparse
import glob
from pathlib import Path
from cbs import CBSSolver
from independent import IndependentSolver
from prioritized import PrioritizedPlanningSolver
from random_instance import random_map, save_map, correct_random_map
from visualize import Animation
from single_agent_planner import get_sum_of_cost
import os
import time as timer

SOLVER = "CBS"


def print_mapf_instance(my_map, starts, goals):
    print('Start locations')
    print_locations(my_map, starts)
    print('Goal locations')
    print_locations(my_map, goals)


def print_locations(my_map, locations):
    starts_map = [[-1 for _ in range(len(my_map[0]))] for _ in range(len(my_map))]
    for i in range(len(locations)):
        starts_map[locations[i][0]][locations[i][1]] = i
    to_print = ''
    for x in range(len(my_map)):
        for y in range(len(my_map[0])):
            if starts_map[x][y] >= 0:
                to_print += str(starts_map[x][y]) + ' '
            elif my_map[x][y]:
                to_print += '@ '
            else:
                to_print += '. '
        to_print += '\n'
    print(to_print)


def import_mapf_instance(filename):
    f = Path(filename)
    if not f.is_file():
        raise BaseException(filename + " does not exist.")
    f = open(filename, 'r')
    # first line: #rows #columns
    line = f.readline()
    rows, columns = [int(x) for x in line.split(' ')]
    rows = int(rows)
    columns = int(columns)
    # #rows lines with the map
    my_map = []
    for r in range(rows):
        line = f.readline()
        my_map.append([])
        for cell in line:
            if cell == '@':
                my_map[-1].append(True)
            elif cell == '.':
                my_map[-1].append(False)
    # #agents
    line = f.readline()
    num_agents = int(line)
    # #agents lines with the start/goal positions
    starts = []
    goals = []
    for a in range(num_agents):
        line = f.readline()
        sx, sy, gx, gy = [int(x) for x in line.split(' ')]
        starts.append((sx, sy))
        goals.append((gx, gy))
    f.close()
    return my_map, starts, goals
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs various MAPF algorithms')
    parser.add_argument('--instance', type=str, default=None,
                        help='The name of the instance file(s)')
    parser.add_argument('--random', action='store_true', default=False,
                        help='Use a random map with auto-genereted agents (see function random_map)')
    parser.add_argument('--benchmark', action='store_true', default=False,
                        help='Runs on benchmark mode')
    parser.add_argument('--batch', action='store_true', default=False,
                        help='Use batch output instead of animation')
    parser.add_argument('--disjoint', action='store_true', default=False,
                        help='Use the disjoint splitting')
    parser.add_argument('--solver', type=str, default=SOLVER,
                        help='The solver to use (one of: {CBS,Independent,Prioritized}), defaults to ' + str(SOLVER))

    args = parser.parse_args()

    result_file = open("results.csv", "w", buffering=1)
    test = 15
    if args.benchmark:
        # Benchmark mode
        map_size = 10;obstacles_dist = .2
        experiment = 0
        result = {}
        start_agents = 5
        for max_agents in range(start_agents, 16):
            result[max_agents] = {'cbs': {'cpu_time':[-1]*test, 'expanded':[-1]*test, 'generated':[-1]*test},
                                  'cbs_disjoint': {'cpu_time':[-1]*test, 'expanded':[-1]*test, 'generated':[-1]*test},
                                  'prioritized': {'cpu_time': [-1] * test, 'expanded': [-1] * test, 'generated': [-1] *test}
                                  }
            for _ in range(test):
                experiment += 1
                print(experiment)
                my_map, starts, goals = correct_random_map(map_size, map_size, start_agents, obstacles_dist)
                filename = "benchmark/max_agents_{}/test_{}.txt".format(max_agents, _)
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                save_map(my_map, starts, goals, filename)
                for alg in ['cbs','cbs_disjoint','prioritized']:
                    solver =  PrioritizedPlanningSolver(my_map,starts,goals,60*2) if alg == 'prioritized' else CBSSolver(my_map,starts,goals,60*2)
                    try:
                        if alg == "prioritized":
                            solver.find_solution()
                        else:
                            solver.find_solution(alg=='cbs_disjoint')
                        result[max_agents][alg]['cpu_time'][_] = round(timer.time() - solver.start_time,2)
                    except BaseException as e:
                        # Timeout
                        result[max_agents][alg]['cpu_time'][_] = 120
                    result[max_agents][alg]['expanded'][_] = solver.num_of_expanded
                    result[max_agents][alg]['generated'][_] = solver.num_of_generated
        with open('benchmark/result.json', 'w') as outfile:
            json.dump(result, outfile)
    else:
        # Otherwise, run the algorithm
        files = ["random.generated"] if args.random else glob.glob(args.instance)
        for file in files:
            print("***Import an instance***")
            my_map, starts, goals = random_map(10, 10, 10, .2) if args.random else import_mapf_instance(file)
            print_mapf_instance(my_map, starts, goals)
            save_map(my_map, starts, goals, 'img/output_map.txt')
            if args.solver == "CBS":
                print("***Run CBS***")
                cbs = CBSSolver(my_map, starts, goals)
                paths = cbs.find_solution(args.disjoint)
            elif args.solver == "Independent":
                print("***Run Independent***")
                solver = IndependentSolver(my_map, starts, goals)
                paths = solver.find_solution()
            elif args.solver == "Prioritized":
                print("***Run Prioritized***")
                solver = PrioritizedPlanningSolver(my_map, starts, goals)
                paths = solver.find_solution()
            else:
                raise RuntimeError("Unknown solver!")

            cost = get_sum_of_cost(paths)
            result_file.write("{},{}\n".format(file, cost))

            if not args.batch:
                print("***Test paths on a simulation***")
                animation = Animation(my_map, starts, goals, paths)
                animation.save("output.mp4", 1.0)
                animation.show()
    print("***Done***")
    result_file.close()
