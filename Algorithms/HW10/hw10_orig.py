from typing import List, Dict, Tuple, Any
from pathlib import Path
import heapq
import csv
from ast import literal_eval
import math
import queue
from timeit import default_timer as timer
from collections import deque
import random


class Vertex:
    def __init__(self, identifier: Any):
        self.identifier = identifier
        self.d = float("inf")
        self.pi = None
        self.color = "white"

def euclidean_dist(a,b):
    return math.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2 + (b[2]-a[2])**2)

def parse_universe(fpath=Path("/Users/archana/Dropbox/Algo/HW10/sde-universe_2018-07-16.csv")
                   ) -> Tuple[List[List[int]], Dict[int, str]]:

    # read in csv file build up dict of just system_id to adjacent id_S
    system_mapping = {}
    security_rating = {}
    coordinates = {}
    name_to_id: Dict[str, int] = {}
    with open(fpath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row["system_id"]) < 31000000:
                name_to_id[row["solarsystem_name"]] = int(row["system_id"])
                if not row["stargates"]:
                    row["stargates"] = "[]"
                system_mapping[int(row["system_id"])] = list(literal_eval(row["stargates"]))
                security_rating[int(row["system_id"])] = max(0.0, float(row['security_status']))
                coordinates[int(row["system_id"])] =  list((float(row["x"]),float(row["y"]),float(row["z"])))

    # dictionary referencing system_id to index position
    id_to_index = {system: index for index, system in enumerate(system_mapping.keys())}

    # constructing list of adjancency-list graph representations
    graph = [None] * len(system_mapping)
    for system, adjacents in system_mapping.items():
        graph[id_to_index[system]] = [id_to_index[neighbor] for neighbor in adjacents]
    
    # I need to know system names to index for future tracking
    name_to_index = {name: id_to_index[system_id] for name, system_id in name_to_id.items()}
    security_rating_id = {id_to_index[system_id]: seq for system_id, seq in security_rating.items()}
    coordinates_id = {id_to_index[system_id]: cord for system_id, cord in coordinates.items()}

    distances = {}
    for system_index, neighbor_list in enumerate(graph):
        for neighbors in neighbor_list:
            dist = euclidean_dist(coordinates_id[system_index], coordinates_id[neighbors])
            distances[(system_index,neighbors)] = dist

    return graph, name_to_index, security_rating_id, coordinates_id, distances

def backtrace(distances, node: Vertex) -> List[int]:
    """Method creates a list of elements that correspond to the order of progression
        
        Arguments:
        node {Vertex} -- Vertex to backtrace from
        
        Returns:
        List[int] -- reconstructing the back-pointers
        """
    path = [node.identifier]
    dist = 0
    while node.pi is not None:
        dist = dist + distances[node.pi.identifier,path[0]]
        path.insert(0, node.pi.identifier)
        node = node.pi
    return (dist,path)

def dijkstra(graph: List[List[int]], distances, source: int, destination: int
             ) -> List[int]:
    # initialization of the nodes
    vertices = [Vertex(index) for index, _ in enumerate(graph)]
    vertices[source].d = 0

    S = set()
    Q = queue.PriorityQueue()
    
    for index, _ in enumerate(graph):
        Q.put((vertices[index].d,vertices[index].identifier))

    while not Q.empty():
        d,u = Q.get()
        S.add(u)
        if u == destination:
            return backtrace(distances, vertices[destination])
        for adj_star in graph[u]:
            if vertices[adj_star].d > vertices[u].d + distances[u, adj_star]:
                vertices[adj_star].d = vertices[u].d + distances[u, adj_star]
                vertices[adj_star].pi = vertices[u]
                index = [y[1] for y in Q.queue].index(adj_star)
                update_priority(Q, index, adj_star, vertices[adj_star].d)

def parent(i):
    return (i-1)//2

def update_priority(Q, index, name, new_priority):
#    print('updating',new_priority, name)
    Q.queue[index] = (new_priority, name)
    while index > -1 and Q.queue[parent(index)][0] > Q.queue[index][0]:
#        print(parent(index))
        Q.queue[index],Q.queue[parent(index)] = Q.queue[parent(index)], Q.queue[index]
        index = parent(index)


def backtrace1(security, node: Vertex) -> List[int]:
    path = [node.identifier]
    final_sec = 0
    while node.pi is not None:
        final_sec = final_sec + security[path[0]]
        path.insert(0, node.pi.identifier)
        node = node.pi
    return (final_sec,path)

def dijkstra1(graph: List[List[int]], security, source: int, destination: int
             ) -> List[int]:
    # initialization of the nodes
    vertices = [Vertex(index) for index, _ in enumerate(graph)]
    vertices[source].d = 0
    
    S = set()
    Q = queue.PriorityQueue()
    
    for index, _ in enumerate(graph):
        Q.put((vertices[index].d,vertices[index].identifier))
    
    while not Q.empty():
        d,u = Q.get()
        S.add(u)
#        print('add', u)
        if u == destination:
            return backtrace1(security, vertices[destination])
        for adj_star in graph[u]:
#            print(adj_star,security[adj_star])
            if adj_star not in S:
                if vertices[adj_star].d > security[adj_star]:
                    vertices[adj_star].d = security[adj_star]
                    vertices[adj_star].pi = vertices[u]
                    index = [y[1] for y in Q.queue].index(adj_star)
                    update_priority(Q, index, adj_star, security[adj_star])


