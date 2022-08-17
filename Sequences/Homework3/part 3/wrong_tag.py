#!usr/bin/python

from __future__ import division
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from pylab import pcolor, show, colorbar



file1 = open('crosscheck_mle.txt', 'r')
file2 = open('output_mle.txt', 'r')
file3 = open('text_mle.txt','r')
file4 = open('wrong_tagged_words_mle.txt','w')
file5 = open('wrong_sorted_mle.txt','w')

#tags=['JJ|IN', 'PRP$', 'RB|RP', 'VBG', 'IN|RB', 'VBD', 'NNPS|NNS', 'JJ|JJR', 'VBG|NN', '``', 'VBN', 'POS', "''", 'NN|CD', 'VBP', 'WDT', 'JJ', 'WP', 'VBZ', 'DT', 'NNS|NN', 'JJ|RB', 'NN|JJ', '#', 'RBR|JJR', 'RP', '$', 'NN', 'VBD|VBP', ')', '(', 'NNS|VBZ', 'FW', ',', '.', 'RB|IN', 'TO', 'PRP', 'RB', 'NN|NNS', 'JJ|VBN', 'VBD|VBN', ':', 'NNS', 'NNP', 'VB', 'WRB', 'VBG|NN|JJ', 'IN|JJ', 'JJ|NN', 'CC', 'LS', 'PDT', 'RBS', 'RBR', 'CD', 'VBP|VB', 'JJR|RBR', 'EX', 'IN', 'WP$', 'NNS|NNPS', 'VB|NN', 'VBG|JJ', 'MD', 'NNPS', 'RBS|JJS', 'VBN|VBD', 'VB|IN', 'JJS', 'JJR', 'SYM', 'RB|JJ', 'UH', 'NN|VBG', 'VBN|JJ', 'JJ|NNP', 'VBP|VBD', 'MD|VB', 'RB|DT']
#

tags=['PRP$', 'VBG', 'VBD', '``', 'VBN', 'POS', "''", 'VBP', 'WDT', 'JJ', 'WP', 'VBZ', 'DT', '#', 'RP', '$', 'NN', ')', '(', 'FW', ',', '.', 'TO', 'PRP', 'RB', ':', 'NNS', 'NNP', 'VB', 'WRB', 'CC', 'LS', 'PDT', 'RBS', 'RBR', 'CD', 'EX', 'IN', 'WP$', 'MD', 'NNPS', 'JJS', 'JJR', 'SYM', 'UH']

tags_lookup = dict(enumerate(tags))

conf_mat=np.zeros((len(tags),len(tags)))

lines1=file1.readlines()
lines2=file2.readlines()
lines3=file3.readlines()


for i in xrange(len(lines1)):
    grounttruth = lines1[i].split()
    result = lines2[i].split()
    words = lines3[i].split()
    for j in xrange(len(grounttruth)):
        conf_mat[tags_lookup.values().index(grounttruth[j])][tags_lookup.values().index(result[j])] +=1
        if grounttruth[j] != result[j]:
            file4.write(words[j]+"\t"+grounttruth[j]+"\t"+result[j]+"\n")

accuracy=np.trace(conf_mat)/np.sum(conf_mat)
print "Accuracy = %f" %accuracy
np.savetxt("conf_mat_mle.csv", conf_mat, delimiter=",")
file4.close()

lst = sorted(open('wrong_tagged_words_mle.txt','r').readlines(), key=str.lower)
file5.write(''.join(lst))


file5.close()
file1.close()
file2.close()
file3.close()
file4.close()


conf_mat /=  conf_mat.sum(axis=1)[:,np.newaxis]

pcolor(conf_mat,cmap='Paired')
colorbar()
plt.xticks(range(len(tags)), [x for x in tags],rotation='vertical',fontsize=10)
plt.yticks(range(len(tags)), [x for x in tags],fontsize=10)
plt.gca().yaxis.grid(True)
plt.gca().xaxis.grid(True)

plt.ylabel('Original tags')
plt.xlabel('Tags given by tagger')
show()
