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
        for index, vertex in enumerate(self.vertices):
            if self.vertices[index].color == "white":
                self.dfs_visit(vertex)
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
#    question3()
    question2_time()


if __name__ == "__main__":
    main()
