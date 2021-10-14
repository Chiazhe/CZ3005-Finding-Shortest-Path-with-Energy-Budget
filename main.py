import json
from queue import PriorityQueue
import heapq
import math

def AStarSearch(start, end ,energy_limit):
    if start not in graph:
        print("Starting node",start,"is not in the graph.")
        return
    elif end not in graph:
        print("Ending node",end,"is not in the graph.")
        return
    open=[]
    closed={}
    end_coord = coord[start]
    heuristics={}
    for key,value in coord.items():
        heuristics[key]=math.sqrt((value[0]-end_coord[0])**2+(value[1]-end_coord[1])**2)
    fn = 0+heuristics[start]
    heapq.heappush(open,(fn,[start,0,0,None,None]))

    while len(open)>0:
        current_node_distance,current_node = heapq.heappop(open)

        if current_node[0]==end:
            path = str(end)
            parent_node = closed[current_node[3]][current_node[-1]]
            while parent_node[0]!= start:
                # print(parent_node[0])
                path = parent_node[0]+ "->"+ path
                parent_node= closed[parent_node[3]][parent_node[-1]]
            print(f"Shortest path: {start}->{path}")
            print("Shortest distance:",current_node[1])
            print("Total energy cost:", current_node[2])
            return
        neighbours = graph[current_node[0]]

        if current_node[0] not in closed:
            for neighbour in neighbours:
                if neighbour==current_node[3]:
                    continue
                else:
                    # add the neighbour as long as it is not the parent
                    cost = current_node[2]+costData[f"{current_node[0]},{neighbour}"]
                    gn = current_node[1]+distData[f"{current_node[0]},{neighbour}"]
                    needToInsert=True
                    for node_distance,node in open:
                        if node[0]==neighbour:
                            if (cost>=node[2] and gn>=node[1]):
                                needToInsert=False
                            break
                    if cost<=energy_limit and needToInsert:
                        parent_index=0
                        if (current_node[0] in closed):
                            parent_index = len(closed[current_node[0]])-1

                        fn = gn+ heuristics[neighbour] +cost/10
                        heapq.heappush(open,(fn,[neighbour,gn,cost,current_node[0],parent_index]))
        closed.setdefault(current_node[0],[]).append(current_node)


    print("Shortest path not found.")

def uniform_cost_search(source, destination):
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
            print('Route not found between '+source+' and ' +
                  destination+" at energy budget ")

        distance, route = pQueue.get()
        # currentNode is the current node we are at
        currentNode = route[len(route)-1]

        # Check if node is visited
        if currentNode not in visited:
            # Add current node into visited set
            visited.add(currentNode)

            # Destination is Reached and Check if the path is larger than the minimum path as of now
            if currentNode == destination:
                route.append(distance)
                return route

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

def uniform_cost_search_with_energy_limit(source, destination, energyLimit):
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
                    t_energy = costData[currentNode+","+n] + energy

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

def get_valid_number_input():
    user_input = input("\nSelect the task you want to run:\n1. Task 1\n2. Task 2\n3. Task 3\n0. Exit\n")
    while not user_input.isdigit():
        user_input = input(
            "Please only enter digit number. Try again.\nSelect the task you want to run:\n1. Task 1\n2. Task 2\n3. Task 3\n0. Exit\n")
    return user_input

# main function
if __name__ == '__main__':
    with open('Coord.json') as f:
        coord = json.load(f)

    with open('G.json') as f1:
        graph = json.load(f1)

    with open('Dist.json') as f2:
        distData = json.load(f2)

    with open('Cost.json') as f3:
        costData = json.load(f3)

    print("Task 1 output:")
    answer = uniform_cost_search('1', '50')
    print("Shortest path: " + "->".join(answer[:-1]))
    print("Shortest distance:",answer[-1])

    print("\nTask 2 output:")
    answer = uniform_cost_search_with_energy_limit('1', '50', 287932)
    print("Shortest path: " + "->".join(answer[:-2]))
    print("Shortest distance: "+ str(answer[-2]))
    print("Total energy cost: "+ str(answer[-1]))

    print("\nTask 3 output:")
    AStarSearch("1","50",287932)

    user_input = get_valid_number_input()

    while int(user_input)!=0:
        if int(user_input)==1:
            task1_start = input("Please enter the starting node in number:\n")
            while not task1_start.isdigit():
                task1_start = input(
                    "Please only enter digit number. Try again.\nPlease enter the starting node in number:\n")
            task1_end = input("Please enter the ending node in number:\n")
            while not task1_end.isdigit():
                task1_end = input(
                    "Please only enter digit number. Try again.\nPlease enter the ending node in number:\n")
            answer =uniform_cost_search(task1_start,task1_end)
            if (len(answer)>0):
                print("Shortest path: " + "->".join(answer[:-1]))
                print("Shortest distance:", answer[-1])
            user_input = get_valid_number_input()
        elif int(user_input)==2:
            task2_start = input("Please enter the starting node in number:\n")
            while not task2_start.isdigit():
                task2_start = input(
                    "Please only enter digit number. Try again.\nPlease enter the starting node in number:\n")
            task2_end = input("Please enter the ending node in number:\n")
            while not task2_end.isdigit():
                task2_end = input(
                    "Please only enter digit number. Try again.\nPlease enter the ending node in number:\n")
            task2_energy = input("Please enter the energy limit in number:\n")
            while not task2_energy.isdigit():
                task2_energy = input(
                    "Please only enter digit number. Try again.\nPlease enter the energy limit in number:\n")
            answer = uniform_cost_search_with_energy_limit(task2_start,task2_end,int(task2_energy))
            if (len(answer)>0):
                print("Shortest path: " + "->".join(answer[:-2]))
                print("Shortest distance: " + str(answer[-2]))
                print("Total energy cost: " + str(answer[-1]))
            user_input = get_valid_number_input()
        elif int(user_input) == 3:
            task3_start = input("Please enter the starting node in number:\n")
            while not task3_start.isdigit():
                task3_start = input(
                    "Please only enter digit number. Try again.\nPlease enter the starting node in number:\n")
            task3_end = input("Please enter the ending node in number:\n")
            while not task3_end.isdigit():
                task3_end = input(
                    "Please only enter digit number. Try again.\nPlease enter the ending node in number:\n")
            task3_energy = input("Please enter the energy limit in number:\n")
            while not task3_energy.isdigit():
                task3_energy = input(
                    "Please only enter digit number. Try again.\nPlease enter the energy limit in number:\n")
            AStarSearch(task3_start, task3_end, int(task3_energy))
            user_input = get_valid_number_input()
