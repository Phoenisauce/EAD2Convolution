import Tree
import ModuleInstance
import decimal
import os
class Convolution_Tree_Kernel_Mutation:
    def __init__(self,moduleLableDict):
        self.moduleLableDict = moduleLableDict

    def treeConvolution(self,t1,t2):
        result = 0.0
        Convolution = [[-1 for col in range(t2.nodesCount)] for row in range(t1.nodesCount)]
        for n1 in range(t1.nodesCount):
            for n2 in range(t2.nodesCount):
                if Convolution[n1][n2] == -1:
                    Convolution[n1][n2]=self.nodeConvolution(t1.nodes[n1], t2.nodes[n2],t1,t2,Convolution)
                try:
                    result += Convolution[n1][n2]
                except:
                    print("%d,%d,%d,%f"%(t1.nodesCount,t2.nodesCount,self.Convolution[n1][n2],result))
                    for i in range(t1.nodesCount):
                        for j in range(t2.nodesCount):
                            print("%d " % Convolution[i][j], end="")
                        print("\n")
                    os._exit(-1)
        return result


    #@staticmethod
    def nodeConvolution(self,tn1,tn2,t1,t2,Convolution):
        labelSim=0
        result=0
        Con=0
        if tn1.label == tn2.label:
            labelSim=1
        else:
            if tn1.label in self.moduleLableDict.keys() and tn2.label in self.moduleLableDict.keys():
                if self.moduleLableDict[tn1.label]==self.moduleLableDict[tn2.label]:
                    if self.moduleLableDict[tn1.label]==-1:
                        labelSim=0.3
                    else:
                        labelSim=0.8
                else:
                    labelSim=0.5
            else:
                labelSim=0.3

        if len(tn1.children) ==0 and len(tn2.children) == 0:
            Con=1
        else:
            Sum = [[0 for col in range(len(tn2.children)+1)] for row in range(len(tn1.children)+1)]
            for i in range(len(tn1.children)+1):
                for j in range(len(tn2.children)+1):
                    if i == 0 or j == 0:
                        Sum[i][j]=1
                    else:
                        n1=t1.nodes.index(tn1.children[i-1])
                        n2=t2.nodes.index(tn2.children[j-1])
                        if Convolution[n1][n2]==-1:
                            Convolution[n1][n2]=self.nodeConvolution(tn1.children[i-1],tn2.children[j-1],t1,t2,Convolution)
                        Sum[i][j]=Sum[i-1][j]+Sum[i][j-1]+Sum[i-1][j-1] * (Convolution[n1][n2]-1)
                        try:
                            result = float(Sum[i][j])
                        except:
                            print("%d" % result)
            Con = Sum[len(tn1.children)][len(tn2.children)]
        result=Con*labelSim

        return result