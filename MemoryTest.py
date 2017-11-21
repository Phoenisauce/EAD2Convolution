from TreeNode import TreeNode
from ModuleInstance import ModuleInstance
from Tree import Tree
from memory_profiler import profile
import sys
import time
class MemoryTest:

    def test(self):
        treeNodes={}
        trees=[]
        rootNode = TreeNode(-1, 0, 'ROOT')
        treeNodes[-1]=rootNode
        # for i in range(1000000):
        #     if i%10==0:
        #         continue
        #     else:
        #         tn=ModuleInstance(i+1,i,'Node',[0 for index in range(8)],2)
        #         treeNodes[i+1]=tn
        for i in range(5):
            tree=Tree(ModuleInstance(i+1,i,'Node',[0 for index in range(8)],2))
            trees.append(tree)
            print("ref append:%d" % sys.getrefcount(tree))
        # print('sleep begin!')
        # time.sleep(10)
        # print('sleep end!')
        # for tree in trees[:]:
        #     print("ref before:%d"%sys.getrefcount(tree))
        #     trees.remove(tree)
        #     print("ref before:%d" % sys.getrefcount(tree))
        # print("switch")
        for tree in trees:
            print("ref before:%d" % sys.getrefcount(tree))
            trees.remove(tree)
            print("ref before:%d" % sys.getrefcount(tree))
        print('sleep begin!')
        time.sleep(10)
        print('sleep end!')
        # for nodeIndex in treeNodes:
        #     treeNodes[nodeIndex].findParent(treeNodes)
        # for node in rootNode.children:
        #     t = Tree(node)
        #     trees.append(t)
        # tn = 0
        # nn = 0
        # temp = False
        # for t in trees[:]:
        #      t.root.getSubTreeOpCount()
        #      t.root.cutNode()
        #      if t.root.cutCheck():
        #          trees.remove(t)
        #          del t
        # treeNodes.clear()
        # rootNode = TreeNode(-1, 0, 'ROOT')
        # treeNodes[-1] = rootNode
        # for t in trees[:]:
        #     tn += 1
        #     t.getTreeNodes()
        #     nn += t.nodesCount
        #     for node in t.nodes:
        #         treeNodes[node.ID] = node
        #
        # print("Total tree number:%d\nTotal node number:%d"%(tn,nn))
