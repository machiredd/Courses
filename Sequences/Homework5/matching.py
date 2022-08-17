    import sys
import datetime as dt
import argparse
from collections import defaultdict
import operator
from itertools import groupby


"""
These functions modified and ported from C code by Brian Roark. 
"""
class PatternPreprocessor:
    #######################
    # Pre-processing utility functions
    #######################

    def __init__(self, patt, text):
        self.pattern = patt
        self.arr_len = len(patt) + 1 # length to use for vectors
        self.Z = [0] * self.arr_len # Gusfield Z-values
        self.sp = [0] * self.arr_len # KMP sp' suffix length values
        self.F = [0] * self.arr_len # KMP failure function values
        self.badc = self.get_bad_char(self.pattern) # weak bad character values for Boyer-Moore
        self.L_prime = [0] * self.arr_len # strong "L" values for Boyer-Moore (L'), Gusfield theorem 2.2.2, p. 21
        self.l_prime = [0] * self.arr_len # l-values for Boyer-Moore - Gusfield theorem 2.2.4, p. 21

        self.calc_good_suffix()        
        self.Z, self.sp, self.F = self.calc_z_vals_and_failure_func(self.pattern)
    
        self.text_full = text
        self.freq = self.get_freq(self.text_full) # Frequency of alphabet from haystack for Optimal mismatch
        self.pat_opt_mis = self.get_sorted_pattern_OM(self.pattern,self.freq) # Sorted pattern for Opt. Mismatch
        self.pat_max_shift = self.get_max_shift(self.pattern) # Sorted pattern for Maximal Shift
        self.bad_c = self.get_new_bad_char(self.pattern) # Bad character values for Optimal mismatch & max. shift
        self.adaptedGs_opti = self.get_adapted_good_suffix(self.pattern,self.pat_opt_mis) # Good suffix for OM
        self.adaptedGs_max = self.get_adapted_good_suffix(self.pattern,self.pat_max_shift) # Good suffix for MS
    

    """
    Computes frequency of characters in the alphabet from the text(haystack) 
    Used in Optimal Mismatch algorithm to sort the pattern
    """
    def get_freq(self, text):
        freq = defaultdict(int)
        for idx, c in enumerate(text):
            freq[c] +=1
        return freq
    
    """
    Gives the sorted pattern for Optimal Mismatch Algorithm
    Sort the pattern from least frequent to most frequent characters as observed in text 
    """
    def get_sorted_pattern_OM(self, pstr, freq):
        groups=[]
        for k,g in groupby((sorted(enumerate(pstr), key=lambda x: freq[x[1]])),lambda x:x[1]):
            groups.append((sorted(list(g),key= lambda x:x[0], reverse=True)))
        pat = [item for sublist in groups for item in sublist]
        return pat
    
    """
    Gives the sorted pattern for Maximal Shift Algorithm
    
    First, for each character in the string the minimun shift to find the next possible match 
    or safely pass the pattern without missing a match is calculated. Then the characters in 
    the string are rearranged such that the ones which lead to larger shifts are placed first 
    and ones leading to shorter shift follow them
    """
    def get_max_shift(self, pstr):
        i = 0
        minShift = [0] * (self.arr_len-1)
        while i < self.arr_len-1:
            j = i-1
            while j >= 0:
                if pstr[i] == pstr[j]:
                    break;
                j -= 1
            minShift[i]=i-j # Minimum shift of the pattern to find a match or pass without missing a match
            i += 1
        new = sorted(zip(enumerate(pstr),minShift),key=lambda x:x[1])
        fin = [i[0] for i in new]
        pat = list(reversed(fin))
        return pat

    """
    Computes values for bad-character rule for Optimal Mismatch and Maximal Shift algorithm
    
    It is given as [len(pattern)- index of rightmost occurance of the character in the pattern]
    If the character is not in the pattern the pattern is shifted by len(pattern)+1, as the values of
    bad-character rule are calculated w.r.t character appearing in T[k+m] position in the text.
    """
    def get_new_bad_char(self, patt):
        bad_c = defaultdict(lambda: self.arr_len)
        for idx, c in enumerate(patt):
            bad_c[c] = (self.arr_len-1)-idx
        return bad_c
    
    """
    This function gives the value of the next matching shift for the first ploc pat elements
    
    If the mismatch is occuring at ploc, we need to find if there is a matching
    occurance of pat[0...ploc-1] in pstr, if so return the shift needed to goto that position
    else shift by len(pstr)-1, as there is no matching pattern in pstr
    
    In a way, similar to value L(i) (valve calculated here is like len(patt)-L(i)) in Boyer-Moore algorithm
    This part is largely inspired from the C code give in "http://www-igm.univ-mlv.fr/~lecroq/string/node28.html#SECTION00280"
    
    pstr = Original pattern
    pat = Reordered pattern
    pat[i][0] = location of character in the original pattern
    pat[i][1] = character in the redordered pattern at position i
    ploc = Location in the pstr being considered (No. of characters observed in pat)
    """
    def matchShift(self,pstr, ploc, lshift, pat):
        for lshift in range(lshift,self.arr_len-1):
            i = ploc-1
            while (i >= 0): # while we are not past the left end of the pattern
                # All preceeding characters seen till now in pat should match
                j = (pat[i][0]-lshift) # location in pstr after the shift
                if (j < 0): # if the character goes beyond the left end of pattern
                    i -= 1 # consider the previous character in pat
                    continue
                if (pat[i][1] != pstr[j]): # if values in pstr and pat don't match increase the shift
                    break
                i -= 1
            if (i < 0): # All previous characters have been checked and they match
                break
        return lshift
            
    """
    Computes values of good-suffix for the re-ordered pattern, used in Maximal Shift and Optimal Mismatch algo.
    
    pstr = Original pattern
    pat = Reordered pattern
    pat[i][0] = location of character in the original pattern
    pat[i][1] = character in the redordered pattern at position i
    ploc = Location in the pstr being considered
    """
    def get_adapted_good_suffix(self, pstr, pat):
        adaptedGs=[0] * self.arr_len
        adaptedGs[0]=1 # First character in pattern, no preceeding characters to compare, so max shift 1
        lshift=1
        for ploc in range(1,self.arr_len):
            # For every location calculate min possible shift to find a match
            adaptedGs[ploc] = self.matchShift(pstr, ploc, lshift, pat)
        
        # Modify the shift value by adding the condition that the current character should not match
        for ploc in xrange(self.arr_len-1):
            lshift=adaptedGs[ploc] # Get the initial matching shift
            while (lshift < self.arr_len-1):
                i = pat[ploc][0] - lshift # position after the min shift
                if (i < 0 or pat[ploc][1] != pstr[i]): # if there is a mismatch this is the min shift
                    break
                lshift += 1 # else keep scanning to get the next possible match
                lshift = self.matchShift(pstr, ploc, lshift, pat)
            adaptedGs[ploc] = lshift
        return adaptedGs
    
    
    """
    Utility function for getting the longest matching prefix of two string/offsets
    """
    def matchlen(self, s1, pos1, s2, pos2):
        to_ret = 0
        l1 = len(s1)
        l2 = len(s2)
    
        idx1 = pos1
        idx2 = pos2
    
        while idx1 < l1 and idx2 < l2 and s1[idx1] == s2[idx2]:
            to_ret += 1
            idx1 += 1
            idx2 += 1
        
        return to_ret
    
    """
    Function to compute Z values, failure function values, and sp' suffix values

    Modified from C code by Brian Roark; as a result, it's not particularly Pythonic. :-/
    
    """
    def calc_z_vals_and_failure_func(self, str_to_use):
        r = 0
        l = 0
        updater_l = False
        patt_len = len(str_to_use)
        vec_len_to_use = patt_len + 1
        
        Z_to_ret = [0] * vec_len_to_use
        sp_to_ret = [0] * vec_len_to_use
        F_to_ret = [0] * vec_len_to_use
        
        i_counter = 0 # just to keep track of 
        for i in range(patt_len):
            i_counter = i
            F_to_ret[i] = sp_to_ret[i - 1]
            upater_l = False # reset if needed from prev. iteration
            if i > r: # outside of a z-box
                Z_to_ret[i] = self.matchlen(str_to_use, i, str_to_use, 0)
                if Z_to_ret[i] > 0:
                    updater_l = True
            else: # inside a z-box
                if Z_to_ret[i - l] < r - i + 1:
                    Z_to_ret[i] = Z_to_ret[i - l]
                else:
                    Z_to_ret[i] = r - i + 1;
                    Z_to_ret[i] += self.matchlen(str_to_use, r + 1, str_to_use, r - i + 2)
                    updater_l = True
            
            if updater_l:
                r = i + Z_to_ret[i] - 1
                l = i
                if sp_to_ret[r] == 0:
                    sp_to_ret[r] = Z_to_ret[i]
        F_to_ret[-1] = sp_to_ret[-2] # clean up
        
        return (Z_to_ret, sp_to_ret, F_to_ret)
        
    
    
    """
    Calculate Boyer-Moore "Good Suffix" rule
    """

    def calc_good_suffix(self):
        patt_len = self.arr_len - 1 # the actual pattern length
        k = 0
        last = 0

        reversed_pattern = self.pattern[::-1]
        rev_z, rev_sp, rev_f = self.calc_z_vals_and_failure_func(reversed_pattern)
        
        # compute L'
        for i in range(1, patt_len - 1): # set strong good suffix values L' from the reversed version of the pattern
            k = patt_len - rev_z[patt_len - i - 1];
            self.L_prime[k] = i
        last = 0
        
        # now commpute l', also using the Z-values of the reversed pattern
        for i in range(patt_len - 1, -1, -1): # go all the way down to zero
            k = patt_len - i - 1
            if rev_z[patt_len - k - 1] == k + 1:
                self.l_prime[i] = k + 1
                last = k + 1
            else:
                self.l_prime[i] = last


    """
    Computes the values needed for the weak "Bad Character" rule for Boyer-Moore

    From Gusfield section 2.2.2: For each character x in the alphabet, let R(x) be the position of right-most occurrence of character x in P. R(x) is defined to be zero if x does not occur in P.

    """
    def get_bad_char(self, patt):
        bc = defaultdict(int)    
        for idx, c in enumerate(patt):
            bc[c] = idx
        return bc
    

