import fst
import operator
import argparse
import string
from collections import OrderedDict

class StateCounter(object):
    def __init__(self):
        self.set = {}
        self.count = -1
        
    def __contains__(self, obj):
        return obj in self.set
 
    def __getitem__(self, obj):
        if not obj in self.set:
            self.count += 1
            self.set[obj] = self.count
        return self.set[obj]

def add_words(new_words,states,my_trans):
    for n,word in enumerate(new_words):
#        if n % 1000 == 0:
#           print n
        state_ids = [state.stateid for state in my_trans.states]
        for idx,c in enumerate(word):
            if states[word[:idx]] in state_ids:
                arcs = [my_trans.osyms.find(x.olabel) for x in my_trans[states[word[:idx]]].arcs]
                if c in arcs:
                    continue
                else:
                    my_trans.add_arc(states[word[:idx]],states[word[:idx+1]],c,c)
            else:
                my_trans.add_arc(states[word[:idx]],states[word[:idx+1]],c,c)

        last_state = my_trans[states[word[:idx+1]]]
        last_state.final = True
    return my_trans

def leven_aut(word,edit,fst1,states1):
    for idx,c in enumerate(word):
        for d in xrange(edit+1):
            # Correct charater
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d)],c,c,0)

            if d < edit:
            # Deletion
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"<epsilon>",10)
    
		    # Insertion
		    fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","a",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","b",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","c",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","d",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","e",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","f",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","g",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","h",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","i",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","j",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","k",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","l",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","m",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","n",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","o",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","p",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","q",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","r",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","s",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","t",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","u",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","v",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","w",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","x",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","y",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","z",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","A",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","B",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","C",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","D",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","E",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","F",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","G",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","H",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","I",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","J",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","K",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","L",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","M",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","N",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","O",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","P",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","Q",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","R",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","S",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","T",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","U",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","V",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","W",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","X",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","Y",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","Z",10)
            # Insertion of same character is common like in embarrass
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>",c,6)


            if c in ["a","e","i","o","u"]: # Insertion of a vowel after vowel is less costly
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","a",6)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","e",6)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","i",6)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","o",6)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","u",6)


		    # Substitution
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"a",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"b",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"c",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"d",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"e",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"f",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"g",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"h",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"i",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"j",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"k",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"l",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"m",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"n",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"o",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"p",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"q",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"r",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"s",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"t",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"u",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"v",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"w",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"x",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"y",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"z",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"A",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"B",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"C",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"D",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"E",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"F",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"G",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"H",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"I",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"J",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"K",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"L",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"M",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"N",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"O",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"P",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"Q",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"R",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"S",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"T",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"U",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"V",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"W",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"X",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"Y",10)
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"Z",10)
    
            # Swapping of vowels is more common, specially 'e' and 'i'
            if c == "a":
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"e",3)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"i",3)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"o",5)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"u",5)
            if c == "e":
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"a",3)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"i",2)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"o",5)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"u",5)
            if c == "i":
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"a",5)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"e",2)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"o",3)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"u",5)
            if c == "o":
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"a",5)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"e",5)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"i",3)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"u",5)
            if c == "u":
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"a",3)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"e",5)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"i",5)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"u",5)	

            # Swapping phonetically similar letter is common, 'c' and 'k', 'c' and 's'(advice,advise)
            if c == "c":
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"k",5)
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"s",3)
            if c == "k":
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"c",5)
            if c == "s":
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"c",3)

            # Swapping consonants for consonants in more common than consonant and vowel
		    if c in ["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"]:
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"b",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"c",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"d",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"f",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"g",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"h",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"j",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"k",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"l",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"m",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"n",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"p",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"q",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"r",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"s",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"t",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"v",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"w",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"x",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"y",8)
                 fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"z",8)

    for d in xrange(edit+1):
        if d < edit:
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","a",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","b",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","c",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","d",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","e",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","f",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","g",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","h",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","i",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","j",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","k",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","l",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","m",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","n",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","o",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","p",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","q",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","r",10)
            # Addition of 's' at the end is more common than other characters
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","s",2)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","t",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","u",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","v",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","w",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","x",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","y",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","z",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","A",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","B",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","C",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","D",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","E",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","F",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","G",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","H",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","I",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","J",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","K",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","L",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","M",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","N",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","O",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","P",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","Q",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","R",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","S",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","T",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","U",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","V",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","W",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","X",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","Y",10)
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","Z",10)  

        last_state = fst1[states1[str((len(word[:idx+1])*20)+d)]]
        last_state.final = True # Record final state
    last_state = fst1[states1[str((len(word[:idx+1])*20)+d+1)]]
    last_state.final = True # Record final state
    return fst1

