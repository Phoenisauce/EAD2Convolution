import Tree
import ModuleInstance
import decimal
import os
class Convolution_Tree_Kernel:
    def __init__(self):
        self.t1=None
        self.t2=None
        self.Convolution = []

    def treeConvolution(self,t1,t2):
        self.t1=t1
        self.t2=t2
        result = 0.0
        self.Convolution = [[-1 for col in range(t2.nodesCount)] for row in range(t1.nodesCount)]
        for n1 in range(t1.nodesCount):
            for n2 in range(t2.nodesCount):
                if self.Convolution[n1][n2] == -1:
                    self.Convolution[n1][n2]=self.nodeConvolution(t1.nodes[n1], t2.nodes[n2])
                try:
                    result += self.Convolution[n1][n2]
                except:
                    print("%d,%d,%d,%f"%(t1.nodesCount,t2.nodesCount,self.Convolution[n1][n2],result))
                    for i in range(t1.nodesCount):
                        for j in range(t2.nodesCount):
                            print("error:%d " % self.Convolution[i][j], end="")
                        print("\n")
                    os._exit(-1)
        return result


    #@staticmethod
    def nodeConvolution(self,tn1,tn2):

        if tn1.label != tn2.label:
            return 0
        else:
            if len(tn1.children) ==0 and len(tn2.children) == 0:
                return 1
            else:
                Sum = [[0 for col in range(len(tn2.children)+1)] for row in range(len(tn1.children)+1)]
            for i in range(len(tn1.children)+1):
                for j in range(len(tn2.children)+1):
                    if i == 0 or j == 0:
                        Sum[i][j]=1
                    else:
                        n1=self.t1.nodes.index(tn1.children[i-1])
                        n2=self.t2.nodes.index(tn2.children[j-1])
                        if self.Convolution[n1][n2]==-1:
                            self.Convolution[n1][n2]=self.nodeConvolution(tn1.children[i-1],tn2.children[j-1])
                        Sum[i][j]=Sum[i-1][j]+Sum[i][j-1]+Sum[i-1][j-1] * (self.Convolution[n1][n2]-1)
            result = Sum[len(tn1.children)][len(tn2.children)]
            # if tn1.ID == 1559527:
            #     for i in range(len(tn1.children) + 1):
            #         for j in range(len(tn2.children) + 1):
            #             print("%d "%Sum[i][j],end="")
            #         print("\n")
            return result