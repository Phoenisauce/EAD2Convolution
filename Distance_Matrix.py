from Convolution_Tree_Kernel import  Convolution_Tree_Kernel
import math
import time
class Distance_Matrix:

    # def compute(self,allTrees,sim_algorithm=None):
    #     distance_matrix=[[0.0 for col in range(len(allTrees))] for row in range(len(allTrees))]
    #     selfsim=[0.0 for i in range(len(allTrees))]
    #     for index, t in enumerate(allTrees):
    #         ctk=Convolution_Tree_Kernel()
    #         distance_matrix[index][index]=0.0
    #         #selfsim[index]=sim_algorithm(t,t)
    #         selfsim[index]=ctk.treeConvolution(t,t)
    #     for index1,t1 in enumerate(allTrees):
    #         for index2,t2 in enumerate(allTrees[index1+1:]):
    #             index2=index1+index2+1
    #             ctk = Convolution_Tree_Kernel()
    #             # selfsim[index]=sim_algorithm(t,t)
    #             # distance_matrix[index1][index2]=1-(sim_algorithm(t1,t2)/(math.sqrt(selfsim[index1])*
    #             #                                    math.sqrt(selfsim[index2])))
    #             distance_matrix[index1][index2] = 1 - (ctk.treeConvolution(t1,t2) / (math.sqrt(selfsim[index1]) *
    #                                                                             math.sqrt(selfsim[index2])))
    #             distance_matrix[index2][index1]=distance_matrix[index1][index2]
    #     return distance_matrix

    def compute(self,allTrees,sim_algorithm=None):
        distance_matrix=[[0.0 for col in range(len(allTrees))] for row in range(len(allTrees))]
        selfsim=[0.0 for i in range(len(allTrees))]
        for index, t in enumerate(allTrees):
            distance_matrix[index][index]=0.0
            #selfsim[index]=sim_algorithm(t,t)
            selfsim[index]=sim_algorithm.treeConvolution(t,t)
        for index1,t1 in enumerate(allTrees):

            for index2,t2 in enumerate(allTrees[index1+1:]):
                index2=index1+index2+1
                # selfsim[index]=sim_algorithm(t,t)
                # distance_matrix[index1][index2]=1-(sim_algorithm(t1,t2)/(math.sqrt(selfsim[index1])*
                #                                    math.sqrt(selfsim[index2])))
                distance_matrix[index1][index2] = 1 - (pow(sim_algorithm.treeConvolution(t1,t2),2) / ((selfsim[index1]) *
                                                                                (selfsim[index2])))
                distance_matrix[index2][index1]=distance_matrix[index1][index2]
            print("distance matrix index %d finished"%index1)
        return distance_matrix

    def computeSingleToMulti(self,single,multi):
        distance=0.0
        return distance

    # def computeMultiToMulti(self,newMulti,baseMulti):
    #     distance_matrix = [[0.0 for col in range(len(baseMulti))] for row in range(len(newMulti))]
    #     selfsimbase = [0.0 for i in range(len(baseMulti))]
    #     for index, t in enumerate(baseMulti):
    #         ctk = Convolution_Tree_Kernel()
    #         # selfsim[index]=sim_algorithm(t,t)
    #         selfsimbase[index] = ctk.treeConvolution(t, t)
    #     selfsimnew = [0.0 for i in range(len(newMulti))]
    #     for index, t in enumerate(newMulti):
    #         ctk = Convolution_Tree_Kernel()
    #         # selfsim[index]=sim_algorithm(t,t)
    #         selfsimnew[index] = ctk.treeConvolution(t, t)
    #     for index1, t1 in enumerate(newMulti):
    #         for index2, t2 in enumerate(baseMulti):
    #             ctk = Convolution_Tree_Kernel()
    #             # selfsim[index]=sim_algorithm(t,t)
    #             # distance_matrix[index1][index2]=1-(sim_algorithm(t1,t2)/(math.sqrt(selfsim[index1])*
    #             #                                    math.sqrt(selfsim[index2])))
    #             distance_matrix[index1][index2] = 1 - (ctk.treeConvolution(t1, t2) / (math.sqrt(selfsimnew[index1]) *
    #                                                                                   math.sqrt(selfsimbase[index2])))
    #     return distance_matrix

    def computeMultiToMulti(self,newMulti,baseMulti,sim_algorithm=None):
        distance_matrix = [[0.0 for col in range(len(baseMulti))] for row in range(len(newMulti))]
        selfsimbase = [0.0 for i in range(len(baseMulti))]
        for index, t in enumerate(baseMulti):
            # selfsim[index]=sim_algorithm(t,t)
            selfsimbase[index] = sim_algorithm.treeConvolution(t, t)
        selfsimnew = [0.0 for i in range(len(newMulti))]
        for index, t in enumerate(newMulti):
            # selfsim[index]=sim_algorithm(t,t)
            selfsimnew[index] = sim_algorithm.treeConvolution(t, t)
        for index1, t1 in enumerate(newMulti):
            for index2, t2 in enumerate(baseMulti):
                # selfsim[index]=sim_algorithm(t,t)
                # distance_matrix[index1][index2]=1-(sim_algorithm(t1,t2)/(math.sqrt(selfsim[index1])*
                #                                    math.sqrt(selfsim[index2])))
                distance_matrix[index1][index2] = 1 - (pow(sim_algorithm.treeConvolution(t1, t2),2) / ((selfsimnew[index1]) *
                                                                                      (selfsimbase[index2])))
                if distance_matrix[index1][index2]<0:
                    print("%d,%d,%d"%(sim_algorithm.treeConvolution(t1, t2),selfsimnew[index1],selfsimbase[index2]))
                    time.sleep(10)
        return distance_matrix