#######################
# Matching algorithms
#######################

"""
implements the naive quadratic-time exact matching algorithm
arguments: 
    patt: the pattern ("needle") to search for
    preproc: a precomputed instance of the PatternPreprocessor class for patt, NOT USED for the naive search
    txt: the text in which to search for patt (the "haystack")
returns: a list containing the offsets in txt at which occurrences of patt were found
"""
def naive_match(patt, preproc, txt):
    matches = [] # will store the indices of matches

    patt_len = len(patt) # save these ahead of time, since we'll be using them a lot
    txt_len = len(txt)
    last = txt_len - patt_len + 1 # the last position in txt at which patt could occurr

    # setup variables for loops
    p_idx = -1 # offset within the pattern for a current possible match
    t_idx = -1 # our offset within txt for the current possible match
    outer_t_idx = -1 # our offset within txt for the outer loop (how far are we in the string?)
    
    # listify for faster indexing - grr, Python...
    t_chars = list(txt) #array(list(txt))
    p_chars = list(patt) #array(list(patt))
    
    # move one character at a time through our string...
    while outer_t_idx < last:
        outer_t_idx += 1
        t_idx = outer_t_idx
        p_idx = 0
        # try to start a new match at outer_t_idx; continue until we run out of pattern, text, or until we stop seeing a match
        while p_idx < patt_len and t_idx < txt_len and p_chars[p_idx] == t_chars[t_idx]:
            t_idx += 1
            p_idx += 1
        if p_idx >= patt_len: # we must have gotten all the way through the pattern- i.e., the previous loop must have terminated because p_idx was > patt_len, not because the match ended, etc.
            matches.append(outer_t_idx)
    return matches
    
