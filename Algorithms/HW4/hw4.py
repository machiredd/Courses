from timeit import default_timer as timer
import random

cache = {}

def version1(a1,a2,x,y,seq):

    n = len(a1)
    m = len(a2)

    if x == n-1 and y == m-1:
        print(seq)
        return

    if x == n-1:
        version1(a1,a2,x,y+1,seq+'|')
        return

    if y == m-1:
        version1(a1,a2,x+1,y,seq+'-')
        return

    version1(a1,a2,x+1,y,seq+'-')
    version1(a1,a2,x,y+1,seq+'|')
    version1(a1,a2,x+1,y+1,seq+'\\')


def time_ver1():
    a = range(10)
    b = range(10)
    time = []

    for i in range(10):
        start = timer()
        version1(a[:i],b[:i],-1,-1,"")
        end = timer()
        print '%-12i%-f' % (i+1, end-start)

def version2(a1,a2,x,y,seq,score):
    
    n = len(a1)
    m = len(a2)
    if x == n-1 and y == m-1:
        print '%-4i%-s' % (score,seq)
        return
    
    if x == n-1:
        version2(a1,a2,x,y+1,seq+'|',score+1)
        return
    
    if y == m-1:
        version2(a1,a2,x+1,y,seq+'-',score+1)
        return
    
    version2(a1,a2,x+1,y,seq+'-',score+1)
    version2(a1,a2,x,y+1,seq+'|',score+1)
    if a1[x+1] == a2[y+1]:
        version2(a1,a2,x+1,y+1,seq+'\\',score)
    else:
        version2(a1,a2,x+1,y+1,seq+'\\',score+1)



def version3(a1,a2,x,y,seq,score):
    
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

    scores = [float("inf"),float("inf"),float("inf")]
    seqs = ["", "", ""]
    seq11 = ['-','|','\\']
    
    seqs[0],scores[0] = version3(a1,a2,x+1,y,seq+'-',score+1)
    scores[0] += 1
    seqs[1],scores[1] = version3(a1,a2,x,y+1,seq+'|',score+1)
    scores[1] += 1
    if a1[x+1] != a2[y+1]:
        seqs[2],scores[2] = version3(a1,a2,x+1,y+1,seq+'\\',score+1)
        scores[2] += 1
    else:
        seqs[2],scores[2] = version3(a1,a2,x+1,y+1,seq+'\\',score)
        
    mn,idx = min( (scores[i],i) for i in xrange(len(scores)) )

    return (seqs[idx], mn)


def version4(a1,a2,x,y,seq,score):
    
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
        return (cseq,cscor+1)
    
    if y == m-1:
        (cseq,cscor) = version4(a1,a2,x+1,y,seq+'-',score+1)
        cache[(x,y)] = ('-'+cache[(x+1,y)][0],cscor+1)
        return (cseq,cscor+1)

    scores = [float("inf"),float("inf"),float("inf")]
    seqs = ["", "", ""]
    seq11 = ['-','|','\\']
    x1 = [x+1,x,x+1]
    y1 = [y,y+1,y+1]

    seqs[0],scores[0] = version4(a1,a2,x+1,y,seq+'-',score+1)
    scores[0] += 1
    seqs[1],scores[1] = version4(a1,a2,x,y+1,seq+'|',score+1)
    scores[1] += 1
    if a1[x+1] != a2[y+1]:
        seqs[2],scores[2] = version4(a1,a2,x+1,y+1,seq+'\\',score+1)
        scores[2] += 1
    else:
        seqs[2],scores[2] = version4(a1,a2,x+1,y+1,seq+'\\',score)
        
    mn,idx = min( (scores[i],i) for i in xrange(len(scores)) )
    cache[(x,y)] = (seq11[idx]+cache[(x1[idx],y1[idx])][0], mn)
    return (seqs[idx], mn)



def time_ver4():
    
    a = list(range(1, 500))
    b = list(range(1, 500))
    random.shuffle(a)
    random.shuffle(b)
    time = []
    d = range(10,501,10)
    for i in d:
        start = timer()
        seq,score = version4(a[:i],b[:i],-1,-1,"",float("inf"))
        end = timer()
        print '%-12i%-f' % (i, end-start)


if __name__ == "__main__":
    
    print('Answer version 1:')
    version1(["A","B","C","C","D"],["A","E","B","F","C","D"],-1,-1,"")
    print('Answer version 2:')
    version2(["A","E","B","F","C","D"],["A","B","C","C","D"],-1,-1,"",0)
    print('Answer version 3:')
    seq,score = version3(["A","B","C","C","D"],["A","E","B","F","C","D"],-1,-1,"",float("inf"))
    print '%-4i%-s' % (score,seq)
    print('Answer version 4:')
    seq,score = version4(["A","B","C","C","D"],["A","E","B","F","C","D"],-1,-1,"",float("inf"))
    print '%-4i%-s' % (score,seq)

#
#    time_ver1()
#    time_ver4()


