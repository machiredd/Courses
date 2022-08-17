cache = {}





class heap:
    def __init__(self,A):
        self.A = A
        self.heap_size = len(A)
        self.length = len(A)
    
    def parent(self,i):
        return int((i-1)//2)

    def left(self,i):
        return 2*i+1

    def right(self,i):
        return 2*i+2
    
    def min_heapify(self,i):
        l = self.left(i)
        r = self.right(i)
        if l <= self.heap_size-1 and self.A[l] < self.A[i]:
            smallest = l
        else:
            smallest = i
        if r <= self.heap_size-1 and self.A[r] < self.A[smallest]:
            smallest = r
        if smallest != i:
            w = self.A[i]
            self.A[i] = self.A[smallest]
            self.A[smallest] = w
            self.min_heapify(smallest)

    def build_min_heap(self):
        self.heap_size = self.length
        for i in range((self.length//2)-1,-1,-1):
            self.min_heapify(i)

    def heap_extract_min(self):
        if self.heap_size < 1:
            print("heap overflow")
        min = self.A[0]
        self.A[0] = self.A[self.heap_size-1]
        del self.A[self.heap_size-1]
        self.heap_size = self.heap_size-1
        self.min_heapify(0)
        return min

    def min_heapify_iterative(self,i):
        while i <= self.heap_size:
            l = self.left(i)
            r = self.right(i)
            if  l <= self.heap_size-1 and self.A[l] < self.A[i]:
                smallest = l
            else:
                smallest = i
            if r <= self.heap_size-1 and self.A[r] < self.A[smallest]:
                smallest = r
            if smallest != i:
                w = self.A[i]
                self.A[i] = self.A[smallest]
                self.A[smallest] = w
                i = smallest
            else:
                break

    def build_min_heap_iterative(self):
        self.heap_size = self.length
        for i in range((self.length//2)-1,-1,-1):
            self.min_heapify_iterative(i)

    def min_heap_insert(self,key):
        self.heap_size = self.heap_size + 1
        self.A.append(-float('Inf'))
        if key < self.A[self.heap_size-1]:
            print('New key smaller than current key')
        self.A[self.heap_size-1] = key
        i = self.heap_size-1
        while i > 0 and self.A[self.parent(i)] > self.A[i]:
            w = self.A[i]
            self.A[i] = self.A[self.parent(i)]
            self.A[self.parent(i)] = w
            i = self.parent(i)

    def __str__(self):
        a = 0
        b = ""
        b += str(self.A[a])
        print(b)
        print(self.left(a))
        print(self.right(a))
        if self.left(a) is not None:
            b += str(self.A[self.left(a)])
        if self.right(a) is not None:
            b += str(self.A[self.right(a)])
        return b






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
    print(str(h1))
#    h1.min_heapify(0)
#    print('min_heapify(0) result: ',b)
#
#    print('-'*80)
#
#    b=[10, 8, 9, 7, 6, 5, 4]
#    h1=heap(b)
#    print('Input heap: ', b)
#    h1.build_min_heap()
#    print('Build_min_heap result: ',b)
#    m=h1.heap_extract_min()
#    print('Extract min: ',m)
#
#    print('-'*80)
#
#    b=[10, 8, 9, 7, 6, 5, 4]
#    h1=heap(b)
#    print('Input heap: ', b)
#    h1.build_min_heap_iterative()
#    print('Build_min_heap_iterative result: ',b)
#
#    h1.min_heap_insert(1)
#    print('Heap after inserting 1: ',b)


if __name__ == "__main__":

#    part1()
    part2()