"""
implements the Knuth-Morris-Pratt matching algorithm
arguments: 
    patt: the pattern ("needle") to search for
    preproc: a precomputed instance of the PatternPreprocessor class for patt
    txt: the text in which to search for patt (the "haystack")
returns: a list containing the offsets in txt at which occurrences of patt were found
"""
def knuth_morris_pratt(patt, preproc, txt):
    matches = [] # will store the indices of matches
    
    patt_len = len(patt) # save these ahead of time, since we'll be using them a lot
    txt_len = len(txt)
    last = txt_len - patt_len + 1 # the last position in txt at which patt could occurr
    
    # listify for faster indexing - grr, Python...
    t_chars = list(txt) #array(list(txt))
    p_chars = list(patt) #array(list(patt))
    
    outer_t_idx=0 # position in the haystack
    while outer_t_idx < last:
        t_idx = outer_t_idx
        p_idx = 0
        # try to start a new match at outer_t_idx; continue until we run out of pattern, text, or until we stop seeing a match
        while p_idx < patt_len and t_idx < txt_len and p_chars[p_idx] == t_chars[t_idx]:
            t_idx += 1
            p_idx += 1
        if p_idx >= patt_len:
            matches.append(outer_t_idx)
            outer_t_idx += (patt_len-preproc.sp[patt_len-1]) # match found, shift by n-sp[n]
        elif p_idx > 0 and preproc.F[p_idx] > 0:
            outer_t_idx += preproc.F[p_idx] # Mismatch, shift by the failure function of the mismatch position
        else:
            outer_t_idx += 1 # Mismatch in the first term
    return matches


