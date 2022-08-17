import hw1


# Check doubly linked list
def doubly_linked_list():
    print('Doubly linked list:')
    print('Making list 4 -> 3 -> 2 -> 1')
    l = hw1.DoublyLinkedList()
    l.insert(hw1.Element(1));
    l.insert(hw1.Element(2));
    l.insert(hw1.Element(3));
    l.insert(hw1.Element(4));
    
    print('Head node: %d' %(l.head.key))
    print('Node before 2: %d' %(l.search(2).prev.key))
    
    print('Delete node with value 3')
    l.delete(l.search(3));
    
    print('Head node: %d' %(l.head.key))
    print('Node before 2: %d' %(l.search(2).prev.key))
    
    print('Search for element 8 which is not present in the list')
    print(l.search(8))


# Check singly linked list
def singly_linked_list():

    print('Singly Linked List:')

    l = hw1.SinglyLinkedList()
    
    l.insert(hw1.Element(1));
    l.insert(hw1.Element(2));
    l.insert(hw1.Element(3));
    l.insert(hw1.Element(4));
    
    print(str(l))
    print('Length of the list: %d' %(len(l)))


    print('Inserting element 5 and deleting element 3 from the list')
    l.insert(hw1.Element(5));
    l.delete(l.search(3));
    
    print(str(l))

    print('Checking equivalence of two lists')
    l1 = hw1.SinglyLinkedList()
    
    l1.insert(hw1.Element(1));
    l1.insert(hw1.Element(2));
    l1.insert(hw1.Element(3));
    l1.insert(hw1.Element(4));

    print('List 1: %s' %(str(l)))
    print('List 2: %s' %(str(l1)))
    print('Equivalence result: %s' %(l==l1))

    l1.insert(hw1.Element(5));
    l1.delete(l1.search(3));

    print('List 1: %s' %(str(l)))
    print('List 2: %s' %(str(l1)))
    print('Equivalence result: %s' %(l==l1))


#Check doubly linked lists with sentinel
def doubly_linked_list_sentinel():
    
    print('Doubly Linked Lists with sentinel:')

    l = hw1.CircularDoublyLinkedList()
    
    print('Empty list')
    print('Sentinel.key: %s' %(l.sentinel.key))
    print('Sentinel.next: %s' %(l.sentinel.next.key))
    print('Sentinel.prev: %s' %(l.sentinel.prev.key))
    
    l.insert(hw1.Element(1));
    l.insert(hw1.Element(2));
    l.insert(hw1.Element(3));
    l.insert(hw1.Element(4));
    
    print('List after inserting elements 1,2,3,4')
    print(str(l))
   
    print('Sentinel.key: %s' %(l.sentinel.key))
    print('Sentinel.next: %s' %(l.sentinel.next.key))
    print('Sentinel.prev: %s' %(l.sentinel.prev.key))
    print('Length of the list: %d' %(len(l)))

    
    print('Inserting element 5 and deleting element 1 from the list')
    l.insert(hw1.Element(5));
    l.delete(l.search(1));
    
    print(str(l))
    print('Sentinel.key: %s' %(l.sentinel.key))
    print('Sentinel.next: %s' %(l.sentinel.next.key))
    print('Sentinel.prev: %s' %(l.sentinel.prev.key))
    
    print('Search for element 4')
    print(l.search(4).key)
    
    print('Search for element 7 which is not present in the list')
    print(l.search(7))


if __name__ == '__main__':

    doubly_linked_list()
    print('-'*80)
    singly_linked_list()
    print('-'*80)
    doubly_linked_list_sentinel()