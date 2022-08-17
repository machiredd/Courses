for i in range(3,-1,-1):
    print(i)

W = [10, 20, 30]
print(W[0:1])
print(W[0])


#def knapsack3(W,V,w): ##### get the list as well 2 functions
#    n = len(V)-1
#    if cache[(n,w)] != -1:
#        return cache[(n,w)]
#
#    if n == 0:
#        if W[n] <= w:
#            cache[(n,w)] = V[n]
#            print('returning for',W,V,w,n,'=>',cache[(n,w)])
#            return cache[(n,w)]
#        else:
#            cache[(n,w)] = 0
#            print('returning for',W,V,w,n,'=>',cache[(n,w)])
#            return cache[(n,w)]
#
#    if W[n] > w:
#        cache[(n,w)] = knapsack3(W[:n],V[:n],w)
#        print('returning for',W,V,w,n,'=>',cache[(n,w)])
#        return cache[(n,w)]
#    else:
#        cache[(n,w)] = max(knapsack3(W[:n],V[:n],w), V[n] + knapsack3(W[:n],V[:n],w-W[n]))
#        print('returning for',W,V,w,n,'=>',cache[(n,w)])
#        return cache[(n,w)]


##
##
#def knapsack2(W,V,w):
#    cost = [[0 for i in range(w+1)] for j in V]
#    for i in range(len(V)):
#        for j in range(w+1):
#            if i == 0:
#                if W[i] <= j:
#                    cost[i][j] = V[i]
#                else:
#                    cost[i][j] = 0
#            elif W[i] <= j:
#                cost[i][j] = max(cost[i-1][j],cost[i-1][j-W[i]]+V[i])
#            else:
#                cost[i][j] = cost[i-1][j]
#
#    cost_final = cost[len(V)-1][w]
#    items = []
#    cur_w = w
##    for i in range(len(V),0,-1):
##        if i == 0:
##            if cur_w >= W[i]:
##                items.append(1)
##            else:
##                items.append(0)
##        if cost_final == cost[i-1][cur_w]:
##            items.append(0)
##        else:
##            items.append(1)
##            cost_final = cost_final - V[i]
##            cur_w = cur_w - W[i]
##
#    for i in range(len(V),-1,-1):
#        if i == 0:
#            if cur_w >= W[i]:
#                items.append(i)
#        if cost_final == cost[i-1][cur_w]:
#            continue
#        else:
#            items.append(i)
#            cost_final = cost_final - V[i]
#            cur_w = cur_w - W[i]
#    return (cost[len(V)-1][w],items)


#W=[5,4,6,3]
#V=[10,40,30,50]
#w = 10

V = [60, 100, 120]
W = [10, 20, 30]
w = 50

#W = [1, 2, 5, 6, 7]
#V = [1,6,18,22,28]
#w = 11
##
#
#W=[10, 20, 30, 35, 15, 5, 20, 10, 15]
#V=[60, 100, 120, 165, 80, 35, 90, 50, 75]
#w=80



def min_heapify(self,A,i):
    l = self.left(i)
        r = self.right(i)
        
        if l <= A.heap_size and A[l] < A[i]:
            smallest = l
    else:
        smallest = i
        if r <= A.heap_size and A[r] < A[smallest]:
            smallest = r
    if smallest != i:
        swap(A[i],A[smallest])
            min_heapify(A,smallest)

def build_min_heapify(self,A):
    A.heap_size = A.length
        for i in range(floor(A.length/2),0,-1):
            self.min_heapify(A,i)
                
                
                def heap_extract_min(self,A):
                    if A.heap_size < 1:
print("heap overflow")
    min = A[1]
        A[1] = A[A.heap_size]
        A.heap_size = A.heap_size-1
        min_heapify(A,1)
        return min

    def min_heapify_iterative(self,A,i):
        while i <= A.heap_size:
            l = self.left(i)
            r = self.right(i)
            if  A[l] < A[i]:
                smallest = l
            else:
                smallest = i
            if A[r] < A[smallest]:
                smallest = r
            if smallest != i:
                swap(A[i],A[smallest])
                i = largest
            else:
                break

def min_heap_insert(self,A,key): #modify
    A.heap_size = A.heap_size + 1
        A[A.heap_size] = -float('Inf')
        if key < A[A.heap_size]:
            print('New key smaller than current key')
    A[A.heap_size] = key
        i = A.heap_size
        while i > 1 and A[parent(i)] < A[i]:
            swap(A[i],A[parent(i)])
            i = parent(i)
