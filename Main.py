from Preprocess import Preprocess
from ModuleCluster import ModuleCluster
from Convolution_Tree_Kernel import Convolution_Tree_Kernel
from Distance_Matrix import Distance_Matrix
from memory_profiler import profile
from ModuleInstance import  ModuleInstance
from ProcessLog import ProcessLog
from MemoryTest import MemoryTest
from TreeCluster import TreeCluster
from ReadPredictionFile import ReadPredictFile
from Convolution_Tree_Kernel_Mutation import Convolution_Tree_Kernel_Mutation
from Visualize import Visualize
import numpy as np
from sklearn.cluster import DBSCAN
import sys
import time

def main_fuction(readmidfile=False):
    log=ProcessLog('ClusterModel.log',1,'cluster model')
    ProcessLog.loggerName='cluster model'
    dataBasePaths=[]

    datatemp=dataBasePaths[1:]
    dataBasePaths.append('D:/NJ-KING-CAO3.db')
    distance_matrix=[]
    dm = Distance_Matrix()

    V=Visualize()
    moduleLabelDict={}
    ctkm=None
    ft = lambda x: x.nodesCount <= 25


    #     mt=MemoryTest()
#     print('test begin!')
#     mt.test()
#     print('sleep begin!')
#     time.sleep(500)
#     print('sleep end!')
#
# def eee():



    pp = Preprocess()
    begin=time.time()
    pp.extractFromFiles_Robert(True, True, treeNumberLimit=5000, nodeLimit=25)
    end=time.time()
    log.getlog().debug("Read file took %f seconds."%(end-begin))
    pp.generateTrees()
    if readmidfile:
        try:
            modulelabelfile=open("ModuleLabel.txt",'r')
            for l in modulelabelfile:
                row=[x for x in l.split(',')]
                if len(row)==2:
                    moduleLabelDict[row[0]]=int(row[1])
            modulelabelfile.close()

            # mc = ModuleCluster()
            # feature_names, feature_matrix = mc.moduleStatistic_feature_extraction(pp.moduleStatistic)
            # for epsNumber in range(100):
            #     eps = float((epsNumber + 1) / 100)
            #     labels = mc.cluster(eps)
            #     file_open = open("ModuleLabel_eps=" + str(eps) + ".txt", 'w')
            #     i = 0
            #     for moduleName in mc.moduleNameList:
            #         file_open.write("%s,%d\n" % (moduleName, labels[i]))
            #         i += 1
            #     file_open.close()
            #     print("eps=%f is done." % eps)
            # V.cluster_result_linechart(eps_list, cluster_num_list, noise_num_list)
            # labels = mc.cluster()
            distancefile=open("Distancenew.txt",'r')
            colnum=0
            rownum=0
            row=[]
            for l in distancefile:
                row = [float(x) for x in l.split()]
                if len(row) > 0:
                    distance_matrix.append(row)
                    rownum+=1
            print("Distance matrix read. %d trees"%rownum)
            distancefile.close()
            if rownum!=len(row):
                raise Exception("Distance file format wrong!")
        except Exception as e:
            print(e)
            #readmidfile=False



    if readmidfile==False:
        mc=ModuleCluster()
        feature_names,feature_matrix=mc.moduleStatistic_feature_extraction(pp.moduleStatistic)

        for epsNumber in range(100):
            eps=float((epsNumber+1)/100)
            labels = mc.cluster(eps)
            file_open = open("ModuleLabel_eps="+str(eps)+".txt", 'w')
            i = 0
            for moduleName in mc.moduleNameList:
                file_open.write("%s,%d\n" % (moduleName, labels[i]))
                i += 1
            file_open.close()
            print("eps=%f is done."%eps)
        labels=mc.cluster()
        moduleLabelDict=mc.moduleLabelDict
        file_open=open("ModuleLabel5000.txt",'w')
        i=0
        for moduleName in mc.moduleNameList:
            file_open.write("%s,%d\n"%(moduleName,labels[i]))
            i+=1
        file_open.close()
        ctkm = Convolution_Tree_Kernel_Mutation(moduleLabelDict)
        begin=time.time()
        distance_matrix=dm.compute([x for j in pp.allTrees for x in filter(ft,j)],ctkm)
        end=time.time()
        log.getlog().debug("Distance computation took %f seconds." % (end - begin))
        file_open=open("Distancenew5000.txt",'w')
        for r,row in enumerate(distance_matrix):
            for c,col in enumerate(row):
                file_open.write("%.6f "%(col))
            file_open.write("\n")
        file_open.close()



    ctkm = Convolution_Tree_Kernel_Mutation(moduleLabelDict)
    print("test begin!")
    eps_list = []
    cluster_num_list = []
    noise_num_list = []
    for epsNumber in range(100):
        eps=float((epsNumber+1)/100)
        tc=TreeCluster(eps=eps,min_samples=5,metric="precomputed",n_jobs=4)
        tc.Train(distance_matrix)
        eps_list.append(eps)
        cluster_num_list.append(tc.clusterNumber)
        noise_num_list.append(tc.noiseNumber)
    #V.cluster_result_linechart(eps_list,cluster_num_list,noise_num_list)
    tc=TreeCluster(eps=0.5,n_jobs=4)
    begin=time.time()
    tc.Train(distance_matrix)
    end=time.time()
    log.getlog().debug("Clustering took %f seconds." % (end - begin))
    V.cluster_result_linechart(range(2000),tc.DB.labels_,tc.DB.labels_)

    #V.distance_matrix_colormap(distance_matrix,True)


    # file_open = open("Label.txt", 'w')
    # for label in tc.DB.labels_:
    #     file_open.write("%d\n"%label)
    # file_open.close()
    #
    #
    # RPF=ReadPredictFile()
    # RPF.fileToTree()
    # baseMulti=[y for j in pp.allTrees for y in filter(ft,j)]
    # newMulti=[x for j in RPF.allTrees for x in filter(ft,j)]
    # predict_distance_matrix=dm.computeMultiToMulti(newMulti,baseMulti,ctkm)
    # file_open = open("PreDistance.txt", 'w')
    # for r, row in enumerate(predict_distance_matrix):
    #     if r == 409:
    #         count = 0
    #         for c, col in enumerate(row):
    #             file_open.write("%.6f " % (col))
    #             count += 1
    #         print("%d" % count)
    #     else:
    #         for c, col in enumerate(row):
    #             file_open.write("%.6f " % (col))
    #     file_open.write("\n")
    # file_open.close()
    # labels,core_index,dis_core=tc.Predict(predict_distance_matrix)
    # prefile = open("prediction.txt", 'w')
    # for index,label in enumerate(labels):
    #     prefile.write('%d,%d,%lf\n'%(label,core_index[index],dis_core[index]))
    # prefile.close()



if __name__=='__main__':
    main_fuction(False)
    print("all done")


