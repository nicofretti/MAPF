import random
import time as timer
import heapq
from single_agent_planner import compute_heuristics, a_star, get_location, get_sum_of_cost

DEBUG = False


def normalize_paths(pathA, pathB):
    """
    given path1 and path2, finds the shortest path and pads it with the last location
    """
    path1 = pathA.copy()
    path2 = pathB.copy()
    shortest, pad = (path1, len(path2) - len(path1)) if len(path1) < len(path2) else (path2, len(path1) - len(path2))
    for _ in range(pad):
        shortest.append(shortest[-1])
    return path1, path2


def detect_collision(pathA, pathB):
    ##############################
    # Task 3.1: Return the first collision that occurs between two robot paths (or None if there is no collision)
    #           There are two types of collisions: vertex collision and edge collision.
    #           A vertex collision occurs if both robots occupy the same location at the same timestep
    #           An edge collision occurs if the robots swap their location at the same timestep.
    #           You should use "get_location(path, t)" to get the location of a robot at time t.
    # this function detects if an agent collides with another even after one of the two reached the goal
    path1, path2 = normalize_paths(pathA, pathB)
    length = len(path1)
    for t in range(length):
        # check for vertex collision
        pos1 = get_location(path1, t)
        pos2 = get_location(path2, t)
        if pos1 == pos2:
            # we return the vertex and the timestep causing the collision
            return [pos1], t, 'vertex'
        # check for edge collision (not if we are in the last timestep)
        if t < length - 1:
            next_pos1 = get_location(path1, t + 1)
            next_pos2 = get_location(path2, t + 1)
            if pos1 == next_pos2 and pos2 == next_pos1:
                # we return the edge and timestep causing the collision
                return [pos1, next_pos1], t + 1, 'edge'
    return None


def detect_collisions(paths):
    ##############################
    # Task 3.1: Return a list of first collisions between all robot pairs.
    #           A collision can be represented as dictionary that contains the id of the two robots, the vertex or edge
    #           causing the collision, and the timestep at which the collision occurred.
    #           You should use your detect_collision function to find a collision between two robots.
    collisions = []
    # i and j are agents
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            coll_data = detect_collision(paths[i], paths[j])
            # if coll_data is not None (collision detected)
            if coll_data:
                collisions.append({
                    'a1': i,
                    'a2': j,
                    'loc': coll_data[0],  # vertex or edge
                    'timestep': coll_data[1],  # timestep
                    'type': coll_data[2]
                })
    return collisions


def standard_splitting(collision):
    ##############################
    # Task 3.2: Return a list of (two) constraints to resolve the given collision
    #           Vertex collision: the first constraint prevents the first agent to be at the specified location at the
    #                            specified timestep, and the second constraint prevents the second agent to be at the
    #                            specified location at the specified timestep.
    #           Edge collision: the first constraint prevents the first agent to traverse the specified edge at the
    #                          specified timestep, and the second constraint prevents the second agent to traverse the
    #                          specified edge at the specified timestep
    # in this case, we can ignore final as all the paths are normalized
    constraints = []
    if collision['type'] == 'vertex':
        constraints.append({
            'agent': collision['a1'],
            'loc': collision['loc'],
            'timestep': collision['timestep'],
            'final': False
        })
        constraints.append({
            'agent': collision['a2'],
            'loc': collision['loc'],
            'timestep': collision['timestep'],
            'final': False
        })
    elif collision['type'] == 'edge':
        constraints.append({
            'agent': collision['a1'],
            'loc': collision['loc'],
            'timestep': collision['timestep'],
            'final': False
        })
        constraints.append({
            'agent': collision['a2'],
            # revesred returns an iterator. In python list == iterator returns false, not an error: nasty bug
            'loc': list(reversed(collision['loc'])),
            'timestep': collision['timestep'],
            'final': False
        })
    return constraints


def disjoint_splitting(collision):
    ##############################
    # Task 4.1: Return a list of (two) constraints to resolve the given collision
    #           Vertex collision: the first constraint enforces one agent to be at the specified location at the
    #                            specified timestep, and the second constraint prevents the same agent to be at the
    #                            same location at the timestep.
    #           Edge collision: the first constraint enforces one agent to traverse the specified edge at the
    #                          specified timestep, and the second constraint prevents the same agent to traverse the
    #                          specified edge at the specified timestep
    #           Choose the agent randomly
    choice = random.randint(0, 1)
    agents = [collision['a1'], collision['a2']]
    agent = agents[choice]
    loc = collision['loc'] if choice == 0 else list(reversed(collision['loc']))
    return [
        {
            'agent': agent,
            'loc': loc,
            'timestep': collision['timestep'],
            'positive': True,
            'final': False
        },
        {
            'agent': agent,
            'loc': loc,
            'timestep': collision['timestep'],
            'positive': False,
            'final': False
        }
    ]


def paths_violate_constraint(constraint, paths):
    ##############################
    # Task 4.3: compute the list of agents that violates the positive constraints
    # constraint:{'agent': 0, 'loc': [(2, 4)], 'timestep': 3, 'final': False, 'positive': False}
    # paths:[[(2, 1), ... (3, 4), (3, 5)], [(1, 2), ..., (4, 4)]]

    agents_violate = []
    if len(constraint['loc']) == 1:
        return vertex_check(constraint, paths)
    else:
        return edge_check(constraint, paths)

