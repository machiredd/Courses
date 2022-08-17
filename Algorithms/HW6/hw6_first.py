import math
from timeit import default_timer as timer
import random


class ht_element:
    def __init__(self, key):
        self.key = key
        self.next = None
        self.prev = None

def next_power_of_2(x):
    return 1 if x == 0 else 2**math.ceil(math.log2(x))

class chained_hash:

    def __init__(self,t_size):
        self.size = t_size
        self.new_size = next_power_of_2(self.size)
        self.T = [None] * self.new_size
    
    def insert(self, x):
        hash_val = self.hash_function(x.key)
        if self.T[hash_val] is None:
            self.T[hash_val] = x
        else:
            node = self.T[hash_val]
            x.next = node
            node.prev = x
            self.T[hash_val] = x

    def search(self,k):
        hash_val = self.hash_function(k)
        ans = None
        node = self.T[hash_val]
        while node is not None:
            if node.key == k:
                ans = node
                break
            else:
                node = node.next
        return ans

    def delete(self,x):
        hash_val = self.hash_function(x.key)
        if x.prev == None:
            self.T[hash_val] = x.next
        else:
            x.prev.next = x.next
        if x.next is not None:
            x.next.prev = x.prev

    def hash_function(self, k):
        return k % self.new_size

    def print_node(self,k):
        hash_val = self.hash_function(k)
        x = self.T[hash_val]
        list_contents=[]
        while x is not None:
            list_contents.append(str(x.key))
            x = x.next
        return " -> ".join(list_contents)

#    def __str__(self):
#        return self.T



class chained_hash2(ht_element):
    
    def __init__(self,t_size):
        ht_element.__init__(self)
        self.size = t_size
        self.new_size = next_power_of_2(self.size)
        self.T = [None] * self.new_size
    
    def insert(self, x):
        hash_val = self.hash_function(x.key)
        if self.T[hash_val] is None:
            self.T[hash_val] = x
        else:
            node = self.T[hash_val]
            x.next = node
            node.prev = x
            self.T[hash_val] = x

    def search(self,k):
        hash_val = self.hash_function(k)
        ans = None
        node = self.T[hash_val]
        while node is not None:
            if node.key == k:
                ans = node
                break
            else:
                node = node.next
        return ans

    def delete(self,x):
        hash_val = self.hash_function(x.key)
        if x.prev == None:
            self.T[hash_val] = x.next
        else:
            x.prev.next = x.next
        if x.next is not None:
            x.next.prev = x.prev

    def hash_function(self, k):
        return k % self.new_size
    
    def print_node(self,k):
        hash_val = self.hash_function(k)
        x = self.T[hash_val]
        list_contents=[]
        while x is not None:
            list_contents.append(str(x.key))
            x = x.next
        return " -> ".join(list_contents)


def test1():
    h = chained_hash(10)
    print(h.T)
    h.insert(ht_element(7))
    print(h.T)
    print(h.print_node(7))
    h.insert(ht_element(8))
    h.insert(ht_element(24))
    print(h.print_node(8))
    h.delete(h.search(24))
    print(h.print_node(8))



def mul_hash(k):
    knuth_A = (math.sqrt(5)-1)/2
    p=14
    m = 2**p
    w = 32
    s = int(knuth_A * 2**(w))
    res= k * s
    r1 = res/(2**w)
    r0 = res%(2**w)
    final = r0 >> (w-p)
    return final


#k=123456
#check = mul_hash(k)
#print(check)

class Node(object):
    def __init__(self, value):
        self.parent = self
        self.value = value
        self.rank = 0

    def __str__(self):
        return self.value


class forests():
    def __init__(self,values=[]):
        self.set = []
        if values:
            self.set = [Node(value) for value in values]

    def make_set(self,x):
        x.parent = x
        x.value = x
        x.rank = 0
        self.set.append(x)
    
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
#
#
#class forests_2():
#    def __init__(self,values):
#        self.set = [Node(value) for value in values]
#    
#    def make_set(self,x):
#        x.parent = x
#        x.rank = 0
#    
#    def union(self,x,y):
#        x_n = self.find_set(x)
#        y_n = self.find_set(y)
#        x_n.parent = y_n
#
#    def find_set(self,x):
#        if x == x.parent:
#            return x
#        else:
#            return self.find_set(x.parent)
#
#
def time_forests():
    time = []
    n  = range(300,3000,300)
    for i in n:
        m = i/3
        start = timer()
        f = forests()
        for j in range(i):
            f.make_set(Node(i))
        while m!=0:
            a = random.randint(0,i)
            r1 = f.find_set(a)
            m = m-1
            r2 = r1
            while r1 == r2:
                b = random.randint(0,i)
                r2 = f.find_set(b)
                m = m-1
            f.union(r1,r2)
            m = m-1
        end = timer()
        print(i, end-start)







#class forests():
#    def __init__(self,values):
#        self.set = [Node(value) for value in values]
#        print([str(i) for i in self.set])
#
#    def make_set(self,x):
#        x.parent = x
#        x.rank = 0
#
#    def union(self,x,y):
#        self.link(self.find_set(x),self.find_set(y))
#
#    def link(self,x,y):
#        if x.rank > y.rank:
#            y.parent = x
#        else:
#            x.parent = y
#            if x.rank == y.rank:
#                y.rank = y.rank + 1
#                    
#    def find_set(self,x):
#        if x != x.parent:
#            x.parent = self.find_set(x.parent)
#        return x.parent
#

#class forests():
#    def __init__(self,values):
#        self.parent={}
#        self.value={}
#        self.rank={}
#        for x in values:
#            self.parent[x] = x
#            self.rank[x] = 0
#            self.value[x] = x
#
#    def make_set(self,x):
#        self.parent[x] = x
#        self.rank[x] = 0
#
#    def union(self,x,y):
#        self.link(self.find_set(x),self.find_set(y))
#
#    def link(self,x,y):
#        if self.rank[x] > self.rank[y]:
#            self.parent[y] = x
#        else:
#            self.parent[x] = y
#            if self.rank[x] == self.rank[y]:
#                self.rank[y] = self.rank[y] + 1
#
#    def find_set(self,x):
#        if x != self.parent[x]:
#            self.parent[x] = self.find_set(self.parent[x])
#        return self.parent[x]
#

def test_forests():
    a= forests(['a','b','c','d','e'])
    sets =  [str(a.find_set(x)) for x in ['a','b','c','d','e']]
    print("set representatives:\t\t", sets)
    print("number of disjoint sets:\t", len(set(sets)))
    a.union('a','c')
    sets =  [str(a.find_set(x)) for x in ['a','b','c','d','e']]
    print("set representatives:\t\t", sets)
    print("number of disjoint sets:\t", len(set(sets)))
    a.union('a','b')
    sets =  [str(a.find_set(x)) for x in ['a','b','c','d','e']]
    print("set representatives:\t\t", sets)
    print("number of disjoint sets:\t", len(set(sets)))
    print(a.parent)


if __name__ == "__main__":

#    test1()
    test_forests()
#    time_forests()



