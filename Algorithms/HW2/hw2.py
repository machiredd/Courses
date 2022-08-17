class Tree:
    def __init__(self):
        self.root = None

    def Insert(self,z):
        y = None
        x = self.root
        while x is not None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

    def Transplant(self,u,v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def Delete(self,z):
        if z.left is None:
            self.Transplant(z,z.right)
        elif z.right is None:
            self.Transplant(z,z.left)
        else: 
            y = z.right.Min()
            if y.parent is not None:
                self.Transplant(y,y.right)
                y.right = z.right
                if y.right is not None:
                    y.right.parent = y
            self.Transplant(z,y)
            y.left = z.left
            y.left.parent = y

    def Insert_new(self,z):
        y = None
        x = self.root
        
        if x is None:
            self.root = z
            return
        
        while x is not None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if z.key < y.key:
            y.left = z
        else:
            y.right = z

class Node:
    def __init__(self,k):
        self.key = k
        self.left = None
        self.right = None
        self.parent = None

    def InOrderWalk(self):
        s = ""
        if self.left is not None:
            s += self.left.InOrderWalk()
        s += str(self.key)
        if self.right is not None:
            s += self.right.InOrderWalk()
        return s

    def Search(self,k):
        if k ==self.key:
            return self
        if k < self.key and self.left is not None:
            return self.left.Search(k)
        if k > self.key and self.right is not None:
            return self.right.Search(k)
        return None

    def Min(self):
        x = self
        while x.left is not None:
            x = x.left
        return x

    def Max(self):
        x = self
        while x.right is not None:
            x = x.right
        return x

    def Succ(self):
        x = self
        if x.right is not None:
            return x.right.Min()
        y = x.parent
        while y is not None and x == y.right:
            x = y
            y = y.parent
        return y
    
    def __str__(self):
        s = ""
        if self.left is not None:
            s += '('
            s += str(self.left)
            s += ')'
        s += str(self.key)
        if self.right is not None:
            s += '('
            s += str(self.right)
            s += ')'
        return s


    def Height(self,x):
        if x is None:
            return 0
        else:
            left_height = self.Height(x.left)
            right_height = self.Height(x.right)

        return 1 + max(left_height,right_height)