def q1_shortest_path(graph, distances, reverse_map, start: str, destination: str) -> List[str]:
    startt = timer()
    dist, jita_dodixie_route = dijkstra(graph, distances, start, destination)
    end = timer()
    print('Total time',end-startt)
    print('total distance', dist)
    route = [reverse_map[system] for system in jita_dodixie_route]
    return route

def q2_best_path(graph, security, reverse_map, start: str, destination: str) -> List[str]:
    startt = timer()
    final_sec, jita_dodixie_route = dijkstra1(graph, security, start, destination)
    end = timer()
    print('Total time',end-startt)
    print('total security', final_sec)
    route = [reverse_map[system] for system in jita_dodixie_route]
    return route

def question_3(systems, coordinates_id, max_distance):
    distance_matrix = [[euclidean_dist(coordinates_id[i], coordinates_id[j]) for i in systems] for j in systems]
    visited = breadth_first_search(distance_matrix, max_distance, 0)

    if set(systems) == set(visited):
        return True
    else:
        return False

def breadth_first_search(graph: List[List[int]], max_distance: int, source: int) -> List[int]:
    queue = []
    processed = []
    queue.append(source)
    while queue != []:
        u = queue.pop(0)
        if u not in processed:
            processed.append(u)
            for adj_star, distance in enumerate(graph[u]):
                if distance <= max_distance:
                    queue.append(adj_star)
    return processed

#def question_4(systems, coordinates_id):
#    distance_matrix = [[euclidean_dist(coordinates_id[i], coordinates_id[j]) for i in systems] for j in systems]
#    #    print(distance_matrix)
#    queue = []
#    processed = []
#    start = 0
#    finish = 0
#    good_indices = list(range(0,len(systems)))
#    #    print(good_indices)
#    final_min_dist = 0
#    queue.append(10)
#    while queue != []:
#        u = queue.pop(0)
#        if u not in processed:
#            processed.append(u)
#            row = distance_matrix[u]
#            good_indices.remove(u)
#            final_list = [row[i] for i in good_indices]
#            if final_list == []:
#                return final_min_dist,start,finish
#            min_dist = min(final_list)
#            #            print(min_dist)
#            minpos = distance_matrix [u].index(min_dist)
#            if min_dist > final_min_dist:
#                final_min_dist = min_dist
#                start = u
#                finish = minpos
#    queue.append(minpos)
#

def question_4(systems, coordinates_id,reverse_map):
    distance_matrix = [[euclidean_dist(coordinates_id[i], coordinates_id[j]) for i in systems] for j in systems]
#    print(distance_matrix)
    # initialization of the nodes
    final_min_dist = 0
    start = 0
    finish = 0
    total = len(systems)
    
    a = 0
    while a < 50:
        source = random.randint(0,total)
        vertices = [Vertex(index) for index, _ in enumerate(systems)]
        vertices[source].d = 0
        
        
        S = set()
        Q = queue.PriorityQueue()
        
        for index, _ in enumerate(systems):
            Q.put((vertices[index].d,vertices[index].identifier))
        num = 0
        while not Q.empty():
            d,u = Q.get()
            num = num + 1
#            print('popped',d,u)
            S.add(u)
            for adj_star,dist in enumerate(distance_matrix[u]):
                if adj_star in [y[1] for y in Q.queue] and dist < vertices[adj_star].d:
    #                print('distance',distance_matrix[u][adj_star])
                    vertices[adj_star].d = dist
                    vertices[adj_star].pi = vertices[u]
                    index = [y[1] for y in Q.queue].index(adj_star)
                    update_priority(Q, index, adj_star, dist)
                    if dist > final_min_dist:
                        final_min_dist = dist
                        start = u
                        finish = adj_star
        print(source,final_min_dist,reverse_map[start],reverse_map[finish])

    return final_min_dist,start,finish


def question1():
    graph, mapping, security, coordinates, distances  = parse_universe()
    reverse_map = {index: name for name, index in mapping.items()}
    route =  q1_shortest_path(graph, distances, reverse_map , mapping["6VDT-H"], mapping["Dodixie"])
#    route =  q2_best_path(graph, security, reverse_map , mapping["6VDT-H"], mapping["Dodixie"])
#    route =  q2_best_path(graph, security, reverse_map , mapping["Egmur"], mapping["Javrendei"])
#    route =  q2_best_path(graph, security, reverse_map , mapping["Pator"], mapping["Lustrevik"])#mapping["U6K-RG"]ahaq7,uivgh)
#    print(route)
#    print(coordinates)
#    systems = [index for name,index in mapping.items()]
##    max_distance = 1.0e+16
##    answer = question_3(systems,coordinates,max_distance)
##    print('Final answer: ',answer)
#    startt = timer()
#    answer,start,finish = question_4(systems,coordinates,reverse_map)
#    end = timer()
#    print('Total time',end-startt)
#    print('Final answer 4: ',answer)
#    print(reverse_map[start],reverse_map[finish])
#    print(reverse_map[0],reverse_map[1877])



def main():
    question1()

if __name__ == "__main__":
    main()
