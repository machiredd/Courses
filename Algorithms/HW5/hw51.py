cache = {}

def knapsack1(W,V,w):
    cost = [[0 for i in range(w+1)] for j in V]
    for i in range(len(V)):
        for j in range(w+1):
            if i == 0:
                if W[i] <= j:
                    cost[i][j] = V[i]
                else:
                    cost[i][j] = 0
            elif W[i] <= j:
                cost[i][j] = max(cost[i-1][j],cost[i-1][j-W[i]]+V[i])
            else:
                cost[i][j] = cost[i-1][j]
#    return cost[i][j]
    return cost[len(V)-1][w]

#def knapsack1(W,V,w):
#    cost = [[0 for i in range(w+1)] for j in V]
#    for j in range(w+1):
#        cost[0][j] = 0
#        if W[0] <= j:
#            cost[0][j] = V[0]
#        for i in range(1,len(V)):
#            cost[i][j] = cost[i-1][j]
#            if W[i] <= j:
#                cost_inc = cost[i-1][j-W[i]]+V[i]
#                if cost_inc > cost[i][j]:
#                    cost[i][j] = cost_inc
#    return cost[len(V)-1][w]

def knapsack21(W,V,w): #1
    cost = [[0 for i in range(w+1)] for j in V]
    for i in range(len(V)):
        for j in range(w+1):
            if i == 0:
                if W[i] <= j:
                    cost[i][j] = V[i]
                else:
                    cost[i][j] = 0
            else:
                cost[i][j] = cost[i-1][j]
                if W[i] <= j:
                    cost_inc = cost[i-1][j-W[i]]+V[i]
                    if cost_inc > cost[i][j]:
                        cost[i][j] = cost_inc


    cost_final = cost[len(V)-1][w]
    items = []
    cur_w = w
    for i in range(len(V),-1,-1):
        if i == 0:
            if cur_w >= W[i]:
                items.append(i)
            break
        if cost_final != cost[i-1][cur_w]:
            items.append(i)
            cost_final = cost_final - V[i]
            cur_w = cur_w - W[i]
    return (cost[len(V)-1][w],items)



def knapsack2(W,V,w):#2
    cost = [[0 for i in range(w+1)] for j in V]
    items = [[0 for i in range(w+1)] for j in V]
    for i in range(len(V)):
        for j in range(w+1):
            if i == 0:
                if W[i] <= j:
                    cost[i][j] = V[i]
                    items[i][j] = 1
                else:
                    cost[i][j] = 0
            else:
                cost[i][j] = cost[i-1][j]
                if W[i] <= j:
                    cost_inc = cost[i-1][j-W[i]]+V[i]
                    if cost_inc > cost[i][j]:
                        cost[i][j] = cost_inc
                        items[i][j] = 1
    cost_final = cost[len(V)-1][w]
    final_items = []
    cur_w = w
    for i in range(len(V)-1,-1,-1):
        if items[i][cur_w] == 1:
            final_items.append(i)
            cur_w = cur_w - W[i]
    return (cost[len(V)-1][w],final_items)



def knapsack3_sub(W,V,w):
    n = len(V)-1
    if cache[(n,w)][0] != -1:
        return cache[(n,w)]
    
    if n == 0:
        if W[n] <= w:
            cache[(n,w)] = (V[n],0)
            return cache[(n,w)]
        else:
            cache[(n,w)] = (0,0)
            return cache[(n,w)]
    if W[n] > w:
        cache[(n,w)] = (knapsack3(W[:n],V[:n],w),0)
        return cache[(n,w)]
    else:
        x1 = knapsack3(W[:n],V[:n],w)[0]
        x2 = V[n] + knapsack3(W[:n],V[:n],w-W[n])[0]
        if x2 > x1:
            cache[(n,w)] = (x2,1)
        else:
            cache[(n,w)] = (x1,0)
        return cache[(n,w)]


def knapsack3(W,V,w):
    best,seq = knapsack3_sub(W,V,w)
    cost_final = cache[len(V)-1,w][0]
    final_items = []
    cur_w = w
    for i in range(len(V)-1,-1,-1):
        if cache[i,cur_w][1] == 1:
            final_items.append(i)
            cur_w = cur_w - W[i]
    return (best,final_items)




