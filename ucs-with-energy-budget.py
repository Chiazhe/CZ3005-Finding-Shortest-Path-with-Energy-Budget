import json
from queue import PriorityQueue

def uniform_cost_search(source, destination, energyLimit):
    if source not in graph.keys():
        print("Source node: "+source+" is not found in the graph!")
        return []

    if destination not in graph.keys():
        print("Destination node: "+destination+" is not found in the graph!")
        return []

    # Used to check if a node is visited or not
    visited = set()

    # Used to store the route in an increasing order of distance
    pQueue = PriorityQueue()
    pQueue.put((0, 0, 0, [source]))

    while pQueue:
        # No route exist between them in the case
        if pQueue.empty():
            print('Route not found between '+source+' and ' +
                  destination+" at energy budget " + str(energyLimit))
            return []

        compare_value, distance, energy, route = pQueue.get()

        # currentNode is the current node we are at
        currentNode = route[len(route)-1]

        # Check if node is visited
        if currentNode not in visited:
            # Add current node into visited set
            visited.add(currentNode)

            # Destination is Reached
            if currentNode == destination:
                route.append(distance)
                route.append(energy)
                return route

            # Get the neighbors of current node
            neighbors = graph[currentNode]
            for n in neighbors:
                if n not in visited:
                    # Total energy to this neighbor
                    t_energy = energyData[currentNode+","+n] + energy

                    # Total Distance to this neighbor
                    t_distance = distData[currentNode+","+n] + distance
                    # Array of the previous route before reaching this neighbor
                    temp = route[:]
                    # Add in this neighbor into the route
                    temp.append(n)

                    # Add the distance, energy and route for this neighbor for further explore later
                    if t_energy <= energyLimit:
                        pQueue.put((t_distance+t_energy/10,
                                   t_distance, t_energy, temp))

# main function
if __name__ == '__main__':
    with open('G.json') as f1:
        graph = json.load(f1)

    with open('Dist.json') as f2:
        distData = json.load(f2)

    with open('Cost.json') as f3:
        energyData = json.load(f3)

    answer = uniform_cost_search('1', '50', 287932)
    print("Shortest path: " + "->".join(answer[:-2]))
    print("Shortest distance: "+ str(answer[-2]))
    print("Total energy cost: "+ str(answer[-1]))
