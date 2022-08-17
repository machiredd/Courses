import hw2
import random
import numpy as np

def question1():
    t = hw2.Tree()
    t.root = hw2.Node(15)
    t.Insert(hw2.Node(10))
    t.Insert(hw2.Node(5))
    t.Insert(hw2.Node(6))
    t.Insert(hw2.Node(12))
    t.Insert(hw2.Node(3))
    t.Insert(hw2.Node(1))
    t.Insert(hw2.Node(23))
    t.Insert(hw2.Node(35))
    t.Insert(hw2.Node(42))
    t.Insert(hw2.Node(16))

    print('In-order walk at root node:')
    print(t.root.InOrderWalk())

    print('In-order walk at node 5:')
    print(t.root.left.left.InOrderWalk())

    print('Print node 16:')
    print(t.root.right.left.key)

    print('Search for node 10 in the tree from root:')
    print(t.root.Search(10).key)
    print('Search for node 6 in the tree from node 10:')
    print(t.root.left.Search(6).key)

    print('Minimum key in the entire tree:')
    print(t.root.Min().key)
    print('Minimum key in the tree under node 23:')
    print(t.root.right.Min().key)
    print('Minimum key in the tree under node 6:')
    print(t.root.left.left.right.Min().key)

    print('Maximum key in the entire tree:')
    print(t.root.Max().key)
    print('Successor to the root is:')
    print(t.root.Succ().key)
    print('Successor to node 6 is:')
    print(t.root.left.left.right.Succ().key)
    print(t.root.Search(6).Succ().key)

    print('Deleting node 23:')
    print('Before deletion : %s' %(t.root.InOrderWalk()))
    t.Delete(t.root.Search(23))
    print('After deletion : %s' %(t.root.InOrderWalk()))

    print('Height of the entire tree')
    print(t.root.Height(t.root.Search(15)))
    print('Height of the tree from node 5')
    print(t.root.Height(t.root.Search(5)))

    print('Deleting node 5:')
    print('Before deletion using str function: %s' %(str(t.root)))
    t.Delete(t.root.Search(5))
    print('After deletion using str function: %s' %(str(t.root)))

    t1 = hw2.Tree()
    t1.Insert_new(hw2.Node(10))
    print(str(t1.root))


def question4():
    a=[1,2,3,4,5,6,7]
    t = hw2.Tree()
    for i in range(len(a)):
        t.Insert(hw2.Node(a[i]))
    print('Inserting in ascending order: %s' %(str(t.root)))
    b=[7,6,5,4,3,2,1]
    t1= hw2.Tree()
    for i in range(len(b)):
        t1.Insert(hw2.Node(b[i]))
    print('Inserting in descending order: %s' %(str(t1.root)))
    c=[4,2,6,3,5,1,7]
    t2= hw2.Tree()
    for i in range(len(c)):
        t2.Insert(hw2.Node(c[i]))
    print('Inserting in balanced order: %s' %(str(t2.root)))


def BuildTree1023():
    numbers = random.sample(range(1,1024), 1023)
    t = hw2.Tree()
    for i in range(len(numbers)):
        t.Insert(hw2.Node(numbers[i]))
    return t.root.Height(t.root)


def BuildTrees():
    height = np.zeros(1000)
    for i in range(1000):
        height[i] = BuildTree1023()
    print('Average height of the tree is %f'%np.mean(height))


if __name__ == '__main__':
    
    question1()
    print('-'*80)
    question4()
    print('-'*80)
    BuildTrees()
