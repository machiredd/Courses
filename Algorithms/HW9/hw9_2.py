class lexicon:
    def __init__(self):
        self.data = []
        with open("/Users/archana/Dropbox/Algo/HW7/hw7.txt","r") as f:
            for line in f:
                line = line.strip()
                self.data.append(line)
        self.len = len(self.data)
    
    def find_after(self,item):
        """
            finds location of item.
            If item is not in list, finds spot of next largest item
            """
        
        if item >= self.data[-1]:
            return None
        
        start = 0
        end = self.len
        while True:
            if end-start == 1:
                #print("find " + str(start) + " " + str(end))
                return start
            half = int((start+end)/2)
            #print("find_sub " + str(start) + " " + str(half) + " " + str(end))
            if item >= self.data[half-1]:
                start = half
            else:
                end = half

    def next5(self,item):
        i = self.find_after(item)
        #print("Got back " + str(i))
        if i is None:
            return []
        e = min(i+5,self.len)
        return self.data[i:e]

    def prefix5(self,item):
        i = self.find_after(item)
        #print("Got back " + str(i))
        if i is None:
            return []
        e = min(i+5,self.len)
        ret = []
        for w in self.data[i:e]:
            if w.startswith(item):
                ret.append(w)
        return ret

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
        if string.find(self.value) != 0:
            return None
        string = string[len(self.value):]
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
            next.print_tree(indent+" "*(len(self.value)))
            next = next.sibling

#    def split_node(self,prefix):
#        b = self.value[len(prefix):]
#        self.value = prefix
#        c = self.child
#        self.child = chars(b)
#        self.child.parent = self
#        if self.word == True:
#            self.child.word = True
#        self.child.child = c
#        if b != "":
#            self.word = False
#        if c != None:
#            self.child.child.parent = self.child
#            next = self.child.child.sibling
#            while next is not None:
#                next.parent = self.child
#                next = next.sibling

    def split_node(self,prefix):
        b = self.value[len(prefix):]
        self.value = prefix
        c = self.child
        self.child = chars(b)
        self.child.parent = self
        if self.word == True:
            self.child.word = True
        self.child.child = c
        if b != "":
            self.word = False
        n = self.child.child
        while n is not None:
            n.parent = self.child
            n = n.sibling


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

#    def set_word(self,next,sub_added):
#        node1 = next.child
#        while node1 is not None:
#            if node1.value == sub_added:
#                node1.word = True
#                break
#            else:
#                node1 = node1.sibling

#    def add_word(self,word):
#        node, sub = self.find_partial(word)
#        next = node.child
#        while next is not None:
#            com = self.common_sub(next.value,sub)
#            if com != "":
#                next.split_node(com)
#                if sub[len(com):] != "":
#                    next.add_child(chars(sub[len(com):]))
#                    self.set_word(next,sub[len(com):])
#                else:
#                    next.word = True
#                return
#            else:
#                next = next.sibling
#        if sub != "":
#            node.add_child(chars(sub))
#            self.set_word(node,sub)
#        return

    def get_word(self):
        word = ""
        node = self
        while node is not None:
            print(node.value)
            word =  node.value + word
            node = node.parent
        return word


    def add_word(self,word):
        node, sub = self.find_partial(word)
        if sub == "":
            print('Word already in trie')
            node.word = True
            return node
        next = node.child
        while next is not None:
            com = self.common_sub(next.value,sub)
            if com == "":
                next = next.sibling
                continue
            next.split_node(com)
            if com != sub:
                new =chars(sub[len(com):])
                next.add_child(new)
                new.word = True
                return new
            next.word = True
            return next
        new = chars(sub)
        node.add_child(new)
        new.word = True
        return new



def create_trie():
    l = lexicon()
    start = ""
    top = chars("")
    while True:
        words = l.next5(start)
        if len(words) < 1:
            break
        for w in words:
            top.add_word(w)
        start = words[-1]
    return top

#def tokenize(trie,string):
#    queue = [(0,[])]
#    str_len = len(string)
#    answers = []
#    while queue:
#        start, tokens = queue.pop(0)
#        print(start,tokens)
#        if start == str_len:
#            answers.append(tokens)
#        else:
#            node, rem = trie.find_partial(string[start:])
#            done = len(string)-len(rem)
#            found = string[start:done]
#            if tokens == []:
#                new_tokens=[found]
#            else:
#                new_tokens = tokens+[found]
#            if node.word == True:
#                queue.append((done,new_tokens))
#            print('Found word %s'%(found))
#            print('Adding to frontier %s %i'%(found,done))
#            next = node.parent
#            l = len(node.value)
#            while next is not None:
#                new_l = len(found)-l
#                new_ll = done - l
#                if next.word == True:
#                    if tokens == []:
#                        new_tokens=[found[0:new_l]]
#                    else:
#                        new_tokens = tokens + [found[0:new_l]]
#                    queue.append((new_ll,new_tokens))
#                    print('Adding to frontier %s %i'%(found[0:new_l],new_ll))
#                else:
#                    print(' Node %s is not a word'%(found[0:new_l]))
#                l = l+len(next.value)
#                next = next.parent
#    return answers

def tokenize(trie,string):
    queue = [(0,[])]
    answers = []
    while queue:
        start, tokens = queue.pop(0)
        print(start,tokens)
        if start == len(string):
            answers.append(tokens)
            continue
        node, rem = trie.find_partial(string[start:])
        print('Found word %s'%(node.get_word()))
        while node is not None:
            w = node.get_word()
            if node.word:
                queue.append((start+len(w),tokens + [w]))
                print('Adding to frontier %s %i'%(w,start+len(w)))
            else:
                print(' Node %s is not a word'%(w))
            node = node.parent
    return answers

def test1():
    l = lexicon()
    print(l.find_after(''))
    print(l.find_after('mo'))
    print(l.find_after('motion'))
    print(l.find_after('zone'))
    print(l.find_after('zu'))
    print(l.next5('retirement'))
    print(l.next5('yea'))
    print(l.prefix5('yea'))

def test2():
    top = chars("r")
    top.add_child(chars("ub"))
    top.add_child(chars("om"))
    top.find("rom").add_child(chars("ulus"))
    top.find("rom").add_child(chars("an"))
    top.find("roman").add_child(chars("e"))
    top.find("roman").add_child(chars("us"))
    top.find("rub").add_child(chars("e"))
    top.find("rub").add_child(chars("ic"))
    top.find("rube").add_child(chars("ns"))
    top.find("rube").add_child(chars("r"))
    top.find("rubic").add_child(chars("on"))
    top.find("rubic").add_child(chars("undus"))
    top.print_tree()


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
    print(top.find("roman").get_word())




if __name__ == "__main__":
#    test2()
#    test_split_node()
#    test_4()

    trie = create_trie()
    trie.print_tree()
    print(trie.find("warm").get_word())
    token = tokenize(trie,'uponthewarmeat')
    print(token)
##
