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

    def __str__(self):
        return " -> ".join(self._queue)




def depth_first_search(graph, use_python_deque=False):
    # initialization of the nodes
    print(graph)
    vertices1 = []
    for key, value in graph.items():
        vertices1.append(key)
        vertices1 = vertices1 + value
    s_ver = set(vertices1)
    name_to_id = {}
    for index, name in enumerate(s_ver):
        name_to_id[name] = index
        print(index,name)
    vertices = [Vertex(index) for index in s_ver]

    if use_python_deque:
        queue = deque()
    else:
        queue = Queue()
            

    time = 0
    for index, vertex in enumerate(vertices):
        print('-----entering-----')
        if vertices[index].color == 'white':
            queue.appendleft(vertex.identifier)
            print('adding',vertex.identifier)
            while bool(queue) == True:
                print(str(queue))
                u = queue.popleft()
                print('poping',u)
                time = time + 1
                print(u)
                if vertices[name_to_id[u]].color == 'white':
                    vertices[name_to_id[u]].d = time
                    print(u,'d',time)
                    vertices[name_to_id[u]].color = 'gray'
                if vertices[name_to_id[u]].identifier in list(graph.keys()):
                    print('going in')
                    for adj_vert in graph[u]:
                        if vertices[name_to_id[adj_vert]].color == 'white':
                            print(adj_vert)
                            vertices[name_to_id[adj_vert]].color = 'gray'
                            time = time + 1
                            vertices[name_to_id[adj_vert]].d = time
                            print(adj_vert,'d',time)
                            vertices[name_to_id[adj_vert]].pi = vertices[name_to_id[u]]
                            
                            if vertices[name_to_id[adj_vert]].identifier in list(graph.keys()):
                                processed = []
                                for vert in graph[adj_vert]:
                                    processed.append(vertices[name_to_id[vert]].color)
                                if 'white' in processed:
                                    queue.appendleft(adj_vert)
                                    print('adding',adj_vert)
                                else:
                                    vertices[name_to_id[adj_vert]].color = 'black'
                                    time = time + 1
                                    vertices[name_to_id[adj_vert]].f = time
                                    print(adj_vert,'f',time)
                            else:
                                vertices[name_to_id[adj_vert]].color = 'black'
                                time = time + 1
                                vertices[name_to_id[adj_vert]].f = time
                                print(adj_vert,'f',time)
    


                vertices[name_to_id[u]].color = 'black'
                time = time + 1
                vertices[name_to_id[u]].f = time
                print('processed',vertices[name_to_id[u]].identifier,vertices[name_to_id[u]].d,vertices[name_to_id[u]].f)
                print('----exiting------')

#def depth_first_search(graph, use_python_deque=False):
#    # initialization of the nodes
#    vertices1 = []
#    for key, value in graph.items():
#        vertices1.append(key)
#        vertices1 = vertices1 + value
#    s_ver = set(vertices1)
#    name_to_id = {}
#    for index, name in enumerate(s_ver):
#        name_to_id[name] = index
#    vertices = [Vertex(index) for index in s_ver]
#
#    if use_python_deque:
#        queue = deque()
#    else:
#        queue = Queue()
#
#
#    time = 0
#    for index, vertex in enumerate(vertices):
#        if vertices[index].color == 'white':
#            queue.appendleft(vertex.identifier)
#            while bool(queue) == True:
#                print(str(queue))
#                u = queue.popleft()
#                time = time + 1
#                if vertices[name_to_id[u]].color == 'white':
#                    vertices[name_to_id[u]].d = time
#                    vertices[name_to_id[u]].color = 'gray'
#                if vertices[name_to_id[u]].identifier in list(graph.keys()):
#                    for adj_vert in graph[u]:
#                        if vertices[name_to_id[adj_vert]].color == 'white':
#                            vertices[name_to_id[adj_vert]].color = 'gray'
#                            time = time + 1
#                            vertices[name_to_id[adj_vert]].d = time
#                            vertices[name_to_id[adj_vert]].pi = vertices[name_to_id[u]]
#                            if vertices[name_to_id[adj_vert]].identifier in list(graph.keys()):
#                                processed = []
#                                for vert in graph[adj_vert]:
#                                    processed.append(vertices[name_to_id[vert]].color)
#                                if 'white' in processed:
#                                    queue.appendleft(adj_vert)
#                                    print('in',str(queue))
#                                else:
#                                    vertices[name_to_id[adj_vert]].color = 'black'
#                                    time = time + 1
#                                    vertices[name_to_id[adj_vert]].f = time
#                            else:
#                                vertices[name_to_id[adj_vert]].color = 'black'
#                                time = time + 1
#                                vertices[name_to_id[adj_vert]].f = time
#            
#                vertices[name_to_id[u]].color = 'black'
#                time = time + 1
#                vertices[name_to_id[u]].f = time


### Question 3

def parse_requirements(fpath=Path("dependencies1.txt")) -> Dict[str, List[str]]:
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


def question3(import_pickle=False) -> List[str]:

    graph = parse_requirements()
    install_order = depth_first_search(graph)
    print(install_order)
    return install_order




def main():
#    question2()
    question3()
#    question2_time()


if __name__ == "__main__":
    main()
