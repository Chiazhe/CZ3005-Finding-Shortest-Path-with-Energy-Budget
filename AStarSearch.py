import heapq
# customers = []
# heapq.heappush(customers, (3.4, ["Harry",4]))
# heapq.heappush(customers, (3.3, ["epng",5]))
# heapq.heappush(customers, (3.5, ["325",5]))
#
# # print(customers[-1])
# # customers[1]=customers[-1]
# # print(customers)
# # customers.pop()
# #
# # print(customers)
# # heapq.heappop(customers)
# # x,y =heapq.heappop(customers)
# # print(y)
# # heapq.heappush(customers, (1, "Riya"))
# # heapq.heappush(customers, (4, "Stacy"))
# customers[1]= (3.2,[])
# # heapq.heapify(customers)
# print(heapq.heappop(customers))
# for i,j in enumerate(customers) :
#     print(i,j)
# # print(customers)

# node structure = [name, actual distance from start, energy, parent,parent_index]
import heapq
import json
import math
import time

with open('Coord.json') as f:
    coord= json.load(f)

with open('G.json') as f1:
    graph = json.load(f1)

with open('Dist.json') as f2:
    distData = json.load(f2)

with open('Cost.json') as f3:
    costData = json.load(f3)

def main(start, end):
    open=[]
    closed={}
    end_coord = coord[start]
    heuristics={}
    for key,value in coord.items():
        heuristics[key]=math.sqrt((value[0]-end_coord[0])**2+(value[1]-end_coord[1])**2)
    # graph ={"S": ["A", "B"],"A": ["S", "B", "D"],"B": ["S", "A"],"D": ["A", "F"],"F": ["D"]}
    # distData={"S,A": 2,"S,B": 2,"A,S": 2,"A,B": 2,"A,D": 3,"B,S": 2,"B,A": 2,"D,A": 3,"D,F": 5,"F,D": 5}
    # costData={"S,A": 8,"S,B": 2,"A,S": 8,"A,B": 2,"A,D": 4,"B,S": 2,"B,A": 2,"D,A": 4,"D,F": 6,"F,D": 6}
    # heuristics={"S": 9,"A": 5,"B": 4,"D": 3,"F": 0}
    fn = 0+heuristics[start]
    heapq.heappush(open,(fn,[start,0,0,None,None]))


    energy_limit = 287932
    while len(open)>0:
        current_node_distance,current_node = heapq.heappop(open)
        # print(current_node)
        closed.setdefault(current_node[0],[]).append(current_node)
        if current_node[0]==end:
            #print the path
            print("found")
            print("distance:",current_node[1])
            print("cost:", current_node[2])
            print(end)
            parent_node = closed[current_node[3]][current_node[-1]]
            while parent_node[0]!= start:
                print(parent_node[0])
                parent_node= closed[parent_node[3]][parent_node[-1]]
            print(start)
            return
        neighbours = graph[current_node[0]]

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

                    fn = gn+ heuristics[neighbour]
                    heapq.heappush(open,(fn,[neighbour,gn,cost,current_node[0],parent_index]))

start= time.time()
main("1","50")
print(time.time()-start)