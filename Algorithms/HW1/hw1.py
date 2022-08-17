class Element:
    def __init__(self, key):
        self.key = key
        self.next = None
        self.prev = None


class DoublyLinkedList:

    def __init__(self):
        self.head = None

    def insert(self, x):
        x.next = self.head
        if self.head is not None:
            self.head.prev = x
        self.head = x
        x.prev = None
            
    def delete(self, x):
        if x.prev is not None:
            x.prev.next = x.next
        else:
            self.head = x.next
        if x.next is not None:
            x.next.prev = x.prev

    def search(self, k):
        x = self.head
        while x is not None and x.key != k:
            x = x.next
        if x == None:
            return False
        else:
            return x


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert(self,x):
        # Inserting in the beginning of the list
        x.next = self.head
        self.head = x

    def delete(self, x):
        # If list is empty
        if self.head == None:
            return
        
        # If head node is the element being deleted
        if self.head == x:
            self.head = x.next
            return

        # Search in the rest of the list and find the element
        # before the one to be deleted and change its 'next' link
        data = self.head
        while data is not None:
            if data == x:
                prev.next = data.next
                return
            else:
                prev = data
                data = data.next

    def search(self, k):
        x = self.head
        while x is not None and x.key != k:
            x = x.next
        if x == None:
            return False
        else:
            return x

    def __str__(self):
        x = self.head
        list_contents=[]
        while x is not None:
            list_contents.append(str(x.key))
            x = x.next
        return " -> ".join(list_contents)

    def __len__(self):
        if self.head == None:
            return 0
        count = 0
        x = self.head
        while x is not None:
            count = count+1
            x = x.next
        return count

    def __eq__(self,other):
        x = self.head
        y = other.head
        while x is not None and y is not None:
            if x.key != y.key:
                return False
            else:
                x = x.next
                y = y.next
        if x is None and y is None:
            return True


class CircularDoublyLinkedList:

    def __init__(self):
        self.sentinel = Element(None)
        self.sentinel.next = self.sentinel
        self.sentinel.prev = self.sentinel

    def insert(self, x):
        x.next = self.sentinel.next
        self.sentinel.next.prev = x
        self.sentinel.next = x
        x.prev = self.sentinel
    
    def delete(self,x):
        x.prev.next = x.next
        x.next.prev = x.prev

    def search(self, k):
        x = self.sentinel.next
        while x != self.sentinel and x.key != k:
            x = x.next
        if x.key == k:
           return x
        else:
           return None

    def __str__(self):
        x = self.sentinel.next
        list_contents=[]
        while x is not self.sentinel:
            list_contents.append(str(x.key))
            x = x.next
        return " -> ".join(list_contents)

    def __len__(self):
        if self.sentinel.next == self.sentinel:
            return 0
        count = 0
        x = self.sentinel.next
        while x is not self.sentinel:
            count = count+1
            x = x.next
        return count







