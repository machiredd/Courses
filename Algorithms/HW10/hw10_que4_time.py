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
import heapq
import itertools

############################## Question 1 ########################################
class Vertex:
    def __init__(self, identifier: Any):
        self.identifier = identifier
        self.d = float("inf")
        self.pi = None
        self.color = "white"

def euclidean_dist(a: [List[float]],b: [List[float]]) -> float :
    """Method will calculate Euclidean distance
        
    Arguments:
        a {[List[float]]} -- List containing x,y,z coordinates of system A
        b {[List[float]]} -- List containing x,y,z coordinates of system B
        
    Returns:
        Float -- Euclidean distance between system A and system B
    """
    return math.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2 + (b[2]-a[2])**2)

def parse_universe(fpath=Path("/Users/archana/Dropbox/Algo/HW10/sde-universe_2018-07-16.csv")
                   ) -> Tuple[List[List[int]], Dict[int, str]]:
    """Method will parse the CSV file and build up a graph representation of the eve universe used for que 1 and 2
        
    Keyword Arguments:
        fpath {[type]} -- path to the csv object ot import (default: {Path("sde-universe_2018-07-16.csv")})
        
    Returns:
        graph Tuple[List[List[int]] -- An adjacency list reprenting the graph in the Eve Universe
        name_to_index Dict[int, str] -- A dictionary with keys of indexes in the adjacency list, and values as the system names
        security_rating_id {Dict[int, float]} -- Security rating for different systems
        distances {Dict[(int, int),float]} -- Distance between two systems
        
    """

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

    return graph, name_to_index, security_rating_id, distances


class PriorityQueue_update(object):
    def __init__(self, pq):
        self.heap = pq
        self.entry_finder = dict({i[-1]: i for i in pq})
        self.REMOVED = 1000000000000
        self.counter = itertools.count()
    
    def add_task(self, task, priority=0):
        if task in self.entry_finder:
            self.delete(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.heap, entry)
    
    def remove_task(self, task):
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED
    
    def pop_task(self):
        while self.heap:
            priority, count , task = heapq.heappop(self.heap)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return priority, count, task
        raise KeyError('pop from an empty priority queue')

def backtrace(distances, node: Vertex):
    """Method creates a list of elements that correspond to the order of progression
        
        Arguments:
        distances {Dict[(int, int),float]} -- Distance between two vertices
        node {Vertex} -- Vertex to backtrace from
        
        Returns:
        dist[float] -- Total path distance
        List[int] -- reconstructing the back-pointers
    """
    path = [node.identifier]
    dist = 0
    while node.pi is not None:
        dist = dist + distances[node.pi.identifier,path[0]]
        path.insert(0, node.pi.identifier)
        node = node.pi
    return (dist,path)


def dijkstra(graph, distances, source: int, destination: int
             ) -> List[int]:
    """Method calculates shortest path from a single source
        
        Arguments:
        graph {List[List[int]]} -- The adjacensy list representation of the graph
        distances {Dict[(int, int),float]} -- Distance between two vertices
        source {int} -- The system index of the starting system
        destination {int} -- The system index of the destination system
        
        Returns:
        List[int] -- The list of system indexes representing the shortest path from the source to target destination
        """
    # initialization of the nodes
    vertices = [Vertex(index) for index, _ in enumerate(graph)]
    vertices[source].d = 0
    
    S = set()
    Q = queue.PriorityQueue()
    
    for index, _ in enumerate(graph):
        Q.put([vertices[index].d, 0, vertices[index].identifier])
    
    pq = PriorityQueue_update(Q.queue)
    
    while len(pq.heap) > len(S):
        d,_,u = pq.pop_task()
        S.add(u)
        if u == destination:
            return backtrace(distances, vertices[destination])
        for adj_star in graph[u]:
            if vertices[adj_star].d > vertices[u].d + distances[u, adj_star]:
                vertices[adj_star].d = vertices[u].d + distances[u, adj_star]
                vertices[adj_star].pi = vertices[u]
                pq.remove_task(adj_star)
                pq.add_task(adj_star,vertices[adj_star].d)

###################################### Question 2 #####################################

