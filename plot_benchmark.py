import json
import matplotlib.pyplot as plt
from statistics import mean
import numpy as np


if __name__=="__main__":

    json_file = open('benchmark/result.json')
    data = json.load(json_file)
    x = [i+5 for i in range(len(data))]
    stats = {'cbs':{'cpu_time':[], 'expanded':[]},\
             'cbs_disjoint':{'cpu_time':[], 'expanded':[]},\
             'prioritized':{'cpu_time':[], 'expanded':[]}
    }
    algoritms = ['cbs', 'cbs_disjoint']
    # fix some stats like -1 for not don't computed
    for max_agents in data:
        max_expanded= max(max(data[max_agents]['cbs']['expanded']), max(data[max_agents]['cbs_disjoint']['expanded']))
        max_cpu = max(max(data[max_agents]['cbs']['cpu_time']), max(data[max_agents]['cbs_disjoint']['cpu_time']))

        for algo in algoritms:
            cpu = np.asarray(data[max_agents][algo]['cpu_time'])
            expanded = np.asarray(data[max_agents][algo]['expanded'])
            expanded[expanded==-1] = max_expanded;cpu[cpu==-1] = max_cpu
            data[max_agents][algo]['cpu_time'] = cpu
            data[max_agents][algo]['expanded'] = expanded

    # calc stats
    for max_agents in data:
        row = data[max_agents]
        for alg in algoritms:
            stats[alg]['cpu_time'].append(mean(row[alg]['cpu_time']))
            if(alg != 'prioritized'):
                stats[alg]['expanded'].append(mean(row[alg]['expanded']))
    # ----- CPU time -----
    fig = plt.figure()
    for alg in algoritms:
        plt.plot(x,stats[alg]['cpu_time'],label=alg)
    plt.legend()
    plt.show()

    # ----- Bar plot -----
    fig, ax = plt.subplots()
    bar_width = 0.35
    opacity = 0.8
    bar = 0
    for alg in algoritms:
        index = np.arange(len(stats[alg]['expanded']))
        rects1 = plt.bar(index + bar, stats[alg]['expanded'], bar_width,
                         alpha=opacity,
                         label=alg)
        bar += bar_width

    plt.xlabel('Number of agents')
    plt.ylabel('Node expanded')
    plt.title('Node expanded by algorithm')
    plt.xticks(index + bar_width, x)
    plt.legend()

    plt.tight_layout()
    plt.show()

