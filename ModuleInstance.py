#!/usr/bin/python
# -*- coding: UTF-8 -*-
from enum import Enum
from TreeNode import TreeNode
import  sys
import threading

OpTypeNum=7
class OpType(Enum):
    FileCreate=0
    FileMoveTo=1
    FileCopyTo=2
    FileDelete=3
    FileOpen=4
    RegOp=5
    NetConnection=6
##OpType=Enum(('FileChange','FileOpen','RegOp','NetConnection'))

class ModuleInstance(TreeNode):
    #testNode = None
    #testBool = False
    bias=0
    def __init__(self,ID,parentID,name,opCount,linkType):

        TreeNode.__init__(self,ID,parentID,name)
        self.opCount = opCount[:]
        self.subTreeOpCount = opCount[:]
        self.label=self.name
        self.linkType=linkType
        self.extensionDict=[{} for i in range(OpTypeNum)]

    def getChildrenOpCountSumWithFilter(self,opType):
        SubTreeOpCount = self.subTreeOpCount[opType]
        for node in self.children:
            SubTreeOpCount += node.getSubTreeOpCountWithFilter(opType)
        self.subTreeOpCount[opType] = SubTreeOpCount
        return SubTreeOpCount

    def getSubTreeOpCount(self):
        self.subTreeOpCount=self.opCount[:]
        for node in self.children:
            node.getSubTreeOpCount()
            for opType in range(OpTypeNum):
                ##self.subTreeOpCount[opType] += node.getChildrenOpCountSumWithFilter(opType)
                self.subTreeOpCount[opType] += node.subTreeOpCount[opType]

        return self.subTreeOpCount

    def cutNode(self):

        for node in self.children[:]:
            #print("before refCount:%d children:%d" % (sys.getrefcount(node), (len(node.children))))
            sum = 0
            erase = True
            for i in range(OpTypeNum):
                if node.subTreeOpCount[i] != 0 and i != 1:
                    erase=False
                    break
            if erase:

                del node.parent
                node.parentID=None
                self.children.remove(node)
                node.cutSubTree()
                sys.getrefcount(node)
                #print(" refCount:%d"%sys.getrefcount(node))
                del node
            else:
                node.cutNode()
    def cutSubTree(self):
        for node in self.children:
            #if ModuleInstance.testBool==False:
            #    ModuleInstance.testNode=node

            del node.parent
            node.parentID=None
            node.cutSubTree()
            del node
        self.children.clear()


    def cutCheck(self):
        erase=True
        for i in range(OpTypeNum):
            if self.subTreeOpCount[i] != 0 and i != 1:
                erase = False
                break
        return erase


    def merge(self):
        ##try:
            for node1 in self.children[:]:
                if node1 in self.children:
                    for node2 in self.children[self.children.index(node1)+1:]:
                        if node2.name == node1.name:
                            for node3 in node2.children:
                                node3.parent = node1
                                node3.parentID = node1.ID
                                node1.addChild(node3)
                            node2.parent =None
                            node2.parentID = None
                            self.children.remove(node2)
                    node1.merge()
        ##except:
            ##print("merge Error")