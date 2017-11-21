#!/usr/bin/python
# -*- coding: UTF-8 -*-
from enum import Enum
class TreeNode:
    #bias=0
    def __init__(self,id,parentID,name):
        self.ID=id
        self.parentID=parentID
        self.name=name
        self.children=[]

    def addChild(self, child):
            self.children.append(child)

    def findParent(self,allNodes):
        #if (self.ID % 100000 == 0):
            #print( "%d nodes scaned \n"%self.ID )
        if (self.parentID == 0):
            return
        if (self.parentID == -1):
            self.parent = allNodes[-1]
            self.parent.addChild(self)
            #TreeNode.bias = 0
            return
        if self.parentID in allNodes.keys():
            self.parent = allNodes[self.parentID]
            self.parent.addChild(self)
            #TreeNode.bias = 0
            return

        ##print("Wrong index ID:%d,parentID:%d\n"%(self.ID,self.parentID))
        self.parentID=-1
        self.parent=allNodes[-1]
        self.parent.addChild(self)
        return

    # def findParent(self,allNodes):
    #     #if (self.ID % 100000 == 0):
    #         #print( "%d nodes scaned \n"%self.ID )
    #     if (self.parentID == 0):
    #         return
    #     if (self.parentID == -1):
    #         self.parent = allNodes[-1]
    #         self.parent.addChild(self)
    #         TreeNode.bias = 0
    #         return
    #     if ((allNodes)[self.parentID].ID == self.parentID):
    #         self.parent = allNodes[self.parentID]
    #         self.parent.addChild(self)
    #         TreeNode.bias = 0
    #         return
    #     if (allNodes[self.parentID + TreeNode.bias].ID == self.parentID):
    #         self.parent = allNodes[self.parentID + TreeNode.bias]
    #         self.parent.addChild(self)
    #         return
    #     for index,node in enumerate(allNodes):
    #         if (node.ID == self.parentID):
    #             self.parent =node
    #             node.addChild(self)
    #             TreeNode.bias = index-self.parentID
    #             return
    #     print("Wrong index ID:%d,parentID:%d\n"%(self.ID,self.parentID))
    #     return

    def getSubTree_NodesCount(self):
        childrenCount = len(self.children)
        result = childrenCount+1
        if result != 0:
            for node in self.children:
                result += node.getSubTree_NodesCount()
        return result

    def getSubTree_NodesVector(self,allTreeNodes):
        for node in self.children:
            allTreeNodes.append(node)
            node.getSubTree_NodesVector(allTreeNodes)

    def childrenSort(self):
        self.children.sort(key=lambda obj:obj.name)
        for node in self.children:
            node.childrenSort()






