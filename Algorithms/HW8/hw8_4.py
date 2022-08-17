import csv
from collections import deque  # built in queue object
from pathlib import Path
from typing import List, Dict, Tuple, Any
from timeit import default_timer as timer
import pickle

__version__ = "2"


### Question 2
class Vertex:
    def __init__(self, identifier: Any):
        self.identifier = identifier
        self.d = float("inf")
        self.pi = None
        self.color = "white"
        self.f = float("inf")


class Queue:
    """FIFO Queue Object
    """

    def __init__(self):
        # we use the underscore to indicate that we do not want to access
        # the attribute directly (it's python's way of saying that it should
        # be treated as private)
        self._queue: List[Vertex] = []
    
    def __bool__(self) -> bool:
        """This magic method tells how to evaluate bool(Queue)

        Think when you would want bool(Queue) to equal False and
        when it should equal true

        This method is not mandatory, but can make some of the code
        a bit easier to write when interacting w/ your queue implementation
        
        Returns:
            bool
        """
        #raise NotImplementedError
        if self._queue != []:
            return True
        else:
            return False

    def popleft(self) -> Vertex:
        """popleft is equivalent to the deque method described in the book
        
        Returns:
            Any -- The element that is next up to be removed from the queue
        """
        #raise NotImplementedError
        return self._queue.pop(0)

    def append(self, element: Vertex) -> None:
        """append is equivalent to the enqueue method described in the book
        """
        #raise NotImplementedError
        self._queue.append(element)

    def appendleft(self, element: Vertex) -> None:
        """append to the beginning of the queue
        """
        #raise NotImplementedError
        self._queue = [element] + self._queue


