class chars:
    def __init__(self,value):
        self.parent = None
        self.child = None
        self.sibling = None
        self.value = value

    def add_child(self,other):
        other.parent = self
        if self.child == None:
            self.child = other
            print("Added ‘%s’ as 1st child to ‘%s’" % (other.value,self.value))
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
        print("%s%s"%(indent,self.value))
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
        self.child.child = c

    def find_partial(self,string,indent=""):
        print("%sSearching for ‘%s’ starting from node with value ‘%s’" %
          (indent,string,self.value))
        if string.find(self.value) != 0:
            return (None,string)
        string = string[len(self.value):]
        last = self
        print("%s Found! Now left with ’%s’" % (indent,string))
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



# def add_word(self,word):
#     if self.value == '':
#         self.value = word
#         return
#     node, sub = self.find_partial(word)
#     print('1111',self.value,sub)
#     com = self.common_sub(self.value,sub)
#     print(com)
#     self.split_node(com)
#     node, sub = self.find_partial(word)
#     node.add_child(chars(sub))

    def add_word(self,word):
        print('..........',word,'..........')
        if self.value == '':
            self.value = word
            return
        node, sub = self.find_partial(word)
        if node == None:
            com = self.common_sub(self.value,sub)
            if com != "":
                print(com)
                self.split_node(com)
                self.add_child(chars(sub[len(com):]))
                return
            else:
                self.add_child(chars(sub))
                return
        print('1111',node.value,sub)
        next = self.child
        while next is not None:
            print('searching',next.value,sub)
            com = self.common_sub(next.value,sub)
            if com != "":
                print(com)
                next.split_node(com)
                next.add_child(chars(sub[len(com):]))
                return
            else:
                next = next.sibling
        node.add_child(chars(sub))
        return

def test2():
    top = chars("r")
    top.add_child(chars("ub"))
    top.add_child(chars("om"))
    top.find("rom").add_child(chars("ulus"))
    top.find("rom").add_child(chars("an"))
    top.find("roman").add_child(chars("e"))
    top.find("roman").add_child(chars("us"))
    #    top.find("r").add_child(chars("om"))
    #    top.find("r").add_child(chars("od"))
    #    top.find("r").add_child(chars("an"))
    #    top.find("r").add_child(chars("ur"))
    top.find("rub").add_child(chars("e"))
    top.find("rub").add_child(chars("ic"))
    top.find("rube").add_child(chars("ns"))
    top.find("rube").add_child(chars("r"))
    top.find("rubic").add_child(chars("on"))
    top.find("rubic").add_child(chars("undus"))
    
#    print(top.walk())
    top.print_tree()
    r,left = top.find_partial('rub')
    print(r,left)
    r,left = top.find_partial('romain')
    print(r,left)
    r,left = top.find_partial('robust')
    print(r,left)


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
    top.print_tree()
    top.add_word("romane")
    top.print_tree()
    top.add_word("romanus")
    top.add_word("rome")
    top.print_tree()
    top.add_word("rose")
    top.print_tree()
    top.add_word("roment")
    top.print_tree()
    top.add_word("roses")
    top.print_tree()


if __name__ == "__main__":
#    test2()
#    test_split_node()
    test_4()
