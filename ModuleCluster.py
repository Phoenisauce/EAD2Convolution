from ModuleStatistic import ModuleStatistic
from ModuleInstance import ModuleInstance
from sklearn import feature_extraction
from sklearn.preprocessing import normalize
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
import numpy as np
class ModuleCluster:
    def __init__(self,clusteralgo='DBSCAN',eps=0.3):
        self.feature_extraction=None
        self.feature_matrix=[]
        self.clusterinfo=None
        self.moduleNameList=[]
        self.clusteralgo='DBSCAN'
        self.moduleLabelDict={}
        self.clusterNumber=0
        self.noiseNumber=0

    def moduleStatistic_feature_extraction(self,modulestatisticList):
        finalList=[]
        moduleNameList=[]
        for moduleName in modulestatisticList.keys():
            extensionDict={}
            for index,subDict in enumerate(modulestatisticList[moduleName].extensionDict):
                for extension in subDict.keys():
                    extensionDict[str(index)+'.'+extension]=subDict[extension]
            finalList.append(extensionDict)
            moduleNameList.append(moduleName)
        D=feature_extraction.DictVectorizer(sparse=False)
        newfeatureMatrix=D.fit_transform(finalList)
        featureNames=D.feature_names_
        #tfidfmatrix=feature_extraction.text.TfidfTransformer(smooth_idf=False).fit_transform(newfeatureMatrix)
        #self.feature_matrix=tfidfmatrix.toarray()

        self.feature_matrix=normalize(newfeatureMatrix)
        self.moduleNameList=moduleNameList
        return featureNames,newfeatureMatrix

    def cluster(self,eps=0.27):
        ds=DBSCAN(eps,min_samples=10,n_jobs=4)
        ##ds=KMeans(n_clusters=8)
        ##ds.predict()
        ds.fit(X=self.feature_matrix)
        for index,module in enumerate(self.moduleNameList):
            self.moduleLabelDict[module]=ds.labels_[index]
        self.clusterNumber=ds.labels_.max()+1

        self.noiseNumber=np.sum(ds.labels_==-1)
        return ds.labels_