def backtrace_2(security: Dict[int, float], node: Vertex) -> (float, List[int]):
    """Method creates a list of elements that correspond to the order of progression
        
        Arguments:
        security {Dict[int, float]} -- Security rating for different systems
        node {Vertex} -- Vertex to backtrace from
        
        Returns:
        final_sec[float] -- Total security along the path
        List[int] -- reconstructing the back-pointers
        """
    path = [node.identifier]
    final_sec = security[path[0]]
    while node.pi is not None:
        path.insert(0, node.pi.identifier)
        final_sec = max(final_sec,security[path[0]])
        node = node.pi
    return (final_sec,path)


def dijkstra_2(graph: List[List[int]], security: Dict[int, float], source: int, destination: int,mapping
              ) -> (float, List[int]):
    # initialization of the nodes
    vertices = [Vertex(index) for index, _ in enumerate(graph)]
    vertices[source].d = 0
    
    S = set()
    Q = queue.PriorityQueue()
    
    for index, _ in enumerate(graph):
        Q.put([vertices[index].d, 0,vertices[index].identifier])

    pq = PriorityQueue_update(Q.queue)
    while len(pq.heap) > len(S):
        d,_,u = pq.pop_task()
        S.add(u)
        if u == destination:
            return backtrace_2(security, vertices[destination])
        for adj_star in graph[u]:
            if adj_star not in S:
                if vertices[adj_star].d > max(vertices[u].d, security[adj_star]):
                    vertices[adj_star].d = max(vertices[u].d, security[adj_star])
                    vertices[adj_star].pi = vertices[u]
                    pq.remove_task(adj_star)
                    pq.add_task(adj_star,security[adj_star])

###################################### Question 3 #####################################

def parse_universe_4(fpath=Path("/Users/archana/Dropbox/Algo/HW10/sde-universe_2018-07-16.csv")
                     ) ->  (Dict[int, str], Dict[int,List[float]]):
    """Method will parse the CSV file and build up a graph representation of the eve universe
        
        Keyword Arguments:
        fpath {[type]} -- path to the csv object ot import (default: {Path("sde-universe_2018-07-16.csv")})
        
        Returns:
        name_to_index Dict[int, str] -- Dictionary with keys of indexes in the adjacency list, and values as the system names
        coordinates_id Dict[int, List[float]] -- Dictionary with keys of system indices and values of their x,y,z coordinates
        """
    
    # read in csv file build up dict of just system_id to adjacent id_S
    system_mapping = {}
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
                coordinates[int(row["system_id"])] =  list((float(row["x"]),float(row["y"]),float(row["z"])))

    # dictionary referencing system_id to index position
    id_to_index = {system: index for index, system in enumerate(system_mapping.keys())}
    
    # I need to know system names to index for future tracking
    name_to_index = {name: id_to_index[system_id] for name, system_id in name_to_id.items()}
    coordinates_id = {id_to_index[system_id]: cord for system_id, cord in coordinates.items()}
    
    return name_to_index, coordinates_id


def question_3(max_distance):
    mapping, coordinates = parse_universe_4()
    reverse_map = {index: name for name, index in mapping.items()}
    systems = [index for name,index in mapping.items()]
    print('Max Distance:', max_distance)
    
    ### Compute adjacency matrix
    distance_matrix = [[euclidean_dist(coordinates[i], coordinates[j]) for i in systems] for j in systems]
    visited = breadth_first_search(distance_matrix, max_distance, systems[0])
    
    if set(systems) == set(visited):
        return True
    else:
        return False

def breadth_first_search(graph: List[List[int]], max_distance: int, source: int) -> List[int]:
    """Perform BFS on the graph,
        
        Arguments:
        graph {List[List[int]]} -- The adjacensy list representation of the graph
        max_distance {int} -- Maximum distance allowed between two systems
        source {int} -- The system index of the starting system
        
        Returns:
        List[int] -- The list of system indexes representing the shortest path from the source to all reachable systems
        """
    # initialization of the nodes
    vertices = [Vertex(index) for index, _ in enumerate(graph)]
    vertices[source].color = "gray"
    vertices[source].d = 0
    
    
    queue = []
    processed = []
    queue.append(source)
    while queue != []:
        u = queue.pop(0)
        processed.append(u)
        for adj_star, distance in enumerate(graph[u]):
            if vertices[adj_star].color == 'white':
                if distance <= max_distance:
                    vertices[adj_star].color = 'gray'
                    vertices[adj_star].d = vertices[u].d + distance
                    vertices[adj_star].pi = vertices[u]
                    queue.append(adj_star)
        vertices[u].color = 'black'
    return processed

