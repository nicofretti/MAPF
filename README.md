### Multi-Agent Path Finding (MAPF)
The MAPF algorithm is used to find the shortest path between multiple agents without making any collision.

In this repo you can find the solution of the assignment given by (Sven Koenig)[http://idm-lab.org/project-p/project.html] that is composed of 5 tasks.
I've used the repository of (jzagoli)[https://github.com/jzagoli] that has already implemented the tasks 1 to 3 included.


### Task 4
The target of this taks is to implement the CBS (Conflict-Based Search) with Disjoint Splitting that means to
add the support of positive contraints to the CBS algorithm. The CBS algorithm use the negative contraints to
indicate conflicts between agents, the idea of the positive contraints is to force agents to be in a certain posizion
in the specified time.

### Task 5
In this task I've to benchmark the performance of MAPF solvers, I choose to make a custom benchmark that is
based on some random maps genereted in runtime.

In my solution there are the following steps:
- Generate a random map
- Check if the map has a solution, if not, generate a new one
- Solve the map with the MAPF solver (CBS and CBS+DS)

Those steps are repeated with different parameters, the parameters are:
- Number of agents (from 5 to 15)
- Size of the map (from 10 to 20)
- CPU time limit (calculated using some previuos results)

As the number of agents increases, the time CPU limit increases and the map size. The solution try ten problems for each
number of agents.

