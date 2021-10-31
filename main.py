import re
import os
from math import sqrt
import matplotlib.pyplot as plt


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
    f.readline()
    line = f.readline()
    numbers = re.findall("\d+", line)
    depot = int(numbers[0])
    return {'dimension': dimension, 'capacity': capacity, 'waypoints': waypoints, 'demands': demands, 'depot': depot-1}

def distance_matrix(waypoints):
    distance_matrix = []
    for i in range(len(waypoints)):
        distance_matrix.append([])
        for j in range(len(waypoints)):
            distance_matrix[i].append(sqrt((waypoints[i][0] - waypoints[j][0])**2 + (waypoints[i][1] - waypoints[j][1])**2))
    return distance_matrix

def compute_savings(depot, distances):
    savings = []
    for i in range(len(distances)):
        if i != depot:
            for j in range(len(distances)):
                if j != depot:
                    if i < j:
                        savings.append({'w1': i, 'w2': j, 'saving': distances[depot][j] + distances[i][depot] - distances[i][j]})
    return sorted(savings, key=lambda d: d['saving'], reverse=True)

def savings_algorithm(depot, distances, capacity, demands):
    savings = compute_savings(depot, distances)
    whatRoute = []
    for i in range(len(distances)):
        whatRoute.append({'waypoints': [i], 'length': 2*distances[0][i], 'demand': demands[i]})

    for i in range(len(savings)):
        saving = savings[i]
        w1 = saving['w1']
        w2 = saving['w2']
        route_1 = whatRoute[w1]
        route_2 = whatRoute[w2]
        if route_1 != route_2:
            if (route_1['demand'] + route_2['demand'] <= capacity):
                if (w1 == route_1['waypoints'][0] and w2 == route_2['waypoints'][-1]):
                    route = {'waypoints': route_2['waypoints'] + route_1['waypoints'], 'length': route_1['length'] + route_2['length'] - saving['saving'], 'demand': route_1['demand'] + route_2['demand']}
                    for wp in route_1['waypoints']:
                        whatRoute[wp] = route
                    for wp in route_2['waypoints']:
                        whatRoute[wp] = route
                elif (w1 == route_1['waypoints'][-1] and w2 == route_2['waypoints'][0]):
                    route = {'waypoints': route_1['waypoints'] + route_2['waypoints'], 'length': route_1['length'] + route_2['length'] - saving['saving'], 'demand': route_1['demand'] + route_2['demand']}
                    for wp in route_1['waypoints']:
                        whatRoute[wp] = route
                    for wp in route_2['waypoints']:
                        whatRoute[wp] = route

    bestRoutes = []
    for route in whatRoute:
        if not route in bestRoutes:
            bestRoutes.append(route)

    del bestRoutes[0]

    return bestRoutes




def main():
    files = os.listdir('Instances')
    for file in files:
        if 'vrp' in file:
            specs = readFile('Instances/' + file)
            distances = distance_matrix(specs['waypoints'])
            print("\n")
            print(file)
            routes = savings_algorithm(specs['depot'], distances, specs['capacity'], specs['demands'])
            for wp in specs['waypoints']:
                plt.plot(wp[0], wp[1], ".")

            for route in routes:
                coords_x = [specs['waypoints'][specs['depot']][0]] + [specs['waypoints'][wp][0] for wp in route['waypoints']] + [specs['waypoints'][specs['depot']][0]]
                coords_y = [specs['waypoints'][specs['depot']][1]] + [specs['waypoints'][wp][1] for wp in route['waypoints']] + [specs['waypoints'][specs['depot']][1]]
                print([(coords_x[i], coords_y[i]) for i in range(len(route['waypoints']) + 2)])
                plt.plot(coords_x, coords_y)
            plt.show()


main()