###################################### Question 4 #####################################

#def backtrace_4(distance, node: Vertex) -> (float, List[int]):
#    """Method creates a list of elements that correspond to the order of progression
#        
#        Arguments:
#        security {Dict[int, float]} -- Security rating for different systems
#        node {Vertex} -- Vertex to backtrace from
#        
#        Returns:
#        final_sec[float] -- Total security along the path
#        List[int] -- reconstructing the back-pointers
#        """
#    path = [node.identifier]
#    max_dist = 0
#    start_in = 0
#    finish_in = 0
#    while node.pi is not None:
#        print('yes')
#        if distance[node.pi.identifier][path[0]] > max_dist:
#            print('enter')
#            max_dist = distance[node.pi.identifier][path[0]]
#            start_in = node.pi.identifier
#            finish_in = path[0]
#        path.insert(0, node.pi.identifier)
#        node = node.pi
#    print(path)
#    return (max_dist,start_in,finish_in)



#def question_4(systems: [List[int]], coordinates_id: Dict[int, List[float]],reverse_map: Dict[int,str]):
#    """Implements Prim's Algorithm starting from 50 different start points
#        
#        Arguments:
#        systems {List[int]} -- List of all systems
#        coordinates_id {Dict[int, List[float]]} -- Dictionary containg the x,y,z coordinates of all systems
#        reverse_map {Dict[int,str]} -- Mapping from system index to system name
#        
#        Returns:
#        Final_min_dist[float] -- Returns the final minimal distance
#        start[int] -- System index of the star from which the longest path starts
#        finish[int] -- System index of the star at which the longest path ends
#        """
#    
#    distance_matrix = [[euclidean_dist(coordinates_id[i], coordinates_id[j]) for i in systems] for j in systems]
#    #    print(distance_matrix)
#    
#    # initialization of the nodes
#    final_min_dist = 1.0e+25
#    start = 0
#    finish = 0
#    
##    for i,_ in enumerate(systems):
##        source = i
#    for i in [1]:
##        source = random.randint(0,len(systems))
#        source = 0
#        # initialization of the nodes
#        vertices = [Vertex(index) for index, _ in enumerate(systems)]
#        vertices[source].d = 0
##        max_dist = 0
##        start_in = 0
##        finish_in = 0
#
#        S = set()
#        Q = queue.PriorityQueue()
#        
#        for index, _ in enumerate(systems):
#            Q.put([vertices[index].d,0,vertices[index].identifier])
#    
#        pq = PriorityQueue_update(Q.queue)
#
#        while len(pq.heap) > len(S):
#            d,_,u = pq.pop_task()
#            S.add(u)
#            print('popping',u)
##            for adj_star, dist in enumerate(distance_matrix[u]):
#            for adj_star,_ in enumerate(systems):
##                if adj_star not in S:
##                    if vertices[adj_star].d > vertices[u].d + dist:
##                        vertices[adj_star].d = vertices[u].d + dist
#                if vertices[adj_star].d > vertices[u].d + euclidean_dist(coordinates_id[u], coordinates_id[adj_star]):
#                    vertices[adj_star].d = vertices[u].d + euclidean_dist(coordinates_id[u], coordinates_id[adj_star])
#                    vertices[adj_star].pi = vertices[u]
#                    pq.remove_task(adj_star)
#                    pq.add_task(adj_star,vertices[adj_star].d)
#                    print('adding',adj_star)
##                        if dist > max_dist:
##                            max_dist = dist
##                            start_in = u
##                            finish_in = adj_star
##        print(len(S),u,vertices[u].pi.identifier)
##        print(vertices[vertices[u].pi.identifier].pi)
##        print(vertices[vertices[u].pi.identifier].pi.identifier)
#        max_dist,start_in,finish_in = backtrace_4(distance_matrix, vertices[u])
##        print('max',max_dist,final_min_dist)
#        if max_dist < final_min_dist:
#            final_min_dist = max_dist
#            start = start_in
#            finish = finish_in
#        print(source,final_min_dist,reverse_map[start],reverse_map[finish])
#    
#    return final_min_dist,start,finish

