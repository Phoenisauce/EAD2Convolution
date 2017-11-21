"""
================================================================
Plot the decision surface of a decision tree on the iris dataset
================================================================
Plot the decision surface of a decision tree trained on pairs
of features of the iris dataset.
See :ref:`decision tree <tree>` for more information on the estimator.
For each pair of iris features, the decision tree learns decision
boundaries made of combinations of simple thresholding rules inferred from
the training samples.
"""
print(__doc__)

import numpy as np
from sklearn.cluster import DBSCAN

class TreeCluster:
    def __init__(self,eps=0.5,metric='precomputed',min_samples=5,
                 algorithm='auto', leaf_size=30, p=None, n_jobs=1):

        self.DB=DBSCAN(eps,min_samples,metric,
                 algorithm, leaf_size, p, n_jobs)

        self.clusterNumber=0
        self.noiseNumber=0

    def Train(self,sampleArray):
        self.DB.fit(sampleArray)
        self.clusterNumber=self.DB.labels_.max()+1
        self.noiseNumber=np.sum(self.DB.labels_==-1)
        return
    def Predict(self,testSample):
        # Result is noise by default
        y_new = np.ones(shape=len(testSample), dtype=int) * -1
        core_index=[0 for index in range(len(testSample))]
        dis_core=[1.0 for index in range(len(testSample))]

        # Iterate all input samples for a label
        for j, x_new in enumerate(testSample):
            # Find a core sample closer than EPS
            min_dis=1.0
            min_core_index=0
            for i, x_core in enumerate(self.DB.components_):
                if x_new[self.DB.core_sample_indices_[i]] < min_dis:
                    min_dis=x_new[self.DB.core_sample_indices_[i]]
                    min_core_index=self.DB.core_sample_indices_[i]
                    # Assign label of x_core to x_new
            core_index[j]=min_core_index
            dis_core[j]=min_dis
            if dis_core[j] < self.DB.eps:
                y_new[j]=self.DB.labels_[core_index[j]]
        # for j,x_new in enumerate(testSample):
        #
        #
        #             y_new[j] = self.DB.labels_[self.DB.core_sample_indices_[i]]
        #             core_index[j]=self.DB.core_sample_indices_[i]
        #             dis_core[j]=x_new[i]
        #             break

        return y_new,core_index,dis_core

    def SaveModel(self):
        return
    def LoadModel(self):

        return





