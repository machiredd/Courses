import math

class ht_element:
    def __init__(self, key):
        self.key = key
        self.next = None
        self.prev = None

def next_power_of_2(x):
    return 1 if x == 0 else 2**math.ceil(math.log2(x))

class ht_element2(ht_element):
    def __init__(self, key, value):
        super().__init__(key)
        self.value = value


class chained_hash:
    
    def __init__(self,t_size):
        self.size = t_size
        self.new_size = next_power_of_2(self.size)
        self.T = [None] * self.new_size
        self.power = int(math.log2(self.new_size))
        knuth_A = (math.sqrt(5)-1)/2
#        self.p=14
        self.p = self.power
        m = 2**self.p
        self.w = 32
        self.s = int(knuth_A * 2**(self.w))
    
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

    def hash_function_mul(self,k):
        res= k * self.s
#        print('k: ',k)
#        print('k*s: ',res)
        r1 = res/(2**self.w)
        r0 = res%(2**self.w)
#        print('r1: ',r1)
#        print('r0: ',r0)
        final = r0 >> (self.w-self.p)
        return final




def test1():
    h = chained_hash(10)
    print('Hash table Initialization:')
    print(h.T)
    h.insert(ht_element(7))
    print('Hash table after inserting element 7:')
    print(h.T)
    print('Printing linked list at slot that key 7 was hashed to:')
    print(h.print_node(7))
    h.insert(ht_element(8))
    h.insert(ht_element(24))
    print('Printing linked list at slot that keys 8 and 24 were hashed to:')
    print(h.print_node(8))
    print('Printing linked list at slot that keys 8 and 24 were hashed to after deleting key 24:')
    h.delete(h.search(24))
    print(h.print_node(8))

def test2():
    h = chained_hash(10)
    h.insert(ht_element2(7,5))
    h.insert(ht_element2(8,6))
    h.insert(ht_element2(24,4))
    print('Inserted keys=(7,8,24) with values=(5,6,4)')
    print('Retriving value of key 24: ', h.search(24).value)
    print('Retriving value of key 8: ',h.search(8).value)
    print('Retriving value of key 7: ',h.search(7).value)
    h.delete(h.search(24))





#def mul_hash(k):
#    knuth_A = (math.sqrt(5)-1)/2
#    p=14
#    m = 2**p
#    w = 32
#    s = int(knuth_A * 2**(w))
#    res= k * s
#    print('k: ',k)
#    print('k*s: ',res)
#    r1 = res/(2**w)
#    r0 = res%(2**w)
#    print('r1: ',r1)
#    print('r0: ',r0)
#    final = r0 >> (w-p)
#    return final

def mul_hash(k):
    knuth_A = (math.sqrt(5)-1)/2
    p=14
    m = 2**p
    w = 32
    s = int(knuth_A * 2**(w))
    res= k * s
    mask = 2**w-1
    print('k: ',k)
    print('k*s: ',res)
    r1 = res/(2**w)
    r0 = res & mask
    print('r1: ',r1)
    print('r0: ',r0)
    final = r0 >> (w-p)
    return final


k=123456
check = mul_hash(k)
print('h(k): ', check)
#
#print(math.log2(16))
#print(math.log2(32))

#test1()
#test2()
#
#h = chained_hash(10)
#print(h.hash_function_mul(12))
#print(h.hash_function_mul(15))
#print(h.hash_function_mul(12))
