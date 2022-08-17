
A = {}
A[(1,1)]=(2,"A")
print A[(1,1)][0]
print range(-1,4)


def version3_boon(a1,a2,x,y,seq,score):
    
    n = len(a1)
    m = len(a2)
    
    cur_score = 1
    if x == n-1 and y == m-1:
        print '%-4i%-s'  %(score,seq)
        return (seq,0)
    
    
    if x == n-1:
        (cseq,cscor) = version3(a1,a2,x,y+1,seq+'|',score+1)
        return (cseq,cur_score+cscor)
    
    if y == m-1:
        (cseq,cscor) = version3(a1,a2,x+1,y,seq+'-',score+1)
        return (cseq,cur_score+cscor)
    
    scores = [0,0,0]
    seqs = ["", "", ""]

    seqs[0],scores[0] = version3(a1,a2,x+1,y,seq+'-',score+1)
    scores[0] += cur_score
    
    seqs[1],scores[1] = version3(a1,a2,x,y+1,seq+'|',score+1)
    scores[1] += cur_score
    
    if a1[x+1] != a2[y+1]:
        seqs[2],scores[2] = version3(a1,a2,x+1,y+1,seq+'\\',score+1)
        scores[2] += cur_score
    else:
        seqs[2],scores[2] = version3(a1,a2,x+1,y+1,seq+'\\',score)
    
    mn,idx = min( (scores[i],i) for i in xrange(len(scores)) )
    #    print '%-4i%-s'  %(mn, seqs[idx])
    return (seqs[idx], mn)

def version2(x_array,y_array,x,y,align,score):
    if x+1 >= len(x_array) and y+1 >= len(y_array):
        print '%-4i%-s' % (score,align)
        return
    if x+1 < len(x_array):
        version2(x_array,y_array,x+1,y,align+"-",score+1)
    if y+1 < len(y_array):
        version2(x_array,y_array,x,y+1,align+"|",score+1)
    if x+1 < len(x_array) and y+1 < len(y_array):
        if x_array[x+1] == y_array[y+1]:
            version2(x_array,y_array,x+1,y+1,align+"\\",score)
        else:
            version2(x_array,y_array,x+1,y+1,align+"\\",score+1)


def version31(a1,a2,x,y,seq,score):
    
    n = len(a1)
    m = len(a2)
    
    
    if x == n-1 and y == m-1:
        return (seq,0)
    
    if x == n-1:
        (cseq,cscor) = version3(a1,a2,x,y+1,seq+'|',score+1)
        return (cseq,cscor+1)
    
    if y == m-1:
        (cseq,cscor) = version3(a1,a2,x+1,y,seq+'-',score+1)
        return (cseq,cscor+1)
    
    scores = [0,0,0]
    seqs = ["", "", ""]

if a1[x+1] == a2[y+1]:
    (cseq,cscor) = version3(a1,a2,x+1,y+1,seq+'\\',score)
        return (cseq,cscor)
    else:
        seqs[0],scores[0] = version3(a1,a2,x+1,y,seq+'-',score+1)
        seqs[1],scores[1] = version3(a1,a2,x,y+1,seq+'|',score+1)
        seqs[2],scores[2] = version3(a1,a2,x+1,y+1,seq+'\\',score+1)
        
        mn,idx = min( (scores[i],i) for i in xrange(len(scores)) )
        return (seqs[idx], mn+1)



def version41(a1,a2,x,y,seq,score):
    
    n = len(a1)
    m = len(a2)
    
    
    ### Initializing cache
    if x == -1 and y == -1:
        for i in range(-1,n):
            for j in range(-1,m):
                cache[(i,j)] = ("",-1)

### Checking if value updated in cache
if cache[(x,y)][1] != -1:
    sequence = cache[(x,y)][0]
        sc = cache[(x,y)][1]
        return (seq + sequence,sc)
    
    if x == n-1 and y == m-1:
        cache[(x,y)] = ("",0)
        return ("",0)

if x == n-1:
    (cseq,cscor) = version4(a1,a2,x,y+1,seq+'|',score+1)
        cache[(x,y)] = ('|'+cache[(x,y+1)][0],cscor+1)
        print(x,y,cache[(x,y)])
        return (cseq,cscor+1)
    
    if y == m-1:
        (cseq,cscor) = version4(a1,a2,x+1,y,seq+'-',score+1)
        cache[(x,y)] = ('-'+cache[(x+1,y)][0],cscor+1)
        print(x,y,cache[(x,y)])
        return (cseq,cscor+1)

scores = [0,0,0]
    seqs = ["", "", ""]
    seq11 = ['-','|','\\']
    x1 = [x+1,x,x+1]
    y1 = [y,y+1,y+1]
    
    if a1[x+1] == a2[y+1]:
        (cseq,cscor) = version4(a1,a2,x+1,y+1,seq+'\\',score)
        cache[(x,y)] = ('\\'+cache[(x+1,y+1)][0],cscor)
        print(x,y,cache[(x,y)])
        return (cseq,cscor)
    else:
        seqs[0],scores[0] = version4(a1,a2,x+1,y,seq+'-',score+1)
        seqs[1],scores[1] = version4(a1,a2,x,y+1,seq+'|',score+1)
        seqs[2],scores[2] = version4(a1,a2,x+1,y+1,seq+'\\',score+1)
        
        mn,idx = min( (scores[i],i) for i in xrange(len(scores)) )
        cache[(x,y)] = (seq11[idx]+cache[(x1[idx],y1[idx])][0], mn+1)
        print(x,y,cache[(x,y)])
        return (seqs[idx], mn+1)