class combine:
    def __init__(self,lev,dic,symboltable):
        self.matches = []
        self.s = ""
        self.calc(symboltable,lev,dic)
    
    # Depth first search on the arcs
    def similar(self,s1,state1,state2,symboltable,lev,dic,w_l):
        # Get common arcs in lev and trie
        arcs_lev = [(symboltable.find(x.olabel).encode("ascii"),x.nextstate,x.weight) for x in state1.arcs]
        arcs_dic = [(symboltable.find(x.olabel).encode("ascii"),x.nextstate) for x in state2.arcs]
        lev_com = [rec for rec in arcs_lev if rec[0] in [y[0] for y in arcs_dic]]
        dic_com = [rec for rec in arcs_dic if rec[0] in [y[0] for y in arcs_lev]]

        # Get a list of the form (char, lev_nextstate, trie_nextstate)
        D=[]
        for k1,v1,w1 in lev_com:
            for k2,v2 in dic_com:
                if k1 == k2:
                    D.append((k1,v1,w1,v2))
                        del_state = [item for item in arcs_lev if item[0] == "<epsilon>"] # Add epsilon state to the list
        if del_state != []:
            del_add = del_state[0] + (state2.stateid,)
            D.append(del_add)

        # Get the next states and note the word and weight if it is final state, else search arcs of that state
        for i in xrange(len(D)):
            state1 = lev[D[i][1]]
            state2 = dic[D[i][3]]
            s2 = s1 + D[i][0]
            w_l2 = w_l + float(D[i][2]) # Add the weight along the path
            if state1.final != lev[states[""]].final and state2.final != dic[states[""]].final:
                if (s2,w_l2) not in self.matches:
                    s2 = string.replace(s2,"<epsilon>","")
                    self.matches.append((s2,w_l2)) # Store the word and the weight
            self.similar(s2,state1,state2,symboltable,lev,dic,w_l2)

    # Get list of initial common arcs
    def calc(self,symboltable,lev,dic):
        state1 = lev[0] # state 0 in lev
        state2 = dic[0] # state 0 in trie
        # Get common arcs in lev and trie
        arcs_lev = [(symboltable.find(x.olabel).encode("ascii"),x.nextstate,x.weight) for x in state1.arcs]
        arcs_dic = [(symboltable.find(x.olabel).encode("ascii"),x.nextstate) for x in state2.arcs]
        lev_com = [rec for rec in arcs_lev if rec[0] in [y[0] for y in arcs_dic]]
        dic_com = [rec for rec in arcs_dic if rec[0] in [y[0] for y in arcs_lev]]
        
        # Get a list of the form (char, lev_nextstate, trie_nextstate)
        D=[]
        for k1,v1,w1 in lev_com:
            for k2,v2 in dic_com:
                if k1 == k2:
                    D.append((k1,v1,w1,v2))
        del_state = [item for item in arcs_lev if item[0] == "<epsilon>"]
        del_add = del_state[0] + (state2.stateid,)
        D.append(del_add)
        
        # Get the next states and note the word and weight if it is final state, else search arcs of that state
        for i in xrange(len(D)):
            state1 = lev[D[i][1]]
            state2 = dic[D[i][3]]
            s1 = self.s + D[i][0]
            w_l = float(D[i][2]) # Initialize the weight
            if not state1 and state2:
                if s1 not in self.matches:
                    s1 = string.replace(s1,"<epsilon>","")
                    self.matches.append((s1,w_l)) # Store word and weight
        self.similar(s1,state1,state2,symboltable,lev,dic,w_l) # Call for depth first search on the common arcs

######################
# Main Prog
#####################

# Get input file with list of words
parser = argparse.ArgumentParser()
parser.add_argument("train", help="a text file containing words, one word per line")
args = parser.parse_args()
words = args.train
new_words = [l.strip() for l in open(words).readlines()]
print sorted(new_words)

# Initialize the state counter and FST
states = StateCounter()
my_trans = fst.Transducer()

# Load the symbol table
letter_syms = fst.read_symbols("ascii.syms.bin")
my_trans.isyms = letter_syms
my_trans.osyms = letter_syms

# Add words to the trie
my_trans = add_words(new_words,states,my_trans)

# Determnize the trie and sort arcs
det_words = my_trans.determinize()
det_words.remove_epsilon()
det_words.arc_sort_input()

# Prompt to get a word and edit distance
word_input=[]
while word_input != "$":
    word_input =raw_input("Enter a word or $ to end: ")
    if word_input == "$":
        break
    else:
        dist = raw_input("Edit distance : ")
        lev_cons = fst.Transducer() # Initialize FST
        lev_cons.isyms = letter_syms
        lev_cons.osyms = letter_syms
        states1=StateCounter()
        # Build the Levenshtein automaton
        out = leven_aut(word_input,int(dist),lev_cons,states1)
        # Traverse through trie and Levenshtein automaton to get common words
        new = combine(out,det_words,lev_cons.osyms)
        print "Matches found : ",list(OrderedDict.fromkeys([x[0] for x in new.matches]))
        # Sort the words according to their weights
        mat_sort = [x[0] for x in sorted(new.matches, key=lambda y: y[1])]
        final_matches = list(OrderedDict.fromkeys(mat_sort))
        print "Reordered matches : ",final_matches

