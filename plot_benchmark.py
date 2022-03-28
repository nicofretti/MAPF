import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

ALGORITMS = ['cbs', 'cbs_disjoint']
THEME = 'darkgrid'

def plot_time_area(data, time_limit):
    """
    Plot cpu time of the be
    """
    keys = list(data.keys())
    start,finish = int(keys[0]), int(keys[-1])+2
    sns.set_theme(style=THEME)
    x_axis = [i for i in range(start,finish,2)]
    y_axis = []
    for alg in ALGORITMS:
        d = []
        for i in range(start,finish,2):
            sub = data[str(i)][alg]['cpu_time']
            sub = [time_limit if x == -1 else x for x in sub]
            d.append(sub)

        y_axis.append(d)
    # d is a list of lists
    std_of_mean = [] # standard error of the mean
    for alg in [0,1]:
        std_of_mean.append([])
        for i in range(len(y_axis[alg])):
            std_of_mean[alg].append(np.std(y_axis[alg][i], ddof=1) / np.sqrt(np.size(y_axis[alg][i])))
    cbs = np.array([np.mean(x) for x in y_axis[0]])
    cbs_disjoint = np.array([np.mean(x) for x in y_axis[1]])
    data = pd.DataFrame(
        data={
            'agents': x_axis,
            'cbs': cbs,
            'cbs_disjoint': cbs_disjoint
        }
    )
    plt = sns.lineplot(data=data.set_index('agents'), linewidth=2.5)
    plt.set(xlabel='Number of agents', ylabel='CPU time (s)')
    plt.axes.set_xticks(np.arange(start, finish, 2.0))
    # CBS area
    lower = cbs - std_of_mean[0]; upper = cbs + std_of_mean[0]
    plt.plot(x_axis, lower, color='tab:blue', alpha=0.2)
    plt.plot(x_axis, upper, color='tab:blue', alpha=0.2)
    plt.fill_between(x_axis, lower, upper, color='tab:blue', alpha=0.2)
    # CBS disjoint area
    lower = cbs_disjoint - std_of_mean[1]; upper = cbs_disjoint + std_of_mean[1]
    plt.plot(x_axis, lower, color='tab:orange', alpha=0.2)
    plt.plot(x_axis, upper, color='tab:orange', alpha=0.2)
    plt.fill_between(x_axis, lower, upper, color='tab:orange', alpha=0.2)
    plt.set(title='CPU time with standard error of the mean')

def plot_success_rate(data, time_limit):
    """
    Plot the success rate of the benchmark.
    """
    keys = list(data.keys())
    start,finish = int(keys[0]), int(keys[-1])+1
    max_tests = len(data[str(start)]['cbs']['cpu_time'])
    sns.set_theme(style=THEME)
    x_axis = [i for i in range(start,finish,2)]
    d = {}
    for alg in ALGORITMS:
        d[alg] = []
        for agents in data:
            success = 0
            for sample in data[agents][alg]['cpu_time']:
                if(sample != -1):
                    success += 1
            d[alg].append(success)
    data = pd.DataFrame(
        data={
            'agents': x_axis,
            'cbs': d['cbs'],
            'cbs_disjoint': d['cbs_disjoint']
        }
    )
    plt = sns.lineplot(data=data.set_index('agents'), linewidth=2.5)
    plt.set(xlabel='Number of agents', ylabel='Problems solved (target={})'.format(max_tests))
    plt.axes.set_xticks(np.arange(start, finish + 1, 2.0))
    plt.set(title='Success rate with time limit of {} minutes'.format(time_limit))

def plot_expanded_nodes(data, default_nodes= 1000):
    """
    Plot cpu time of the be
    """
    keys = list(data.keys())
    start,finish = int(keys[0]), int(keys[-1])+2
    sns.set_theme(style=THEME)
    x_axis = [i for i in range(start,finish,2)]
    y_axis = []
    for alg in ALGORITMS:
        d = []
        for i in range(start,finish,2):
            sub = data[str(i)][alg]['expanded']
            sub = [default_nodes if x == -1 else x for x in sub]
            d.append(np.mean(sub))
        y_axis.append(d)
    data = pd.DataFrame(
        data={
            'agents': x_axis,
            'cbs': y_axis[0],
            'cbs_disjoint': y_axis[1]
        }
    )
    plt = sns.lineplot(data=data.set_index('agents'), linewidth=2.5)
    plt.set(xlabel='Number of agents', ylabel='Expanded nodes')
    plt.axes.set_xticks(np.arange(start, finish, 2.0))
    plt.set(title='Mean of expanded nodes')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Runs various MAPF algorithms')
    parser.add_argument('--plot', type=str,
                        help='Select the plot to be generated, based on benchmark data {random, success}')
    args=parser.parse_args()
    if args.plot == 'random':
        # plot based on many random instances
        json_file = open('benchmark/result.json')
        data = json.load(json_file)
        plot_success_rate(data, 2)
        plt.show()
        plot_time_area(data, 60*2)
        plt.show()
        plot_expanded_nodes(data, 500)
        plt.show()
    if args.plot == 'success':
        # plot based of one map with different instances
        json_file = open('benchmark/result_success.json')
        data = json.load(json_file)
        plot_success_rate(data,5)
        plt.show()
        plot_time_area(data, 60*5)
        plt.show()
