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

def save_map(map, starts, goals, filename):
    # Saves the map to a file
    with open(filename, 'w') as f:
        f.write('{} {}\n'.format(len(starts)))
        for row in map:
            f.write('{}\n'.format(''.join(['@' if cell else '.' for cell in row])))
        for agent in range(len(starts)):
            f.write('{} {} {} {}\n'.format(starts[agent][0], starts[agent][1], goals[agent][0], goals[agent][1]))

if __name__== '__main__':
    # Generates a random map and saves it to a file
    map, starts, goals = random_map(10, 10, 5, 0.5)
    save_map(map, starts, goals, 'random_map.txt')
