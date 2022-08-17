#!/usr/bin/python

import re
re.UNICODE

a='^\s*[A-Z]+\s*$'

file=open('pg1041.txt','r')
count=0

for line in file:
    for match in re.finditer(a,line):
        #s=match.start()
        #e=match.end()
        #print line[s:e]
        count=count+1

print 'There are %d Sonets'%count