"""
implements the Boyer-Moore matching algorithm
arguments: 
    patt: the pattern ("needle") to search for
    preproc: a precomputed instance of the PatternPreprocessor class for patt
    txt: the text in which to search for patt (the "haystack")
returns: a list containing the offsets in txt at which occurrences of patt were found
"""
def boyer_moore(patt, preproc, txt):
    matches = [] # will store the indices of matches
    
    patt_len = len(patt) # save these ahead of time, since we'll be using them a lot
    txt_len = len(txt)
    last = txt_len - patt_len + 1 # the last position in txt at which patt could occurr
    
    # listify for faster indexing - grr, Python...
    t_chars = list(txt) #array(list(txt))
    p_chars = list(patt) #array(list(patt))

    outer_t_idx=0 # position in haystack
    while outer_t_idx < last:
        t_idx = outer_t_idx
        p_idx = patt_len-1 # Compare from right end of pattern
        # try to start a new match at outer_t_idx; continue until we run out of pattern, text, or until we stop seeing a match
        while p_idx > -1 and p_chars[p_idx] == t_chars[p_idx+t_idx]:
            p_idx -= 1
        if p_idx == -1: # we must have gotten all the way through the pattern
            matches.append(outer_t_idx)
            outer_t_idx += patt_len-preproc.l_prime[1] # Match found, increment by l' of second character in patt
        # Mismatch somewhere between the pattern
        elif p_idx > -1 and p_idx < patt_len-1:
            if preproc.L_prime[p_idx+1] > 0: # if there is a matching suffix shift by max(bad_char,L')
                outer_t_idx += max(p_idx-preproc.badc[t_chars[p_idx+t_idx]],patt_len-preproc.L_prime[p_idx+1]-1)
            else: # else shift by max (bad_char,l')
                outer_t_idx += max(p_idx-preproc.badc[t_chars[p_idx+t_idx]],patt_len-preproc.l_prime[p_idx+1]-1)
        # Mismatch at the rightmost(first) place
        elif p_idx > -1 and p_idx == patt_len-1:
            outer_t_idx += max(1,p_idx-preproc.badc[t_chars[p_idx+t_idx]])
    return matches

