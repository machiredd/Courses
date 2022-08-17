#!/usr/bin/python

import string
import re
import matplotlib.pyplot as plt
from tabulate import tabulate
from operator import itemgetter

re.UNICODE

# RE for (Mr.,Mrs.,Miss,Lady)
a='[ML][r*ia*][s*d*\.?]s*\.*y?'
# RE for ('s,--)
d='[\'-][s-].*'
e='.*\s[A-Z].*'

# Open txt file
file=open('pg1342.txt','r')

count=0
list1=[]
list2=[]
check=[]

# Check if any of (Mr.,Mrs.,Miss,Lady) are present in a line and take its next word as a surname
for line in file:
    for match in re.findall(a,line):
        words=line.split()
        for i,w in enumerate(words):
            if w==match:
                # Check if pattern is the last word in the line, if so take the first word in next line
                if i==len(words)-1:
                    n_line=next(file).split()
                    if n_line!=[]:
                        name=n_line[0]
                        if (n_line[0][0].islower() and n_line[1][0].isupper()):
                            if not re.match(a,n_line[1]):
                                name=' '.join([n_line[0],n_line[1]])
                            else:
                                name=n_line[2]
                # If pattern is the last but one word in the line, and if the next word starts with a capital letter (condition to avoid words like and as in Mr. and Mrs.),take it as a surname
                elif i==len(words)-2:
                    if words[i+1][0].isupper():
                        name=words[i+1]
                #If pattern is present anywhere else consider the next word as a surname if it starts with a capital letter
                elif i<=len(words)-3:
                    if words[i+1][0].isupper():
                        name=words[i+1]
                    #To match surnames like 'de Bourgh'(which do not start with a capital letter)
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

file.close()

# Compute the histogram of Surnames
for word in list1:
    if word in check:
        list2[check.index(word)][1]+=1
    else:
        list2.append([word,1])
        check.append(word)
        count=count+1

# Sort in decreasing order of occurance
# D=sorted(list2, key=itemgetter(1),reverse=True)

# Sort alphabetically
D=sorted(list2, key=itemgetter(0))

# Plot the histogram
fig2 = plt.figure()
ax2 = fig2.add_axes([0.15, 0.25, 0.7, 0.6])
plt.bar(range(len(D)), [x[1] for x in D])
plt.xticks(range(len(D)), [x[0] for x in D],rotation='vertical')
plt.tick_params(axis='x',which='both',bottom='off',top='off')
plt.gca().yaxis.grid(True)
plt.ylabel('Count')
plt.xlim([0,len(D)])
plt.ylim([0,320])
plt.show()

# Print frequency table
print tabulate(D)
print 'There are %d surnames'%count






