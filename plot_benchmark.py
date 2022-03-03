import json
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    benchmark = "success"
    algoritms = ['cbs', 'cbs_disjoint']
    if benchmark == "random":
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
        plt.suptitle('CPU time for CBS and CBS-disjoint')
        plt.xlabel('Number of agents')
        plt.ylabel('CPU time (s)')
        for alg in algoritms:
            plt.plot(x, stats[alg]['cpu_time'], label=alg)
        plt.tight_layout()
        plt.legend()
        plt.show()

        # ----- Bar plot -----
        fig, ax = plt.subplots(2)
        fig.suptitle("Number of problem solved/unsolved by algorithm")
        x = 0

        plot_index = 0
        for alg in algoritms:
            index = np.arange(len(stats[alg]['unsolved'])) + 5
            solved = [20 - i for i in stats[alg]['unsolved']]
            ax[plot_index].set_title(alg.upper())
            ax[plot_index].bar(index + x, solved,
                    bottom=0,
                    width=.5,
                    label="solved")
            ax[plot_index].bar(index + x, stats[alg]['unsolved'],
                     bottom=solved,
                     width=.5,
                     label="unsolved")
            ax[plot_index].legend()
            plot_index +=1
            x += .5
        plt.xlabel('Number of agents')
        plt.ylabel('Problems solved')
        plt.tight_layout()
        plt.show()
    else:
        json_file = open('benchmark/result_success.json')
        data = json.load(json_file)
        fig,ax = plt.subplots()
        ax.set_title('Success rate for CBS and CBS-disjoint')
        plt.xlabel('Number of agents')
        plt.ylabel('Success rate')
        x = [i for i in range(5, 25)]
        for alg in algoritms:
            ax.plot(x, [data[str(i)][alg][0] for i in range(5, 25)], label=alg)
        plt.legend()
        plt.show()
