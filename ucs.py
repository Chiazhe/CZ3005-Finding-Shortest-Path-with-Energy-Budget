import json
from queue import PriorityQueue

def uniform_cost_search(source, destination):
    minimumDistance = 99999999999999999
    ans=[]
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
    pQueue.put((0, [source]))

    while pQueue:
        # No route exist between them in the case
        if pQueue.empty():
            if len(ans) == 0:
                print('Route not found between '+source+' and ' +
                      destination+" at energy budget ")
            return ans
        distance, route = pQueue.get()
        # currentNode is the current node we are at
        currentNode = route[len(route)-1]

        # Check if node is visited
        if currentNode not in visited:
            # Add current node into visited set
            visited.add(currentNode)

            # Destination is Reached and Check if the path is larger than the minimum path as of now
            if currentNode == destination and distance < minimumDistance:
                print("found")
                minimumDistance = distance
                route.append(distance)
                ans= route
                visited.remove(currentNode)
                continue
                # return route

            # Get the neighbors of current node
            neighbors = graph[currentNode]
            for n in neighbors:
                if n not in visited:
                    # Total distance to this neighbor
                    t_distance = distData[currentNode+","+n] + distance

                    # Array of the previous route before reaching this neighbor
                    temp = route[:]
                    # Add in this neighbor into the route
                    temp.append(n)

                    # Add the distance and route for this neighbor for further explore later
                    pQueue.put((t_distance, temp))

# main function
if __name__ == '__main__':
    with open('G.json') as f1:
        graph = json.load(f1)

    with open('Dist.json') as f2:
        distData = json.load(f2)

    with open('Cost.json') as f3:
        costData = json.load(f3)

    answer = uniform_cost_search('1', '50')
    print(len(answer))
    print(answer)
