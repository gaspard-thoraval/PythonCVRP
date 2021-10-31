import re

def readFile(filename):
    f = open(filename, "r")
    f.readline()
    f.readline()
    f.readline()
    line = f.readline()
    dimension = int(re.findall("\d+", line)[0])
    f.readline()
    line = f.readline()
    capacity = int(re.findall("\d+", line)[0])
    f.readline()
    waypoints = []
    for i in range(dimension):
        line = f.readline()
        numbers = re.findall("\d+", line)
        waypoints.append((int(numbers[1]), int(numbers[2])))
    f.readline()
    demands = []
    for i in range(dimension):
        line = f.readline()
        numbers = re.findall("\d+", line)
        demands.append(int(numbers[1]))
    return {'dimension': dimension, 'capacity': capacity, 'waypoints': waypoints, 'demands': demands}

