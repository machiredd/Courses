#!usr/bin/python

from __future__ import division
from ngrammodel import MaximumLikelihoodNGramModel
from collections import defaultdict
import operator
from bitweight import BitWeight, INF
import random
from bitweight import BitWeight
from numpy import array, int8, ones, zeros,dtype,arange,argmax
from copy import deepcopy
from tabulate import tabulate
import time

t0=time.time()

result = open('output_mle.txt', 'w')
check = open('crosscheck_mle.txt','w')
actual = open('text_mle.txt','w')
file=open('wsj-normalized.pos','r')
lines=file.readlines()

# Split data into training and testing
random.shuffle(lines)
b=int(0.9*(len(lines)))
train=lines[:b]
test=lines[b+1:]

print "Number of lines in training = %d" %len(train)
print "Number of lines in test = %d" %len(test)

################################## Training #############################################
new_wt=[]
tags=[]
words=[]
new_tags=[]

# Remove end of line character
new_lines=[train[i].replace('\n','') for i in xrange(len(train))]
# Split line to words
word_tags=[new_lines[i].split(' ') for i in xrange(len(new_lines))]
# Split the word/tag to 'word','tag'
for line in word_tags:
    new_wt.append([line[i].rsplit('/',1) for i in xrange(len(line))])

new_wt_2=deepcopy(new_wt)

# Separating tags of the for IN|RB to IN and RB
for line in new_wt:
    for i in xrange(len(line)):
        if '|' in line[i][1]:
            tags1=line[i][1].rsplit('|')
            line[i][1]=tags1[0]
            for j in xrange(len(tags1)-1):
                newline=deepcopy(line)
                newline[i][1]=tags1[j+1]
                new_wt.append(newline[i-1:i+2])
# Collect all tags
for line in new_wt:
    tags.append([line[i][1] for i in xrange(len(line))])
# Calculate transition probabilities
m=MaximumLikelihoodNGramModel(tags, 2)

# Getting the list of tags
counts = defaultdict(int)
for line in tags:
    for j in xrange(len(line)):
        counts[line[j]] += 1
sorted_c = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
# Prints the tag frequency table
#print tabulate(sorted_c)

# Preparing words with tags separated
for line in new_wt_2:
    for i in xrange(len(line)):
        if '|' in line[i][1]:
            tags2=line[i][1].rsplit('|')
            for j in xrange(len(tags2)-1):
                line.insert(i+1,[line[i][0],tags2[j+1]])
            line[i][1]=tags2[0]

# Collect all words
for line in new_wt:
    words.append([line[i][0] for i in xrange(len(line))])

# Calculate emission probabilities
freque = defaultdict(lambda: defaultdict(int))
for line in new_wt:
    for i in xrange(len(line)):
        freque[line[i][0]][line[i][1]] +=1
probab = defaultdict(lambda: defaultdict(lambda: BitWeight()))
for (prefix, suffixes) in freque.iteritems():
    denominator = BitWeight(sum(suffixes.values()))
    fdist = freque[prefix]
    pdist = probab[prefix]
    for suffix in suffixes:
        pdist[suffix] = BitWeight(fdist[suffix]) / denominator
# Assign all OOV words to nouns
probab[('UNK')]={"NN":BitWeight(1)}

t1=time.time()
print 'training time:'
print t1-t0

###################################### Testing ###########################################
# Preparing test data
new_wt_test=[]
tags_test=[]
words_test=[]

# Remove end of line character
test_lines=[test[i].replace('\n','') for i in xrange(len(test))]
# Split line to words
word_tags_test=[test_lines[i].split(' ') for i in xrange(len(test_lines))]
# Split the word/tag to 'word','tag'
for line in word_tags_test:
    new_wt_test.append([line[i].rsplit('/',1) for i in xrange(len(line))])

# Collect all tags and words
for line in new_wt_test:
    tags_test.append([line[i][1] for i in xrange(len(line))])
    words_test.append([line[i][0] for i in xrange(len(line))])
    # Save the tags evaluation
    check.write(' '.join(line[i][1] for i in xrange(len(line))))
    check.write("\n")
    # Save the words to see which words were tagged wrong
    actual.write(' '.join(line[i][0] for i in xrange(len(line))))
    actual.write("\n")

# Viterbi Algorithm, Tagging the lines in test

# Get list of all states
states=counts.keys()
state_lookup = dict(enumerate(states))

input=words_test #each line
nlines=0

# Tagging all new words in test to 'UNK'
dictionary=sorted(probab)
mapping = defaultdict(lambda: 'UNK')
for words in dictionary:
    mapping[words]=words

for line in input:
    nlines += 1
    # Tagging all new words in test to 'UNK'
    line=[mapping[v] for v in line]
    emis_lookup = dict(enumerate(line))
    
    prob_mat=zeros((len(state_lookup),len(emis_lookup)),dtype=BitWeight)
    lookup=zeros((len(state_lookup),len(emis_lookup)))
    best_path=zeros(len(emis_lookup))
    
    # Calculate values of first column of probability matrix
    list_keys=probab[line[0]].keys()
    for keys in list_keys:
        prob_mat[state_lookup.values().index(keys),0]=m.prob[('<S_0>',)][keys]*probab[line[0]][keys]

    # Populate the rest of the prob_mat and the look up table
    for i in arange(1,len(line)):
        list_keys=probab[line[i]].keys()
        for keys in list_keys:
            temp=[]
            for k in arange(len(prob_mat)):
                # If an state transition unseen in the training data is present,
                # transition probability is made to be same as transition from first state to state 'NN'
                if (prob_mat[k,i-1] !=0 and m.prob[(state_lookup[k],)][keys].to_real == 0):
                    m.prob[(state_lookup[k],)][keys] = m.prob[(state_lookup[k],)]['NN']
                # Get probabilities of all possible transitions to that state
                temp.append(m.prob[(state_lookup[k],)][keys]*prob_mat[k,i-1])
            lookup[state_lookup.values().index(keys),i]=argmax(temp)
            prob_mat[state_lookup.values().index(keys),i]=max(temp)*probab[line[i]][keys]

    # Final state
    final_state=argmax(prob_mat[:,-1])
    best_path[-1]=final_state
    
    # Get the best path
    for i in arange(len(emis_lookup)-1,0,-1):
        best_path[i-1]=lookup[best_path[i],i]
    best_path=best_path.astype(int)
    
    # Write the tags into a file
    #print ' '.join(state_lookup[i] for i in best_path)
    result.write(' '.join(state_lookup[i] for i in best_path))
    result.write("\n")
    if nlines % 100 ==0:
        print "%d/%d lines processed" %(nlines,len(test))

result.close()
file.close()
check.close()
actual.close()

t2=time.time()
print 'testing time:'
print t2-t1