"""
implements the Optimal Mismatch algorithm
arguments:
    patt: the pattern ("needle") to search for
    preproc: a precomputed instance of the PatternPreprocessor class for patt
    txt: the text in which to search for patt (the "haystack")
returns: a list containing the offsets in txt at which occurrences of patt were found
"""
def optimal_mismatch(patt, preproc, txt):
    matches = [] # will store the indices of matches
    
    patt_len = len(patt) # save these ahead of time, since we'll be using them a lot
    txt_len = len(txt)
    last = txt_len - patt_len + 1 # the last position in txt at which patt could occurr
    
    # listify for faster indexing - grr, Python...
    t_chars = list(txt) #array(list(txt))
    p_chars = list(patt) #array(list(patt))

    outer_t_idx=0 # Position in haystack
    while outer_t_idx < last:
        t_idx = outer_t_idx
        p_idx = 0
        # try to start a new match at outer_t_idx following the order in the re-ordered pattern
        while p_idx < patt_len and t_idx < txt_len and preproc.pat_opt_mis[p_idx][1] == t_chars[t_idx+(preproc.pat_opt_mis[p_idx][0])]:
            p_idx += 1
        if p_idx >= patt_len: # we must have gotten all the way through the pattern
            matches.append(outer_t_idx)
        #shift by max(bad_char,good_suffix)
        if t_idx+patt_len < txt_len:
            outer_t_idx += max(preproc.adaptedGs_opti[p_idx],preproc.bad_c[t_chars[t_idx+patt_len]])
        else:
            outer_t_idx += preproc.adaptedGs_opti[p_idx]
    return matches


"""
implements the Maximal Shift algorithm
arguments:
    patt: the pattern ("needle") to search for
    preproc: a precomputed instance of the PatternPreprocessor class for patt
    txt: the text in which to search for patt (the "haystack")
returns: a list containing the offsets in txt at which occurrences of patt were found
"""
def maximal_shift(patt, preproc, txt):
    matches = [] # will store the indices of matches
    
    patt_len = len(patt) # save these ahead of time, since we'll be using them a lot
    txt_len = len(txt)
    last = txt_len - patt_len + 1 # the last position in txt at which patt could occurr

    # listify for faster indexing - grr, Python...
    t_chars = list(txt) #array(list(txt))
    p_chars = list(patt) #array(list(patt))
    
    outer_t_idx=0 # Position in haystack
    while outer_t_idx < last:
        t_idx = outer_t_idx
        p_idx = 0
        # try to start a new match at outer_t_idx following the order in the re-ordered pattern
        while p_idx < patt_len and t_idx < txt_len and preproc.pat_max_shift[p_idx][1] == t_chars[t_idx+(preproc.pat_max_shift[p_idx][0])]:
            p_idx += 1
        if p_idx >= patt_len: # we must have gotten all the way through the pattern
            matches.append(outer_t_idx)
        #shift by max(bad_char,good_suffix)
        if t_idx+patt_len < txt_len:
            outer_t_idx += max(preproc.adaptedGs_max[p_idx],preproc.bad_c[t_chars[t_idx+patt_len]])
        else:
            outer_t_idx += preproc.adaptedGs_max[p_idx]
    return matches


#######################
# I/O and main program logic
#######################

parser = argparse.ArgumentParser()
parser.add_argument("patt_fname", help="a text file containing patterns to search for, one pattern per line")
parser.add_argument("text_fname", help="the text file in which to search")
args = parser.parse_args()

patterns_fname = args.patt_fname
in_fname = args.text_fname

needles = [l.strip() for l in open(patterns_fname).readlines()]

haystack = open(in_fname).read() # the text to search

for p in needles:
    print p
    start_preproc_time = dt.datetime.now()
    pre_processed_vals = PatternPreprocessor(p,haystack) # see definition above; can ask it for things like Z-values, etc.
    end_preproc_time = dt.datetime.now()
    elapsed_preproc_time = end_preproc_time - start_preproc_time
    print "\tPre-processing time:",elapsed_preproc_time.total_seconds(),"seconds."
 
    for search_algorithm in [naive_match, knuth_morris_pratt, boyer_moore, optimal_mismatch, maximal_shift]:
        time = []
        start_time = dt.datetime.now()
        matches = search_algorithm(p, pre_processed_vals, haystack)
        end_time = dt.datetime.now()
        elapsed = (end_time - start_time)
        print "\t", search_algorithm.__name__, "\t", elapsed.total_seconds(), "seconds\t", len(matches), "matches"
