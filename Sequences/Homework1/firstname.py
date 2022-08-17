#!/usr/bin/python

import re

re.UNICODE

# Regular expression to match Mr., Mrs., Miss, Lady and Colonel
a='[MLC][r*ia*o][s*d*\.?l]s*\.*y?o?n?e?l?'
# Regular expression to match any two consecutive words with first letters as a capital letters
b='[A-Z][a-z]+\s[A-Z][a-z]+\s'

file=open('pg1342.txt','r')

# Output from Surname_histogram (list of surnames)
check=['Anne', 'Annesley', 'Bennet', 'Bingley', 'Bennets', 'Collins', 'Catherine', 'Darcy', 'Denny', 'Eliza', 'Elizabeth', 'Fitzwilliam', 'Forster', 'F', 'Grantley', 'Gardiner', 'Hurst', 'Hill', 'Jones', 'Jane', 'Jenkinson', 'King', 'Long', 'Lucas', 'Lucases', 'Lydia', 'Lizzy', 'Morris', 'Metcalf', 'Nicholls', 'Phillips', 'Phillip', 'Pope', 'Robinson', 'Reynolds', 'Stone', 'Watson', 'Wickham', 'Webbs', 'Younge', 'de Bourgh']

count=0
first_name=[]

for line in file:
    words=line.split()
    for i,w in enumerate(words):
        # Check of surnames in line
        if any(x==w for x in check):
            # Check if there are two consecutive Title words
            for match in re.findall(b,line):
                # Check if the first Title word matches Mr., Mrs., Miss, Lady or Colonel
                if not re.match(a,words[i-1]):
                    if words[i-1][0].isupper():
                        # Word should not be followed by a period
                        if not words[i-2][-1]=='.':
                            # Word should not at the beggining of the line
                            if not i-1<=0:
                                if not words[i-1] in first_name:
                                    first_name.append(words[i-1])
                                    print words[i-1:i+1]
                                    count+=1


file.close()

print first_name
print 'Found %d First names'%count