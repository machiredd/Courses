class chars:
    def __init__(self,value):
        self.parent = None
        self.child = None
        self.sibling = None
        self.value = value
        self.word = False

    def add_child(self,other):
        other.parent = self
        if self.child == None:
            self.child = other
#            print("Added ‘%s’ as 1st child to ‘%s’" % (other.value,self.value))
            return
        if other.value <= self.child.value:
            other.sibling = self.child
            self.child = other
            return
        prev = self.child
        next = prev.sibling
        while next and next.value < other.value:
            prev = next
            next = next.sibling
        other.sibling = next
        prev.sibling = other

    def find(self,string,indent=""):
        print("%sSearching for ‘%s’ starting from node with value ‘%s’" %
              (indent,string,self.value))
        if string.find(self.value) != 0:
            return None
        string = string[len(self.value):]
        print("%s Found! Now left with ’%s’" % (indent,string))
        if string == "":
            return self
        next = self.child
        while next is not None:
            ret = next.find(string,indent+" ")
            if ret is not None:
                return ret
            next = next.sibling
        return None
    
    def walk(self,prefix=""):
        prefix += self.value
        if self.child is None:
            return [prefix]
        results = []
        ch = self.child
        while ch is not None:
            results.extend(ch.walk(prefix))
            ch = ch.sibling
        return results

    def print_tree(self,indent=""):
        if self.word == False:
            print("%s%s"%(indent,self.value))
        else:
            print("%s%s W"%(indent,self.value))
        next = self.child
        while next is not None:
            ret = next.print_tree(indent+" "*(len(self.value)))
            if ret is not None:
                return ret
            next = next.sibling
        return None

    def split_node(self,prefix):
        b = self.value[len(prefix):]
        self.value = prefix
        c = self.child
        self.child = chars(b)
        if self.word == True:
            self.child.word = True
        self.child.child = c
        if b != "":
            self.word = False

    def find_partial(self,string,indent=""):
        if string.find(self.value) != 0:
            return (None,string)
        string = string[len(self.value):]
        last = self
        if string == "":
            return (self,string)
        next = self.child
        while next is not None:
            ret,sub = next.find_partial(string,indent+" ")
            if ret is not None:
                return (ret,sub)
            next = next.sibling
        return (last,string)

    def common_sub(self,string_1,string_2):
        def _iter():
            for a, b in zip(string_1, string_2):
                if a == b:
                    yield a
                else:
                    return
        return ''.join(_iter())


    def add_word(self,word):
        if self.value == '':
            self.value = word
            self.word = True
            return
        node, sub = self.find_partial(word)
        if node == None:
            com = self.common_sub(self.value,sub)
            if com != "":
                self.split_node(com)
                self.add_child(chars(sub[len(com):]))
                self.child.word = True
                return
            else:
                self.sibling = chars(sub)
                return
        next = self.child
        while next is not None:
            com = self.common_sub(next.value,sub)
            if com != "":
                next.split_node(com)
                if sub[len(com):] != "":
                    next.add_child(chars(sub[len(com):]))
                    node1 = next.child
                    while node1 is not None:
                        if node1.value == sub[len(com):]:
                            node1.word = True
                            break
                        else:
                            node1 = node1.sibling
                else:
                    next.word = True
                return
            else:
                next = next.sibling
        if sub != "":
            node.add_child(chars(sub))
            node.child.word = True
        return

def test_split_node():
    top = chars("")
    top.add_child(chars("roman"))
    top.find("roman").add_child(chars("e"))
    top.find("roman").add_child(chars("us"))
    top.print_tree()
    top.find("roman").split_node("rom")
    top.print_tree()
    top.find("rom").add_child(chars("e"))
    top.print_tree()

def test_4():
    top = chars("")
    top.add_word("roses")
    top.add_word("romane")
    top.add_word("romanus")
    top.add_word("rome")
    top.add_word("rose")
    top.add_word("roment")
    top.add_word("roses")
    top.print_tree()

def test_4():
    top = chars("")
    top.add_word("roses")
    top.add_word("romane")
    top.add_word("romanus")
    top.add_word("rome")
    top.add_word("rose")
    top.add_word("roment")
    top.add_word("roses")
    top.print_tree()


if __name__ == "__main__":
#    test2()
#    test_split_node()
    test_4()