#def backtrace_4( node: Vertex, coordinates_id) -> (float, List[int]):
#    """Method creates a list of elements that correspond to the order of progression
#        
#        Arguments:
#        security {Dict[int, float]} -- Security rating for different systems
#        node {Vertex} -- Vertex to backtrace from
#        
#        Returns:
#        final_sec[float] -- Total security along the path
#        List[int] -- reconstructing the back-pointers
#        """
#    path = [node.identifier]
#    while node.pi is not None:
#        path.insert(0, node.pi.identifier)
#        node = node.pi
#    return (max_dist,start_in,finish_in)
#
#
#
#def question_4(systems, coordinates_id,mapping):
##    distance_matrix = [[euclidean_dist(coordinates_id[i], coordinates_id[j]) for i in systems] for j in systems]
#    graph = [[i for i,_ in enumerate(systems)]] * len(systems)
#    
##    final_min_dist = 1.0e+25
##    start = 0
##    finish = 0
#
##    for i,_ in enumerate(systems):
#    source = 0
#
#    max_dist = 0
#    start_in = 0
#    finish_in = 0
#
#    vertices = [Vertex(index) for index, _ in enumerate(graph)]
#    vertices[source].d = 0
#    
#    S = set()
#    Q = queue.PriorityQueue()
#    
#    for index, _ in enumerate(graph):
#        Q.put([vertices[index].d, 0,vertices[index].identifier])
#    
#    good_indices = list(range(0,len(systems)))
#    
#    pq = PriorityQueue_update(Q.queue)
#    while len(pq.heap) > len(S):
#        print(len(S),max_dist)
#        d,_,u = pq.pop_task()
#        S.add(u)
#        good_indices.remove(u)
#        for adj_star in good_indices:
#            dist = euclidean_dist(coordinates_id[u], coordinates_id[adj_star])
#            if adj_star in [a[2] for a in pq.heap] and dist < vertices[adj_star].d:
#                vertices[adj_star].d = dist
#                vertices[adj_star].pi = vertices[u]
#                pq.remove_task(adj_star)
#                pq.add_task(adj_star,vertices[adj_star].d)
#                if dist > max_dist:
#                    max_dist = dist
#                    start_in = u
#                    finish_in = adj_star
##        if max_dist < final_min_dist:
##            final_min_dist = max_dist
##            start = start_in
##            finish = finish_in
##            print(source,final_min_dist,mapping[start],mapping[finish])
#    print(source,max_dist,mapping[start_in],mapping[finish_in])
#
#    return final_min_dist,start,finish


def question_4(systems,coordinates,reverse_map):
    
    ### Compute adjacency matrix
    distance_matrix = [[euclidean_dist(coordinates[i], coordinates[j]) for i in systems] for j in systems]
    visited,final_min_dist,start,finish = breadth_first_search(systems, distance_matrix,reverse_map)
    
    if set(systems) == set(visited):
        print(True)
    else:
        print(False)

    print(final_min_dist)
    return final_min_dist,start,finish

#def breadth_first_search(systems, graph: List[List[int]],mapping) -> List[int]:
#
#    final_min_dist = 1.0e+25
#    start = 0
#    finish = 0
#
#    for i,_ in enumerate(systems):
#        source = i
#        if source % 100 == 0:
#            print('source',source)
#        max_dist = 0
#        start_in = 0
#        finish_in = 0
#
#        vertices = [Vertex(index) for index, _ in enumerate(graph)]
#        vertices[source].d = 0
#
#        queue = []
#        processed = []
#        queue.append(source)
#        good_indices = list(range(0,len(systems)))
#        while queue != []:
#            u = queue.pop(0)
#            processed.append(u)
#            good_indices.remove(u)
#            a = graph[u]
#            remaining_nodes = [a[i] for i in good_indices]
#            if remaining_nodes != []:
#                min_dist = min(remaining_nodes)
#                minpos = graph[u].index(min_dist)
#                if min_dist > max_dist:
#                    max_dist = min_dist
#                    start_in = u
#                    finish_in = minpos
#                queue.append(minpos)
#
#        if max_dist < final_min_dist:
#            final_min_dist = max_dist
#            start = start_in
#            finish = finish_in
#            print(source,final_min_dist,mapping[start],mapping[finish])
#
#    return (processed,final_min_dist,start,finish)


