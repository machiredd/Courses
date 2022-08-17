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
    
    def add_task(self, task, priority=0):
        if task in self.entry_finder:
            self.delete(task)
        entry = [priority, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.heap, entry)
    
    def remove_task(self, task):
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED
    
    def pop_task(self):
        while self.heap:
            priority, task = heapq.heappop(self.heap)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return priority, task
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
        Q.put([vertices[index].d,vertices[index].identifier])
    
    pq = PriorityQueue_update(Q.queue)
    
    while len(pq.heap) > 0:
        d,u = pq.pop_task()
        S.add(u)
        if u == destination:
            return backtrace(distances, vertices[destination])
        for adj_star in graph[u]:
            if vertices[adj_star].d > vertices[u].d + distances[u, adj_star]:
                vertices[adj_star].d = vertices[u].d + distances[u, adj_star]
                vertices[adj_star].pi = vertices[u]
                pq.remove_task(adj_star)
                pq.add_task(adj_star,vertices[adj_star].d)


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


def question1():
    q1_shortest_path("6VDT-H", "Dodixie")


def main():
    question1()


if __name__ == "__main__":
    main()
