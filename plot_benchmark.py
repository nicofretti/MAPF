import json
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":

    json_file = open('benchmark/result.json')
    data = json.load(json_file)
    x = [i + 5 for i in range(len(data))]
    stats = {
        'cbs': {
            'cpu_time': [],
            'unsolved': []
        },
        'cbs_disjoint': {
            'cpu_time': [],
            'unsolved': []
        },
    }
    algoritms = ['cbs', 'cbs_disjoint']
    # fix some stats like -1 for not don't computed
    for max_agents in data:
        for algo in algoritms:
            cpu = np.asarray(data[max_agents][algo]['cpu_time'])
            stats[algo]['unsolved'].append(np.count_nonzero(cpu == -1))
            cpu[cpu == -1] = 0
            data[max_agents][algo]['cpu_time'] = cpu

    # calc stats
    for max_agents in data:
        row = data[max_agents]
        for alg in algoritms:
            stats[alg]['cpu_time'].append(mean(row[alg]['cpu_time']))
    # ----- CPU time -----
    fig = plt.figure()
    #for alg in algoritms:
    #    plt.plot(x, stats[alg]['cpu_time'], label=alg)
    #plt.legend()
    #plt.show()

    # ----- Bar plot -----
    fig, ax = plt.subplots(2)
    fig.suptitle("Number of problem solved/unsolved by algorithm")
    x = 0
    plt.xlabel('Number of agents')
    plt.ylabel('Problems solved')
    for alg in algoritms:
        index = np.arange(len(stats[alg]['unsolved'])) + 5
        print(index)
        solved = [20 - i for i in stats[alg]['unsolved']]
        ax[0 if alg=="cbs" else 1].bar(index + x, solved,
                bottom=0,
                width=.5,
                label="solved {}".format(alg))
        ax[0 if alg=="cbs" else 1].bar(index + x, stats[alg]['unsolved'],
                 bottom=solved,
                 width=.5,
                 label="unsolved {}".format(alg))
        x += .5

        plt.legend()




    plt.tight_layout()
    plt.show()
