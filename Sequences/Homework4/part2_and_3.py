#!/usr/bin/python

from hmmlearn import hmm
import numpy as np
from itertools import groupby
import pickle
import operator
import matplotlib.pyplot as plt

f=open('data.pkl.txt', 'r')
observation=pickle.load(f)
states=pickle.load(f)
seg_clus=pickle.load(f)
f.close()

data=[]
gmm_input=[]

# Splitting observations according to labels given in gold-standard
for k,g in groupby(sorted(enumerate(states),key=operator.itemgetter(1)), lambda x: x[1]):
    data.append(list(observation[i] for i in (list((x[0] for x in list(g))))))

# Training GMM and getting the mean and covariance
for i in xrange(len(data)):
    g = hmm.GMM(n_components=16,covariance_type='diag',n_iter=10)
    g.fit(data[i])
    gmm_input.append(g)

# Define the start probabilities and transition matrix
n_comp=5
start_prob = np.tile(1.0/n_comp, n_comp)
trans_mat=np.zeros((n_comp,n_comp))
for i in xrange(len(states)-1):
    trans_mat[states[i]][states[i+1]] +=1
trans_mat /=  trans_mat.sum(axis=1)[:,np.newaxis]

# Substitute GMMs in HMM
model=hmm.GMMHMM(n_components=5,n_mix=16,n_iter=10, covariance_type='diag',
                 startprob=start_prob,transmat=trans_mat,gmms=gmm_input)

# Predict the states based on model
vit_op = model.predict(observation)

# Calculate confusion matrix and accuracy
conf_mat=np.zeros((n_comp,n_comp))
for a,b in zip(vit_op,states):
    conf_mat[a][b] += 1
accuracy=np.trace(conf_mat)/np.sum(conf_mat)
print "Accuracy = %f" %accuracy
#print conf_mat
print conf_mat.astype(int)

# Plot posterior probability
log,post=model.score_samples(observation[6000:7000])

plot1=plt.plot(list(x[0] for x in post),label='0')
plot2=plt.plot(list(x[1] for x in post),label='1')
plot3=plt.plot(list(x[2] for x in post),label='2')
plot4=plt.plot(list(x[3] for x in post),label='3')
plot5=plt.plot(list(x[4] for x in post),label='4')

plt.legend()
plt.show()







