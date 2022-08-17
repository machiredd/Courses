import math
from timeit import default_timer as timer
import random

class Node(object):
    def __init__(self, value):
        self.parent = self
        self.value = value
        self.rank = 0
    
    def __str__(self):
        return self.value


class forests():
    def __init__(self,values=[]):
        self.set = [Node(value) for value in values]

    def make_set(self,x):
#        x.parent = x
#        x.rank = 0
        self.set.append(Node(x))

    def union(self,x,y):
        self.link(self.find_set(x),self.find_set(y))
    
    def link(self,x,y):
        if x.rank > y.rank:
            y.parent = x
        else:
            x.parent = y
            if x.rank == y.rank:
                y.rank = y.rank + 1

    def find_set(self,x):
        if x != x.parent:
            x.parent = self.find_set(x.parent)
        return x.parent


class forests_2():
    def __init__(self,values=[]):
        self.set = [Node(value) for value in values]

    def make_set(self,x):
#        x.parent = x
#        x.rank = 0
        self.set.append(Node(x))

    def union(self,x,y):
        x_n = self.find_set(x)
        y_n = self.find_set(y)
        x_n.parent = y_n

    def find_set(self,x):
        if x == x.parent:
            return x
        else:
            return self.find_set(x.parent)



def time_forests(ver):
    time = []
    m  = range(3000,83000,3000)
    for i in m:
        n = int(i/3)
        n_make = 0
        n_union = 0
        n_find = 0
        start = timer()
        if ver == 1:
            f = forests()
        else:
            f = forests_2()
        for j in range(n):
            f.make_set(j)
            n_make += 1
        left = i - n
        while left > 0:
            a = random.randint(0,n-1)
            r1 = f.find_set(f.set[a])
            n_find += 1
            left = left-1
            r2 = r1
            while r1 == r2:
                b = random.randint(0,n-1)
                r2 = f.find_set(f.set[b])
                n_find += 1
                left = left-1
            f.union(r1,r2)
            n_union += 1
            left = left-1
        end = timer()
        diff = end-start
        c = diff/(i * math.log(i)) * 1000000
        print(i, n_make, n_union, n_find, diff, c)


def test_forests():
    a= forests(['a','b','c','d','e'])
    print(len(a.set))
    sets =  [str(a.find_set(x)) for x in a.set]
    print("set representatives:\t\t", sets)
    print("number of disjoint sets:\t", len(set(sets)))
    a.union(a.set[0],a.set[2])
    sets =  [str(a.find_set(x)) for x in a.set]
    print("set representatives:\t\t", sets)
    print("number of disjoint sets:\t", len(set(sets)))
    a.union(a.set[0],a.set[1])
    sets =  [str(a.find_set(x)) for x in a.set]
    print("set representatives:\t\t", sets)
    print("number of disjoint sets:\t", len(set(sets)))


time_forests(1)
#test_forests()



