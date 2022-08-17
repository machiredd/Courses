#!/usr/bin/python

import string
import re
import matplotlib.pyplot as plt
from tabulate import tabulate
from operator import itemgetter
import numpy as np
from pylab import pcolor, show, colorbar

re.UNICODE
# RE for chapter numbers
RE1='Chapter \d*'
# RE for Mr., Mrs., Miss, Lady
a='[ML][r*ia*][s*d*\.?]s*\.*y?'
# RE for ('s,--)
d='[\'-][s-].*'
# RE to match de Bourgh (surnames starting with small letters)
e='.*\s[A-Z].*'

file=open('pg1342.txt','r')

Ch_count=0
count=0
list1=[]
list2=[]
check=[]
number=0
lines=file.readlines()
ch_start=[]

# Find the lines in which chapter numbers appear
for i in range(0,len(lines)):
    if re.match(RE1,lines[i]):
        ch_start.append(i);
ch_start.append(len(lines))

# For each chapter calculate the histogram of surnames
for k in range(0,len(ch_start)-1):
    Ch_count+=1
    list1=[]
    for j in range(ch_start[k],ch_start[k+1]):
        if not re.match(RE1,lines[j]):
            line=lines[j]
            for match in re.findall(a,line):
                words=line.split()
                for i,w in enumerate(words):
                    if w==match:
                        # Check if pattern is the last word in the line, if so take the first word in next line, else take the word that follows
                        if i==len(words)-1:
                            n_line=lines[j+1].split()
                            if n_line!=[]:
                                name=n_line[0]
                                if (n_line[0][0].islower() and n_line[1][0].isupper()):
                                    if not re.match(a,n_line[1]):
                                        name=' '.join([n_line[0],n_line[1]])
                                    else:
                                        name=n_line[2]
                        elif i==len(words)-2:
                            if words[i+1][0].isupper():
                                name=words[i+1]
                        elif i<=len(words)-3:
                            if words[i+1][0].isupper():
                                name=words[i+1]
                            if (words[i+1][0].islower() and words[i+2][0].isupper()):
                                if not re.match(a,words[i+2]):
                                    name=' '.join([words[i+1],words[i+2]])
                                else:
                                    name=words[i+3]
                        # Remove "'s","--" and other punctuation marks attached to the surname
                        name=re.sub(d,'',name)
                        #if name[0].isupper():
                        for ci in string.punctuation:
                            name=name.replace(ci,"")
                            # Store all occurances of surnames in a list
                        if (name[0].isupper() or re.match(e,name)):
                            list1.append(name)

    # Calculate histogram
    for word in list1:
        if word in check:
            list2[check.index(word)][Ch_count]+=1
        else:
            list2.append([word])
            check.append(word)
            list2[check.index(word)]+=[0]*(len(ch_start)-1)
            list2[check.index(word)][Ch_count]=1
            count=count+1

# Sort surnames alphabetically
D=sorted(list2, key=itemgetter(0))

names=sorted(check, key=itemgetter(0))
print (names)
print 'There are %d surnames'%count

# Plot the distribution of surnames amoung the chapters
mat=[]
for k in range(len(D)):
    mat.append(D[k][+1:])

for a in range(len(D)):
    for b in range(len(ch_start)-1):
        mat[a][b]=float(mat[a][b])

mat=np.asarray(mat)
print mat[2]

mat1=mat
for a in range(len(D)):
    #local=max(mat[a])
    local=max(mat[a])
    if a ==0:
        tot1=max(mat[a])
        tot2=sum(mat[a])
    for b in range(len(ch_start)-1):
        mat[a][b]=mat[a][b]/local
print 'Maximum number of times the name is seen : %d' %tot1
print mat[0]


mat=mat1
for a in range(len(D)):
    #local=max(mat[a])
    local=sum(mat[a])
    for b in range(len(ch_start)-1):
        mat[a][b]=mat[a][b]/local
print 'Total number of times the name is seen : %d' %tot2
print mat[0]

#pcolor(mat,cmap="OrRd")
pcolor(mat,cmap="binary")
colorbar()
plt.yticks(range(len(D)), [x[0] for x in D])
plt.gca().yaxis.grid(True)
plt.gca().xaxis.grid(True)
plt.xlabel('Chapters')
plt.xlim([0,len(ch_start)-1])
plt.ylim([0,len(D)])
show()