class heap:
    
    def __init__(self):
        self.__heap = []
    
#    def __init__(self,A):
#        self.A = A
#        self.heap_size = len(A)
#        self.length = len(A)

    def heap_size(self):
        return len(self.__heap)
    
    def build_heap(self,A):
        n = len(A)
        for i in range(n):
            self.append(A[i])

    def parent(self,i):
        return int((i-1)//2)

    def left(self,i):
        return 2*i+1

    def right(self,i):
        return 2*i+2
    
    def min_heapify(self,i):
        l = self.left(i)
        r = self.right(i)
        if l <= self.heap_size-1 and self.__heap[l] < self.__heap[i]:
            smallest = l
        else:
            smallest = i
        if r <= self.heap_size-1 and self.__heap[r] < self.__heap[smallest]:
            smallest = r
        if smallest != i:
            w = self.__heap[i]
            self.__heap[i] = self.__heap[smallest]
            self.__heap[smallest] = w
            self.min_heapify(smallest)

    def build_min_heap(self):
        self.heap_size = self.length
        for i in range((self.length//2)-1,-1,-1):
            self.min_heapify(i)

    def heap_extract_min(self):
        if self.heap_size < 1:
            print("heap overflow")
        min = self.__heap[0]
        self.__heap[0] = self.__heap[self.heap_size-1]
        del self.__heap[self.heap_size-1]
        self.heap_size = self.heap_size-1
        self.min_heapify(0)
        return min

    def min_heapify_iterative(self,i):
        while i <= self.heap_size:
            l = self.left(i)
            r = self.right(i)
            if  l <= self.heap_size-1 and self.__heap[l] < self.__heap[i]:
                smallest = l
            else:
                smallest = i
            if r <= self.heap_size-1 and self.__heap[r] < self.__heap[smallest]:
                smallest = r
            if smallest != i:
                w = self.__heap[i]
                self.__heap[i] = self.__heap[smallest]
                self.__heap[smallest] = w
                i = smallest
            else:
                break

    def build_min_heap_iterative(self):
        self.heap_size = self.length
        for i in range((self.length//2)-1,-1,-1):
            self.min_heapify_iterative(i)

    def min_heap_insert(self,key):
        self.heap_size = self.heap_size + 1
        self.__heap.append(-float('Inf'))
        if key < self.__heap[self.heap_size-1]:
            print('New key smaller than current key')
        self.__heap[self.heap_size-1] = key
        i = self.heap_size-1
        while i > 0 and self.__heap[self.parent(i)] > self.__heap[i]:
            w = self.__heap[i]
            self.__heap[i] = self.__heap[self.parent(i)]
            self.__heap[self.parent(i)] = w
            i = self.parent(i)

def part1():
    V = [60, 100, 120]
    W = [10, 20, 30]
    w = 50
    
    best = knapsack1(W,V,w)
    print('Version 1:','Best value: ',best)
    best,seq = knapsack2(W,V,w)
    print('Version 2:','Best value: ', best,'List index of items: ',seq)
    
    for i in range(len(V)):
        for j in range(w+1):
            cache[(i,j)] = (-1,0)
    best,seq = knapsack3(W,V,w)
    print('Version 3:','Best value: ', best,'List index of items: ',seq)


def part2():

    b=[4,5,1,8,9,7,10]
    h1=heap(b)
    print('Input heap: ', b)
    h1.min_heapify(0)
    print('min_heapify(0) result: ',b)

    print('-'*80)

    b=[10, 8, 9, 7, 6, 5, 4]
    h1=heap(b)
    print('Input heap: ', b)
    h1.build_min_heap()
    print('Build_min_heap result: ',b)
    m=h1.heap_extract_min()
    print('Extract min: ',m)

    print('-'*80)

    b=[10, 8, 9, 7, 6, 5, 4]
    h1=heap(b)
    print('Input heap: ', b)
    h1.build_min_heap_iterative()
    print('Build_min_heap_iterative result: ',b)

    h1.min_heap_insert(1)
    print('Heap after inserting 1: ',b)


if __name__ == "__main__":

#  part1()
#    part2()

    h = heap()
    h.build_heap([4,5,1,8,9,7,10])