def vertex_check(constraint, paths):
    agents_violate = []
    for agent in range(len(paths)):
        if constraint['loc'][0] == get_location(paths[agent], constraint['timestep']):
            agents_violate.append(agent)
    return agents_violate

def edge_check(constraint, paths):
    agents_violate = []
    for agent in range(len(paths)):
        loc = [get_location(paths[agent], constraint['timestep'] - 1), get_location(paths[agent], constraint['timestep'])]
        if loc == constraint['loc'] or constraint['loc'][0] == loc[0] or constraint['loc'][1] == loc[1]:
            agents_violate.append(agent)
    return agents_violate



class CBSSolver(object):
    """The high-level search of CBS."""

    def __init__(self, my_map, starts, goals, max_time=None):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.start_time = 0
        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)

        self.num_of_generated = 0
        self.num_of_expanded = 0
        self.CPU_time = 0
        self.max_time =  max_time if max_time else float('inf')

        self.open_list = []
        self.cont = 0

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    def push_node(self, node):
        heapq.heappush(self.open_list, (node['cost'], len(node['collisions']), self.num_of_generated, node))
        if DEBUG:
            print("Generate node {}".format(self.num_of_generated))
        self.num_of_generated += 1

    def pop_node(self):
        _, _, id, node = heapq.heappop(self.open_list)
        if DEBUG:
            print("Expand node {}".format(id))
        self.num_of_expanded += 1
        return node

    def find_solution(self, disjoint=False):
        """ Finds paths for all agents from their start locations to their goal locations

        disjoint    - use disjoint splitting or not
        """
        self.start_time = timer.time()

        # Generate the root node
        # constraints   - list of constraints
        # paths         - list of paths, one for each agent
        #               [[(x11, y11), (x12, y12), ...], [(x21, y21), (x22, y22), ...], ...]
        # collisions     - list of collisions in paths
        root = {
            'cost': 0,
            'constraints': [],
            'paths': [],
            'collisions': []
        }
        for i in range(self.num_of_agents):  # Find initial path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, root['constraints'])
            if path is None:
                raise BaseException('No solutions')
            root['paths'].append(path)

        root['cost'] = get_sum_of_cost(root['paths'])
        root['collisions'] = detect_collisions(root['paths'])
        self.push_node(root)
        # Task 3.1: Testing
        if DEBUG:
            print(root['collisions'])

        # Task 3.2: Testing
        if DEBUG:
            for collision in root['collisions']:
                print(standard_splitting(collision))

        ##############################
        # Task 3.3: High-Level Search
        #           Repeat the following as long as the open list is not empty:
        #             1. Get the next node from the open list (you can use self.pop_node())
        #             2. If this node has no collision, return solution
        #             3. Otherwise, choose the first collision and convert to a list of constraints (using your
        #                standard_splitting function). Add a new child node to your open list for each constraint
        #           Ensure to create a copy of any objects that your child nodes might inherit

        while self.open_list and timer.time() - self.start_time < self.max_time:
            p = self.pop_node()
            # if there are no collisions, we found a solution
            if not p['collisions']:
                self.print_results(p)
                return p['paths']
            # we choose a collision and turn it into constraints
            collision = random.choice(p['collisions'])
            # 4.2 Adjusting the High-Level Search
            constraints = disjoint_splitting(collision) if disjoint else standard_splitting(collision)
            # HERE
            for c in constraints:
                skip_node = False
                q = {'cost': 0,
                     'constraints': [*p['constraints'], c],  # all constraints in p plus c
                     'paths': p['paths'].copy(),
                     'collisions': []
                     }
                agent = c['agent']
                path = a_star(self.my_map, self.starts[agent], self.goals[agent], self.heuristics[agent],
                              agent, q['constraints'])
                if path:
                    q['paths'][agent] = path
                    if c['positive']:
                        rebuild_agents = paths_violate_constraint(c, q['paths'])
                        for r_agent in rebuild_agents:
                            c_new = c.copy()
                            c_new['agent'] = r_agent
                            c_new['positive'] = False
                            q['constraints'].append(c_new)
                            r_path = a_star(self.my_map, self.starts[r_agent], self.goals[r_agent],
                                            self.heuristics[r_agent], r_agent,q['constraints'])
                            if r_path is None:
                                skip_node = True
                                break # at least one agents has none solution
                            else:
                                q['paths'][r_agent] = r_path
                    if(not skip_node):
                        q['collisions'] = detect_collisions(q['paths'])
                        q['cost'] = get_sum_of_cost(q['paths'])
                        self.push_node(q)
                else:
                    raise BaseException('No solutions')
        raise BaseException('Time limit exceeded')

    def print_results(self, node):
        pass
        #if DEBUG:
        #print("\n Found a solution! \n")
        #CPU_time = timer.time() - self.start_time
        #print("CPU time (s):    {:.2f}".format(CPU_time))
        #print("Sum of costs:    {}".format(get_sum_of_cost(node['paths'])))
        #print("Expanded nodes:  {}".format(self.num_of_expanded))
        #print("Generated nodes: {}".format(self.num_of_generated))
