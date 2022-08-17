#!/usr/bin/env python -O
# viterbi.py: simple Viterbi decoding, with protections against underflow
# Steven Bedrick <bedricks@ohsu.edu> and Kyle Gorman <gormanky@ohsu.edu>


from bitweight import BitWeight
from numpy import array, int8, ones, zeros,dtype,arange,argmax


def viterbi(observations, states, transitions, emissions):

    prob_mat=zeros((len(state_lookup),len(emis_lookup)),dtype=BitWeight)
    lookup=zeros((len(state_lookup),len(emis_lookup)),dtype=BitWeight)
    best_path=zeros(len(emis_lookup),dtype=BitWeight)

    # Calculate values of first column of probability matrix
    prob_mat[:,0]=transitions[0,:]*emissions[:,0]
    
    # Populate the rest of the prob_mat and the look up table
    for i in arange(1,len(emis_lookup)):
        for j in arange(len(state_lookup)):
            temp=prob_mat[:,i-1]*transitions[1:,j]
            lookup[j,i]=argmax(temp)
            prob_mat[j,i]=max(temp)*emissions[j,i]

    # Final state
    final_state=argmax(prob_mat[:,-1])
    best_path[-1]=final_state

    # Get the best path
    for i in arange(len(emis_lookup)-1,0,-1):
        best_path[i-1]=lookup[best_path[i],i]
    best_path=best_path.astype(int)
    return best_path+1



if __name__ == "__main__":
    
    states = ['VB', 'TO', 'NN', 'PPSS']
    observations = ['I', 'want', 'to', 'race']
    print 'Input :'
    print observations
    state_lookup = {1: 'VB', 2: 'TO', 3: 'NN', 4: 'PPSS'}
    emis_lookup = {1: 'I', 2: 'want', 3: 'to', 4: 'race'}
    
    # note that row 0 of transitions represents the starting transitions
    # (i.e., P("VB" | "start"), etc.)
    
    transitions = array([[BitWeight(0.19),    BitWeight(0.0043),
                          BitWeight(0.41),    BitWeight(0.067)  ],
                         [BitWeight(0.0038),  BitWeight(0.035),
                          BitWeight(0.047),   BitWeight(0.0070)],
                         [BitWeight(0.83),    BitWeight(0.),
                          BitWeight(0.00047), BitWeight(0.)    ],
                         [BitWeight(0.0040),  BitWeight(0.016),
                          BitWeight(0.087),   BitWeight(0.0045)],
                         [BitWeight(0.23),    BitWeight(0.0079),
                          BitWeight(0.0012),  BitWeight(0.00014)]])
                          
    emissions = array([[BitWeight(0.),   BitWeight(0.0093),
                        BitWeight(0.),   BitWeight(0.00012)],
                       [BitWeight(0.),   BitWeight(0.),
                        BitWeight(0.99), BitWeight(0.)    ],
                       [BitWeight(0.),   BitWeight(0.000054),
                        BitWeight(0.),   BitWeight(0.00057)],
                       [BitWeight(0.37), BitWeight(0.),
                        BitWeight(0.),   BitWeight(0.)     ]])
                         
    sequence = viterbi(observations, states, transitions, emissions)
    print 'Viterbi output:'
    print ' '.join(state_lookup[i] for i in sequence)