#def breadth_first_search(graph: List[List[int]]) -> List[int]:
#    """Perform BFS on the graph,
#        
#        Arguments:
#        graph {List[List[int]]} -- The adjacensy list representation of the graph
#        max_distance {int} -- Maximum distance allowed between two systems
#        source {int} -- The system index of the starting system
#        
#        Returns:
#        List[int] -- The list of system indexes representing the shortest path from the source to all reachable systems
#        """
#    # initialization of the nodes
#    source = 10
#    max_dist = 0
#    start_in = 0
#    finish_in = 0
#    vertices = [Vertex(index) for index, _ in enumerate(graph)]
#    vertices[source].color = "gray"
#    vertices[source].d = 0
#    
#    
#    queue = []
#    processed = []
#    queue.append(source)
#    while queue != []:
#        u = queue.pop(0)
#        processed.append(u)
#        for adj_star, distance in enumerate(graph[u]):
#            if vertices[adj_star].color == 'white':
#                vertices[adj_star].color = 'gray'
#                vertices[adj_star].d = vertices[u].d + distance
#                vertices[adj_star].pi = vertices[u]
#                queue.append(adj_star)
#                if distance > max_dist:
#                    max_dist = distance
#                    start_in = u
#                    finish_in = adj_star
#        vertices[u].color = 'black'
#
#    final_distance, start_in, finish_in =  backtrace_4(graph, vertices[u])
#    return processed, final_distance

def backtrace_4(distance, node: Vertex) -> (float, List[int]):
    """Method creates a list of elements that correspond to the order of progression

        Arguments:
        security {Dict[int, float]} -- Security rating for different systems
        node {Vertex} -- Vertex to backtrace from

        Returns:
        final_sec[float] -- Total security along the path
        List[int] -- reconstructing the back-pointers
        """
    path = [node.identifier]
    max_dist = 0
    start_in = 0
    finish_in = 0
    while node.pi is not None:
        print('yes')
        if distance[node.pi.identifier][path[0]] > max_dist:
            print('enter')
            max_dist = distance[node.pi.identifier][path[0]]
            start_in = node.pi.identifier
            finish_in = path[0]
        path.insert(0, node.pi.identifier)
        node = node.pi
    print(path)
    return (max_dist,start_in,finish_in)

######################################################################################

def q1_shortest_path(start: str, destination: str) -> List[str]:
    graph, mapping, security, distances  = parse_universe()
    reverse_map = {index: name for name, index in mapping.items()}
    if start not in mapping.keys():
        print('Source system does not exist')
        return
    if destination not in mapping.keys():
        print('Destination system does not exist')
        return
    startt = timer()
    dist, jita_dodixie_route = dijkstra(graph, distances, mapping[start], mapping[destination])

    end = timer()
    print('Total time',end-startt)
    print('total distance', dist)
    route = [reverse_map[system] for system in jita_dodixie_route]
    print(route)
    return route

def q2_best_path(start: str, destination: str) -> List[str]:
    graph, mapping, security, distances  = parse_universe()
    reverse_map = {index: name for name, index in mapping.items()}
    if start not in mapping.keys():
        print('Source system does not exist')
        return
    if destination not in mapping.keys():
        print('Destination system does not exist')
        return
    startt = timer()
    final_sec, jita_dodixie_route = dijkstra_2(graph, security, mapping[start], mapping[destination],reverse_map)
    end = timer()
    print('Total time',end-startt)
    print('total security', final_sec)
    route = [reverse_map[system] for system in jita_dodixie_route]
    print(route)
    return route


def question1():
    q1_shortest_path("6VDT-H", "Dodixie")

def question2():
    q2_best_path("6VDT-H", "N-RAEL")
#    q2_best_path("Egmur", "Javrendei")

def question3():
#    max_distance = 1.0e+16
#    max_distance = 9.712106816772234e+17
    max_distance = 2.4675e+16
    answer = question_3(max_distance)
    print('Final answer: ',answer)

def question4():
    mapping, coordinates = parse_universe_4()
    reverse_map = {index: name for name, index in mapping.items()}
    systems = [index for name,index in mapping.items()]
    startt = timer()
    answer,start,finish = question_4(systems[1:2500],coordinates,reverse_map)
    end = timer()
    print('Total time',end-startt)
    print('Final answer 4: ',answer)
    print(reverse_map[start],reverse_map[finish])



def main():
#    question1()
#    question2()
    question3()
#    question4()


if __name__ == "__main__":
    main()