def parse_universe(
    fpath=Path("sde-universe_2018-07-16.csv.txt")
) -> Tuple[List[List[int]], Dict[int, str]]:
    """Method will parse the CSV file and build up a graph representation of the eve universe

    Keyword Arguments:
        fpath {[type]} -- path to the csv object ot import (default: {Path("sde-universe_2018-07-16.csv")})

    Returns:
        Tuple[List[List[int]], Dict[int, str] -- First item returned is an adjacency list reprenting 
        the graph in the Eve Universe, the second item returned is a dictionary with keys of indexes 
        in the adjacency list, and values as the system names.
    """

    # dictionary where key is a system_id and value is a list of adjacent system_ids
    system_mapping: Dict[int, List[int]] = {}

    # dictionary where the key is the name of the system, and the value is the associated system_id
    name_to_id: Dict[str, int] = {}

    # dictionary where key is the system_id, and the value is the index number in the
    # adjacency lists representation
    id_to_index: Dict[int, int] = {}

    #raise NotImplementedError
    with open(fpath, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            system_mapping[row['system_id']] = row['stargates']
            name_to_id[row['solarsystem_name']] = row['system_id']

    for index, name in enumerate(name_to_id):
        id_to_index[name_to_id[name]] = index


    # empty list of the right size to put your adjacency lists into
    graph: List[List[int]] = [None] * len(system_mapping)
    for system, adjacents in system_mapping.items():
        # here is where you populate the adjacency lists representation
        #raise NotImplementedError
        adj_list = []
        adjacents = adjacents.strip('[')
        adjacents = adjacents.strip(']')
        adjacents = adjacents.replace(' ', '')
        adjacents = adjacents.split(',')
        for stars in adjacents:
            if stars != '':
                adj_list.append(id_to_index[str(stars)])
                graph[id_to_index[system]] = adj_list

    # not only can you do list comprehensions
    # you can do dictionary comprehensions in python as well!!
    name_to_index = {
        name: id_to_index[system_id] for name, system_id in name_to_id.items()
    }
    return graph, name_to_index


def backtrace(node: Vertex) -> List[int]:
    """Method creates a list of elements that correspond to the order of progression
    
    Arguments:
        node {Vertex} -- Vertex to backtrace from
    
    Returns:
        List[int] -- reconstructing the back-pointers 
    """
    path = [node.identifier]
    while node.pi is not None:
        path.insert(0, node.pi.identifier)
        node = node.pi
    return path


def breadth_first_search(
    graph: List[List[int]], source: int, destination: int, use_python_deque=False
) -> List[int]:
    """Perform BFS on the graph, 
    
    Arguments:
        graph {List[List[int]]} -- The adjacensy list representation of the graph
        source {int} -- The system index of the starting system
        destination {int} -- The system index of the destination system
    
    Keyword Arguments:
        use_python_deque {bool} -- option to use the native deque python object or your own implementation (default: {False})
    
    Returns:
        List[int] -- The list of system indexes representing the shortest path from the source to target destination
    """

    # initialization of the nodes
    vertices = [Vertex(index) for index, _ in enumerate(graph)]
    vertices[source].color = "gray"
    vertices[source].d = 0

    if use_python_deque:
        queue = deque()
    else:
        queue = Queue()
    
    # Here is where you implement the breadth first search
    #raise NotImplementedError
    queue.append(source)
    while bool(queue) == True:
        u = queue.popleft()
        for adj_star in graph[u]:
            if vertices[adj_star].color == 'white':
                vertices[adj_star].color = 'gray'
                vertices[adj_star].d = vertices[u].d + 1
                vertices[adj_star].pi = vertices[u]
                if adj_star == destination:
                    return backtrace(vertices[destination])
                queue.append(adj_star)
        vertices[u].color = 'black'




def print_route(route: List[int], reverse_mapping: Dict[int, str]) -> None:
    named_route = [reverse_mapping[system] for system in route]
    print(" -> ".join(named_route))

def question2(import_pickle=False):
    if import_pickle:
        with open("Q2_pickle", "rb") as f:
            graph = pickle.load(f)
            mapping = pickle.load(f)
    else:    
        graph, mapping = parse_universe()
    # mapping gives us a dict of name -> index
    # BFS algorithm will give us a list of indexes, so we need a dict
    # of index -> name
    reverse_map = {index: name for name, index in mapping.items()}

    jita_dodixie_route = breadth_first_search(graph, mapping["Jita"], mapping["Dodixie"])
    print_route(jita_dodixie_route, reverse_map)

def question2_time():
    graph, mapping = parse_universe()
    reverse_map = {index: name for name, index in mapping.items()}
    
    start = timer()
    jita_dodixie_route = breadth_first_search(graph, mapping["Jita"], mapping["Dodixie"])
    end = timer()
    print('cq_jd time',end-start)
    print_route(jita_dodixie_route, reverse_map)
    
    start = timer()
    jita_dodixie_route = breadth_first_search(graph, mapping["Jita"], mapping["Dodixie"],use_python_deque=True)
    end = timer()
    print('dq_jd time',end-start)
    
    start = timer()
    ib_zdyag_route = breadth_first_search(graph, mapping["313I-B"], mapping["ZDYA-G"])
    end = timer()
    print('cq_iz time',end-start)
    print_route(ib_zdyag_route, reverse_map)
    
    start = timer()
    ib_zdyag_route = breadth_first_search(graph, mapping["313I-B"], mapping["ZDYA-G"],use_python_deque=True)
    end = timer()
    print('dq_iz time',end-start)




### Question 3

def parse_requirements(fpath=Path("dependencies.txt")) -> Dict[str, List[str]]:
    """Function read in dependencies, and create a graph representation
    
    Keyword Arguments:
        fpath {[type]} -- Path to the file to be imported (default: {Path("dependencies.txt")})
    
    Returns:
        Dict[str, List[str]] -- A dictionary representing the graph.  The key will be 
    """
    #raise NotImplementedError
    graph = {}
    with open(fpath) as f:
        for line in f.readlines():
            line = line.strip()
            if line[0] != '-':
                first = line
                graph[first] = []
            else:
                graph[first].append(line.strip('- '))

    return graph


class dfs():
    def __init__(self,graph):
        self.graph = graph
        self.time = 0
        vertices1 = []
        for key, value in self.graph.items():
            vertices1.append(key)
            vertices1 = vertices1 + value
        s_ver = set(vertices1)
        self.name_to_id = {}
        for index, name in enumerate(s_ver):
            self.name_to_id[name] = index
        self.vertices = [Vertex(index) for index in s_ver]
        self.final_list = []
    
    def depth_first_search(self):
#        for index, vertex in enumerate(self.vertices):
#            if self.vertices[index].color == "white":
#                self.dfs_visit(vertex)
        self.dfs_visit(self.vertices[self.name_to_id["TimeView"]])
        
        print(self.vertices[self.name_to_id["TimeView"]].d,self.vertices[self.name_to_id["TimeView"]].f)
        print(self.time)
        return self.final_list

    def dfs_visit(self,vertex):
        self.time = self.time + 1
        self.vertices[self.name_to_id[vertex.identifier]].d = self.time
        self.vertices[self.name_to_id[vertex.identifier]].color = "gray"
        
        if vertex.identifier in list(self.graph.keys()):
            for adj_vert in self.graph[vertex.identifier]:
                if self.vertices[self.name_to_id[adj_vert]].color == "white":
                    self.vertices[self.name_to_id[adj_vert]].pi = self.vertices[self.name_to_id[vertex.identifier]]
                    self.dfs_visit(self.vertices[self.name_to_id[adj_vert]])
        self.vertices[self.name_to_id[vertex.identifier]].color = "black"
        self.final_list = [vertex.identifier] + self.final_list
        self.time = self.time + 1
        self.vertices[self.name_to_id[vertex.identifier]].f = self.time


def topological_sort(graph: Dict[str, List[str]]) -> List[str]:
    """Performs topological sort on the adjacency list generated earlier
    
    Arguments:
        graph {Dict[str, List[str]]} -- dictionary containing adjacency lists created by parse_requirements function
    
    Returns:
        List[str] -- Sorted dependencies
    """
    #raise NotImplementedError
    dfs_graph = dfs(graph)
    sorted_depandencies = dfs_graph.depth_first_search()
    return sorted_depandencies



def question3(import_pickle=False) -> List[str]:
    """Function to give the solution to Question 3
    
    Returns:
        List[str] -- returns a list of strings with the order in which one should install TimeView's dependencies
    """

    if import_pickle:
        with open("Q3_pickle", "rb") as f:
            graph = pickle.load(f)
    else:
        graph = parse_requirements()
    install_order = topological_sort(graph)
    print(install_order)
    return install_order



def main():
#    question2()
    question3()
#    question2_time()


if __name__ == "__main__":
    main()
