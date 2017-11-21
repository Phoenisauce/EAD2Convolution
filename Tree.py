#!/usr/bin/python
# -*- coding: UTF-8 -*-

import TreeNode

class Tree:
    def __init__(self,root):
        self.root=root
        self.nodes=[self.root]
        self.nodesCount=1


    def getTreeNodes(self):
        #self.nodeCount=self.root.getSubTree_NodesCount()
        self.root.getSubTree_NodesVector(self.nodes)
        self.nodesCount=len(self.nodes)

    def orderTreeNodes(self):
        self.root.childrenSort()

