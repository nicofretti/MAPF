import random

def random_map(height, width, agents, obstables_percentage):
    # Creates a random map with the given parameters
    map = [];starts = [];goals = []
    positions = [(x,y) for x in range(height) for y in range(width)]
    random.shuffle(positions)

    for _ in range(agents):
        starts.append(positions.pop())
        goals.append(positions.pop())

    for i in range(height):
        map.append([])
        for j in range(width):
            if (i,j) in starts or (i,j) in goals or random.random() > obstables_percentage:
                # mark as obstacle
                map[i].append(False)
            else:
                # free space
                map[i].append(True)
    return map, starts, goals

