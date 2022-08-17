import fst
import operator
import argparse

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
Adds words from a list to a trie
"""
def add_words(new_words,states,my_trans):
    for n,word in enumerate(new_words):
#        if n % 1000 == 0:
#            print n  # Print number of words processed
        state_ids = [state.stateid for state in my_trans.states] # Get list of all states in trie
        for idx,c in enumerate(word):
            if states[word[:idx]] in state_ids:
                arcs = [my_trans.osyms.find(x.olabel) for x in my_trans[states[word[:idx]]].arcs]
                if c in arcs: # If character already in trie at that state look at next character
                    continue
                else:
                    # else add an arc for that character
                    my_trans.add_arc(states[word[:idx]],states[word[:idx+1]],c,c)
            else:
                my_trans.add_arc(states[word[:idx]],states[word[:idx+1]],c,c)
        
        last_state = my_trans[states[word[:idx+1]]]
        last_state.final = True # Mark the final state
    return my_trans

"""
Searches for words matching a prefix in the trie
"""
class Search:
	
    def __init__(self,prefix):
        self.prefix = prefix
        self.suffix = []
        self.count = 0
        self.search_suff()
    """
    Performs depth first search for a given prefix
    """
    def dfs(self,new):
        arcs1 = [my_trans.osyms.find(x.olabel) for x in my_trans[states[new]].arcs]
        if arcs1 == []: # If no outgoing arcs, add word to final list
            self.suffix.append(new)
        if my_trans[states[new]].final != my_trans[states[""]].final: # Check if it is final state
            if new not in self.suffix: # If word not in list add to list
                self.suffix.append(new)
        if len(arcs1) == 1: # If only one arc, add to the prefix and continue searching
            new += arcs1[0]
            self.dfs(new)
        else:
            for arc in my_trans[states[new]].arcs: # If more than one arc, for every arc do depth first search
                out1 = new + my_trans.osyms.find(arc.olabel)
                self.dfs(out1)
    """
    Gets the list of arcs from the end state of prefix and calls for depth first search on each arc
    """
    def search_suff(self):
        arcs = [my_trans.osyms.find(x.olabel) for x in my_trans[states[self.prefix]].arcs]
        if arcs == [] and self.count == 1: # If there are no outgoing arcs, return the prefix
            self.suffix.append(self.prefix)
        self.count = 1
        if my_trans[states[self.prefix]].final != my_trans[states[""]].final: # Check if it is final state
            if self.prefix not in self.suffix: # If it is not already in the suffix list, append
                self.suffix.append(self.prefix)
        if len(arcs) == 1:  # If only one outgoing arc add character to prefix and repeat
            self.prefix += arcs[0]
            self.search_suff()
        else: # if there are more than one ars, do depth first search on each arc
            for arc in my_trans[states[self.prefix]].arcs:
                new_prefix = self.prefix + my_trans.osyms.find(arc.olabel)
                self.dfs(new_prefix)

################################
# Main program
###############################

parser = argparse.ArgumentParser()
parser.add_argument("train", help="a text file containing words, one word per line")
args = parser.parse_args()

# Get list of input words
words = args.train
new_words = [l.strip() for l in open(words).readlines()]
print sorted(new_words)

# Initialize the state counter
states = StateCounter()

# Initialize the transducer
my_trans = fst.Transducer()

# Read the symbol tables
letter_syms = fst.read_symbols("ascii.syms.bin")
my_trans.isyms = letter_syms
my_trans.osyms = letter_syms

# Build the trie
my_trans = add_words(new_words,states,my_trans)

# Get prefix from user and search for matchign words
prefix =[]
while prefix != "$":
     prefix = raw_input ("Enter a prefix or $ to end : ")
     if prefix == "$":
          break
     else:
          result = Search(prefix) # Search for matchign words
          print "Prefix : ", prefix
          if result.suffix == []:
               print "No matching words"
          else:
               print "Matching words : ", [x.encode('ascii') for x in result.suffix]
     
det_words = my_trans.determinize()
det_words.remove_epsilon()
det_words.arc_sort_input()
det_words.write("determinized_words.fst") # Save the FST
