#!/usr/bin/python

from __future__ import division
import pickle
from hmmlearn import hmm
import numpy as np

# Loading data
f=open('data.pkl.txt', 'r')
observation=pickle.load(f)
states=pickle.load(f)
seg_clus=pickle.load(f)
f.close()

# Training HMM
model2 = hmm.GMMHMM(n_components=5,n_mix=16,n_iter=10, covariance_type='diag')
model2.fit([observation])

# Predicting output states
Z2 = model2.predict(observation)

# Calculating accuracy by changing state assignments
# in gold-standard labels in a cyclic fashion
num=[0,1,2,3,4]
final=[]
for i in xrange(len(num)):
    for j in xrange(len(states)):
        n=num.index(states[j])
        states[j]=num[(n + 1) % len(num)]
    conf_mat=np.zeros((5,5))
    for a,b in zip(Z2, states):
        conf_mat[a][b] += 1
    accuracy=np.trace(conf_mat)/np.sum(conf_mat)
    final.append(accuracy)
#    print "Accuracy = %f" %accuracy
#    print conf_mat.astype(int)
print "Accuracy in all cases:"
print final
print "Overall accuracy: %s"%(max(final))

