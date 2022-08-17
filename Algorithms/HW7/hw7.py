
class lexicon:
    def __init__(self):
        file1 = open('/Users/archana/Dropbox/Algo/HW7/hw7.txt','r')
        words = file1.readlines()
        self.word_array = [s.strip('\n') for s in words]
    
    def get_index(self, input_string, first, last):
        word_len = len(input_string)
        if last < first:
            return last
        if word_len == 0:
            return -1
        mid = (first + last) // 2
        if self.word_array[mid][0:word_len] < input_string:
            return self.get_index(input_string, mid + 1, last)
        elif self.word_array[mid][0:word_len] > input_string:
            return self.get_index(input_string, first, mid - 1)
        else:
            while self.word_array[mid][0:word_len] == self.word_array[mid-1][0:word_len]:
                mid = mid - 1
            if self.word_array[mid] == input_string:
                return mid
            return mid - 1

    def find_after(self,input_string):
        first = 0
        last = len(self.word_array) - 1
        index = self.get_index(input_string,first,last)
        next_index = index + 1
        if next_index == last+1:
            return None
        return next_index

    def next5(self,input_string):
        first = 0
        last = len(self.word_array)
        index = self.get_index(input_string,first,last)
        next5_words = []
        next_index = index + 1
        num = 0
        while next_index < last and num < 5:
            next5_words.append(self.word_array[next_index])
            next_index = next_index + 1
            num = num + 1
        return next5_words

    def prefix5(self,input_string):
        first = 0
        last = len(self.word_array)
        index = self.get_index(input_string,first,last)
        next5_prefix_words = []
        next_index = index + 1
        num = 0
        word_len = len(input_string)
        while next_index < last and num < 5:
            if self.word_array[next_index][0:word_len] == input_string:
                next5_prefix_words.append(self.word_array[next_index])
            next_index = next_index + 1
            num = num + 1
        return next5_prefix_words


def retrieve_all():
    l = lexicon()
    all_words = []
    num = 5
    a = ''
    while num >= 5 :
        words_5 = l.next5(a)
        all_words.extend(words_5)
        num = len(words_5)
        if num >= 5:
            a = words_5[4]
    print(all_words)
#    if all_words == l.word_array:
#        print('yes')

    assert all_words == l.word_array


class chars:
    def __init__(self,value):
        self.parent = None
        self.child = None
        self.sibling = None
        self.value = value

    def add_child(self,other):
        other.parent = self
        if self.child is None:
            self.child = other
        else:
            ch = self.child
            if other.value <= ch.value:
                other.sibling = ch
                self.child = other
            else:
                while ch.sibling != None and other.value > ch.sibling.value:
                    ch = ch.sibling
                new = ch.sibling
                ch.sibling = other
                other.sibling = new

    def find(self,string):
        while len(string) > 0:
            a = len(self.value)
            if self.value == string[0:a]:
                if self.value == string:
                    node = self
                    break
                self = self.child
                string = string[a:]
            else:
                self = self.sibling
        return node


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


def test1():
    new = lexicon()
    print(new.find_after(''))
    print(new.find_after('mo'))
    print(new.find_after('motion'))
    print(new.find_after('zone'))
    print(new.find_after('zu'))
    print(new.next5('retirement'))
    print(new.next5('yea'))
    print(new.prefix5('yea'))


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

    print(top.walk())


if __name__ == "__main__":
    test1()
#    retrieve_all()
    test2()
