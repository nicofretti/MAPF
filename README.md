### Multi-Agent Path Finding (MAPF)
The MAPF (Multi-Agent Path Finding) is the planning problem to find a path between multiple agents without making any collision. In this repo you can find the solution of the assignment given by [Sven Koenig](http://idm-lab.org/project-p/project.html) that is composed of 5 tasks. I've used the repository of [jzagoli](https://github.com/jzagoli) that has already implemented the tasks 1 to 3 included. Try the solution executing the following command:

```bash
python run_experiments.py --disjoint --random --solver CBS
```
<center>
    <img style="width:400px;height:400px;align-center" src="img/output.gif"/>
</center>



### Task 4
The target of this taks is to implement the CBS (Conflict-Based Search) with Disjoint Splitting that means (in a few words)
to add the support of positive contraints to the CBS algorithm. The CBS algorithm use the negative contraints to
indicate conflicts between agents, the idea of the positive contraints is to force agents to be in a certain posizion
in the specified time.

### Task 5
In this task I've to benchmark the performance of MAPF solvers, I choose to make a custom benchmark that is
based on some random maps genereted in runtime.

In my solution there are the following steps:
- Generate a random map
- Solve the map with the MAPF solver (CBS and CBS+DS)
- Increase the number of agents and repeat the process

##### Plot 1
The plot shows the time that the solver takes to solve the 25 random maps for each number of agents. The numbers of agents start from 5 to 20 and the time limit is set to 2 minutes. Every map is a 10x10 grid with a probability of 5% of obstacles for each cell.
<plt>
##### Plot 2
In this plot I've generated a random map with obstacles distributed in the 5% of the map. The idea is to increase the number of agents and see if the algoritm can solver the problem in less than 5 minutes. For each number of agents is used the same map for 25 times, but the start and goal positions randomly distributed. Idea taken from this [paper](http://idm-lab.org/bib/abstracts/papers/icaps19a.pdf)
<plt>
