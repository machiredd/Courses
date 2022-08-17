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
    print(l.prefix5(''))

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


def simple():
    l = lexicon()
    start = ""
    while True:
        words = l.prefix5(start)
        if len(words) < 1:
            break
        for w in words:
            print(w.lower())
        start = words[-1]




if __name__ == "__main__":
#    test1()
    simple()
#    test2()
