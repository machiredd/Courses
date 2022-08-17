import csv
from collections import deque  # built in queue object
from pathlib import Path
from typing import List, Dict, Tuple, Any
from timeit import default_timer as timer
from ast import literal_eval  # makes handling import of csv nicer
import pickle
from itertools import count


### Question 2
class Vertex:
    def __init__(self, identifier: Any):
        self.identifier = identifier
        self.d = float("inf")
        self.pi = None
        self.color = "white"


class Queue:
    """FIFO Queue Object
    """

    def __init__(self):
        self._queue: List[Vertex] = []

    def __bool__(self):
        return bool(self._queue)

    def __iter__(self):
        return self._queue.__iter__()
    
    def __contains__(self, key):
        return key in self._queue

    def __getitem__(self, item):
        return self._queue[item]
    
    def __repl__(self):
        return " ".join([node.identifier for node in self._queue])

    def popleft(self) -> Vertex:
        """popleft is equivalent to the deque method described in the book
        
        Returns:
            Any -- The element that is next up to be removed from the queue
        """
        return self._queue.pop(0)
    
    def pop(self) -> Vertex:
        """pop removes and returns the last element in the queue
        
        Returns:
            Vertex -- the last element in the queue
        """
        return self._queue.pop()

    def append(self, element: Vertex) -> None:
        """append is equivalent to the enqueue method described in the book
        """
        self._queue.append(element)

    def appendleft(self, element: Vertex) -> None:
        self._queue.insert(0, element)




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

    # read in csv file build up dict of just system_id to adjacent id_S
    system_mapping = {}
    name_to_id: Dict[str, int] = {}
    with open(fpath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name_to_id[row["solarsystem_name"]] = int(row["system_id"])
            if not row["stargates"]:
                row["stargates"] = "[]"
            system_mapping[int(row["system_id"])] = list(literal_eval(row["stargates"]))
            # TA Note: `ast.literal_eval`` is okay, `eval` is not okay, don't ever use `eval`
            # heaven forbid you use eval on some input provided elsewhere, and had a maliscious actor
            # something like could be executed
            # eval('import os; os.system("rm -rf /"))')

    # dictionary referencing system_id to index position
    id_to_index = {system: index for index, system in enumerate(system_mapping.keys())}

    # constructing list of adjancency-list graph representations
    graph = [None] * len(system_mapping)
    for system, adjacents in system_mapping.items():
        graph[id_to_index[system]] = [id_to_index[neighbor] for neighbor in adjacents]

    # I need to know system names to index for future tracking
    name_to_index = {
        name: id_to_index[system_id] for name, system_id in name_to_id.items()
    }
    return graph, name_to_index


def backtrace(node: Vertex) -> List[int]:
    """Method creates a list of elements that correspond to the order of progression
    
    Arguments:
        node {Vertex} -- Vertex to backtrace from
    
    Returns:
        List[int] -- [description]
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

    # constructing the queue
    if use_python_deque:
        queue = deque()
    else:
        queue = Queue()

    queue.append(vertices[source])
    while queue:
        u = queue.popleft()
        for neighbor in graph[u.identifier]:
            v = vertices[neighbor]
            if v.color == "white":
                v.color = "gray"
                v.d = u.d + 1
                v.pi = u
                if v.identifier == destination:
                    return backtrace(vertices[destination])
                queue.append(v)
        u.color = "black"
    # if we finish the queue entirely, without finding our target, we have a problem
    raise KeyError


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
        with open('Q2_pickle', "wb") as f:
            pickle.dump(graph, f)
            pickle.dump(mapping, f)

    reverse_map = {index: name for name, index in mapping.items()}

    start = timer()
    jita_dodixie_route = breadth_first_search(
        graph, mapping["Jita"], mapping["Dodixie"]
    )
    end = timer()

    print(
        f"Jita -> Dodixie runtime with custom queue object was {end-start:{4}.{4}} seconds"
    )

    start = timer()
    jita_dodixie_route = breadth_first_search(
        graph, mapping["Jita"], mapping["Dodixie"], use_python_deque=True
    )
    end = timer()

    print(
        f"Jita -> Dodixie runtime with native queue object was {end-start:{4}.{4}} seconds"
    )

    start = timer()
    long_route = breadth_first_search(graph, mapping["313I-B"], mapping["ZDYA-G"])
    end = timer()

    print(
        f"313I-B -> ZDYA-G runtime with custom queue object was {end-start:{4}.{4}} seconds"
    )

    start = timer()
    long_route = breadth_first_search(
        graph, mapping["313I-B"], mapping["ZDYA-G"], use_python_deque=True
    )
    end = timer()

    print(
        f"313I-B -> ZDYA-G runtime with native queue object was {end-start:{4}.{4}} seconds"
    )

    print_route(jita_dodixie_route, reverse_map)


### Question 3


def parse_requirements(fpath=Path("dependencies.txt")) -> Dict[str, List[str]]:
    """Function read in dependencies, and create a graph representation
    
    Keyword Arguments:
        fpath {[type]} -- Path to the file to be imported (default: {Path("dependencies.txt")})
    
    Returns:
        Dict[str, List[str]] -- A dictionary representing the graph.  The key will be 
    """
    dep_mapping = {}
    with open(fpath) as f:
        for line in f:
            # is dependency of dependency
            if line.startswith("  -"):
                # shouldn't be needed but want to error in case it's not the case
                assert "current_dep" in locals()
                dependency = line.strip().lstrip("- ")
                dep_mapping[current_dep].append(dependency)
                if dependency not in dep_mapping.keys():
                    dep_mapping[dependency] = []
            # is top-level dependency
            else:
                current_dep = line.strip()
                dep_mapping[current_dep] = []
    return dep_mapping


def topological_sort(graph: Dict[str, List[str]]) -> List[str]:
    """Performs topological sort on the adjacency list generated earlier

    Arguments:
        graph {Dict[str, List[str]]} -- dictionary containing adjacency lists created by parse_requirements function
    
    Returns:
        List[str] -- Sorted dependencies
    """
    vertices = {dependency: Vertex(dependency) for dependency in graph.keys()}

    # constructing the queue
    queue = Queue()
    install_order = []

    queue.append(vertices["TimeView"])
    inner_stack = Queue()

    while queue:
        u = queue.pop()
        if u.color == "white":
            u.color = "gray"

            for neighbor in graph[u.identifier]:
                queue.append(vertices[neighbor])

            while inner_stack and u.identifier not in graph[inner_stack[0]]:
                install_order.append(inner_stack.popleft())

            inner_stack.appendleft(u.identifier)


    
    while inner_stack:
        install_order.append(inner_stack.popleft())
    return install_order


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
        with open("Q3_pickle", "wb") as f:
            pickle.dump(graph, f)
    install_order = topological_sort(graph)
    print(install_order)
    return install_order


def main():
    question2(import_pickle=False)
    question3(import_pickle=False)


if __name__ == "__main__":
    main()
