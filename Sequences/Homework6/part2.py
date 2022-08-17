import fst
import operator
import argparse
import string

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

"""
Add words to a trie
"""
def add_words(new_words,states,my_trans):
    for n,word in enumerate(new_words):
#        if n % 1000 == 0:
#           print n
        state_ids = [state.stateid for state in my_trans.states]
        for idx,c in enumerate(word):
            if states[word[:idx]] in state_ids:
                arcs = [my_trans.osyms.find(x.olabel) for x in my_trans[states[word[:idx]]].arcs] # If arc present go to next character
                if c in arcs:
                    continue
                else:
                    my_trans.add_arc(states[word[:idx]],states[word[:idx+1]],c,c) # else add a new arc for the character
            else:
                my_trans.add_arc(states[word[:idx]],states[word[:idx+1]],c,c)

        last_state = my_trans[states[word[:idx+1]]]
last_state.final = True # Set last state
    return my_trans

"""
Construct the Levenshtein automaton for a given word and edit distance
"""
def leven_aut(word,edit,fst1,states1):
    for idx,c in enumerate(word):
        for d in xrange(edit+1):
            # Correct charater
            fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d)],c,c)
	        if d < edit:
                # Deletion
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"<epsilon>")
                 
                # Insertion
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","a")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","b")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","c")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","d")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","e")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","f")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","g")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","h")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","i")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","j")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","k")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","l")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","m")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","n")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","o")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","p")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","q")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","r")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","s")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","t")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","u")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","v")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","w")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","x")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","y")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","z")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","A")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","B")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","C")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","D")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","E")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","F")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","G")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","H")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","I")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","J")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","K")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","L")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","M")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","N")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","O")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","P")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","Q")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","R")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","S")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","T")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","U")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","V")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","W")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","X")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","Y")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx])*20)+d+1)],"<epsilon>","Z")


                # Substitution
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"a")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"b")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"c")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"d")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"e")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"f")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"g")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"h")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"i")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"j")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"k")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"l")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"m")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"n")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"o")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"p")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"q")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"r")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"s")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"t")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"u")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"v")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"w")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"x")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"y")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"z")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"A")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"B")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"C")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"D")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"E")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"F")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"G")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"H")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"I")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"J")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"K")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"L")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"M")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"N")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"O")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"P")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"Q")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"R")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"S")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"T")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"U")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"V")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"W")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"X")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"Y")
                fst1.add_arc(states1[str((len(word[:idx])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],c,"Z")


    for d in xrange(edit+1):
        if d < edit:
            # Insertion at the end if edits are still allowed
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","a")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","b")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","c")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","d")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","e")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","f")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","g")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","h")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","i")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","j")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","k")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","l")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","m")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","n")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","o")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","p")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","q")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","r")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","s")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","t")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","u")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","v")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","w")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","x")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","y")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","z")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","A")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","B")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","C")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","D")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","E")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","F")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","G")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","H")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","I")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","J")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","K")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","L")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","M")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","N")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","O")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","P")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","Q")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","R")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","S")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","T")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","U")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","V")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","W")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","X")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","Y")
            fst1.add_arc(states1[str((len(word[:idx+1])*20)+d)],states1[str((len(word[:idx+1])*20)+d+1)],"<epsilon>","Z")  

        last_state = fst1[states1[str((len(word[:idx+1])*20)+d)]]
        last_state.final = True # Mark final state
    last_state = fst1[states1[str((len(word[:idx+1])*20)+d+1)]]
    last_state.final = True # Mark final state
    return fst1

"""
Traverse through the trie and Levenshtein automaton to get common words
"""
class combine:
    def __init__(self,lev,dic,symboltable):
        self.matches = [] # initialize empty matches array
        self.s = "" # Initialize empty string
        self.calc(symboltable,lev,dic)

    # Depth first search along common arcs in trie and Levenshtein automaton (lev)
    def similar(self,s1,state1,state2,symboltable,lev,dic):
        # Get list of all arcs from a given state in lev and trie
        arcs_lev = [(symboltable.find(x.olabel).encode("ascii"),x.nextstate) for x in state1.arcs]
        arcs_dic = [(symboltable.find(x.olabel).encode("ascii"),x.nextstate) for x in state2.arcs]
        # Get list of all common arc in lev and trie
        lev_com = [rec for rec in arcs_lev if rec[0] in [y[0] for y in arcs_dic]]
        dic_com = [rec for rec in arcs_dic if rec[0] in [y[0] for y in arcs_lev]]
        
        # Rearrange such that a given character is followed by the next states in lev an trie (char, lev_next, trie_next)
        D=[]
        for k1,v1 in lev_com:
            for k2,v2 in dic_com:
                if k1 == k2:
                    D.append((k1,v1,v2))
        del_state = [item for item in arcs_lev if item[0] == "<epsilon>"]
        # if epsilon arc is present add to the list
        if del_state != []:
            del_add = del_state[0] + (state2.stateid,)
            D.append(del_add)
        
        # For each character traverse the arcs in both lev and trie
        for i in xrange(len(D)):
            state1 = lev[D[i][1]] # set next states
            state2 = dic[D[i][2]]
            s2 = s1 + D[i][0]  # append the string
            # If it is a final state append the list
            if state1.final != lev[states[""]].final and state2.final != dic[states[""]].final:
                if s2 not in self.matches:
                    s2 = string.replace(s2,"<epsilon>","")
                    self.matches.append(s2)
            # Continue search to next common arcs
            self.similar(s2,state1,state2,symboltable,lev,dic)

    # Get the first set of common arcs and call depth first search along each common arc
    def calc(self,symboltable,lev,dic):
        state1 = lev[0] # initial state
        state2 = dic[0]
        arcs_lev = [(symboltable.find(x.olabel).encode("ascii"),x.nextstate) for x in state1.arcs] # arcs form state 0 in lev
        arcs_dic = [(symboltable.find(x.olabel).encode("ascii"),x.nextstate) for x in state2.arcs] # arcs from state 0 in trie
        lev_com = [rec for rec in arcs_lev if rec[0] in [y[0] for y in arcs_dic]] # get common arcs
        dic_com = [rec for rec in arcs_dic if rec[0] in [y[0] for y in arcs_lev]]
        D=[]
        for k1,v1 in lev_com:
            for k2,v2 in dic_com:
                if k1 == k2:
                    D.append((k1,v1,v2)) # rearrage to get (char, lev_next_state, trie_next_state)
                        del_state = [item for item in arcs_lev if item[0] == "<epsilon>"] # Append epsilon arc state
                            del_add = del_state[0] + (state2.stateid,) # state in trie remains same, as there was deletion
        D.append(del_add)
        for i in xrange(len(D)): # For each common arc
            state1 = lev[D[i][1]]
            state2 = dic[D[i][2]]
            s1 = self.s + D[i][0]
            if not state1 and state2: # If final state, append the word
                if s1 not in self.matches:
                    s1 = string.replace(s1,"<epsilon>","")
                    self.matches.append(s1)
            self.similar(s1,state1,state2,symboltable,lev,dic) # Call for a depth first search on the common arcs

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
        lev_cons = fst.Transducer()  # Initialize a FST
        lev_cons.isyms = letter_syms
        lev_cons.osyms = letter_syms
        states1=StateCounter()
        out = leven_aut(word_input,int(dist),lev_cons,states1) # Build the Levenshtein automaton
        new = combine(out,det_words,lev_cons.osyms) # Traverse through trie and Levenshtein automaton to get common words
        print "Similar words : ",new.matches # Print results

