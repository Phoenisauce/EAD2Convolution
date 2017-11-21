import sqlite3
import re
from Tree import  Tree
from TreeNode import  TreeNode
from ModuleInstance import ModuleInstance
from ModuleStatistic import  ModuleStatistic
from Extension import Extension
import os.path
import time
from memory_profiler import profile

import sys


OpTypeMap={6:0,7:1,8:2,11:3}
class Preprocess:
    def __init__(self):
        self.rootTreeNode=TreeNode(-1,0,'ROOT')
        self.allNodes=[]
        self.allTrees=[]
        self.allTrees_separated=[]
        self.moduleStatistic={}
        self.extensionParse=Extension()
        self.treeNumber=0
        self.nodeNumber = 0

    def getAllSubFiles(self,basePath):
        fileNameList=[]
        fileDirPathList=[]
        for dirPath, dirNames, fileNames in os.walk(basePath):
            if dirPath!=basePath:
                print("Directory%s" % (dirPath))
                fileDirPathList.append(dirPath)
                for fileName in fileNames:
                    print("File%s"%fileName)
                fileNameList.append(fileNames)
        return fileDirPathList,fileNameList

    def getExtension(self,filePath):
        return self.extensionParse.getExtension(filePath)

    #@profile(precision=4)
    def extractFromFiles_Robert(self,autoGenerateTree=True,withCut=False,withMerge=False,treeNumberLimit=500,nodeLimit=100):

        dirPaths,fileNames=self.getAllSubFiles('d:\\\\EADData\\feature_ex')
        readcount = 0
        OverLoad=False
        for index,dirPath in enumerate(dirPaths):
            #if dirPath=='d:\\\\EADData\\feature_ex\\nj-kevin-song1':
                # if readcount>=10:
                #     break
                if OverLoad:
                    break
                for fileName in fileNames[index]:
                    if re.split('_',fileName)[1]=='link' and re.split('_',fileName)[3].startswith('iexplore'):
                        tn = 0
                        nn = 0
                        readcount+=1
                        for fileOpFile in fileNames[index]:
                            if re.split('_',fileOpFile)[1]=='fop' and re.split('_',fileOpFile)[3]==re.split('_',fileName)[3]:
                                print('started reading %s' % dirPath + '\\' + fileName +' and '+fileOpFile)
                                treeNodes = {}
                                rootNode=TreeNode(-1,0,'ROOT')
                                treeNodes[-1]=rootNode
                                file_open = open(dirPath + '\\' + fileName, 'r', encoding='UTF-8')
                                fileOp_open=open(dirPath + '\\' + fileOpFile, 'r', encoding='UTF-8')
                                fop_line=fileOp_open.readline()
                                fop_items=re.split(',',fop_line)
                                # while True:
                                #     if len(fop_items) == 5:
                                #         if fop_items[0].isdigit():
                                #             fop_items[0] = int(fop_items[0])
                                #         else:
                                #             print('wrong format:%s is not int!' % fop_items[0])
                                #             continue
                                #
                                #         if fop_items[1].isdigit():
                                #             fop_items[1] = int(fop_items[1])
                                #         else:
                                #             print('wrong format:%s is not int!' % fop_items[1])
                                #             continue
                                #     else:
                                #         print('wrong format:%s' % fop_line)
                                #         continue
                                #     break
                                fop_temp=[]
                                lineCount = 0
                                opLineCount=0
                                # for line in file_open:
                                #     if line == "\n":
                                #         continue
                                #     items = re.split(',', line)
                                #     lineCount += 1
                                #     if len(items) == 5:
                                #         if items[0].startswith('['):
                                #             items[0] = items[0].split('[')[1]
                                #         items[0]=int(items[0])
                                #         items[1] = int(items[1])
                                #         items[2] = int(items[2])
                                #         items[4] = items[4].split(']')[0]
                                items=[]
                                linkID=-1
                                opID=-1
                                linkFileRead = False
                                opFileRead = False
                                for line in file_open:
                                    if line == "\n":
                                        continue
                                    if line == "":
                                        break
                                    temp_items = re.split(',', line)
                                    lineCount += 1
                                    if len(temp_items) == 5:
                                        if temp_items[0].startswith('['):
                                            temp_items[0] = temp_items[0].split('[')[1]
                                        if temp_items[0].isdigit():
                                            temp_items[0] = int(temp_items[0])
                                        else:
                                            #print('wrong format:%s is not int!' % temp_items[0])
                                            continue
                                        if temp_items[1].isdigit():
                                            temp_items[1] = int(temp_items[1])
                                        else:
                                            #print('wrong format:%s is not int!' % temp_items[1])
                                            continue
                                        if temp_items[2].isdigit():
                                            temp_items[2] = int(temp_items[2])
                                        else:
                                            #print('wrong format:%s is not int!' % temp_items[2])
                                            continue
                                        temp_items[4] = temp_items[4].split(']')[0]
                                    else:
                                        #print('wrong format:%s' % line)
                                        continue
                                    items = temp_items
                                    if items[0] not in treeNodes.keys():
                                        node = ModuleInstance(items[0], int(items[1]), items[4],
                                                              [0 for index in range(8)], items[2])
                                        if items[4] not in self.moduleStatistic:
                                            ms = ModuleStatistic(items[4])
                                            self.moduleStatistic[items[4]] = ms
                                        self.moduleStatistic[items[4]].count += 1
                                        treeNodes[items[0]] = node
                                node=None
                                oldID=-1
                                oldErrorModuleID=-1
                                for line in fileOp_open:
                                    if line == "\n":
                                        continue
                                    if line == "":
                                        break
                                    temp_items = re.split(',', line)
                                    lineCount += 1
                                    if len(temp_items) == 5:
                                        if temp_items[0].startswith('['):
                                            temp_items[0] = temp_items[0].split('[')[1]
                                        if temp_items[0].isdigit():
                                            temp_items[0] = int(temp_items[0])
                                        else:
                                            print('wrong format:%s is not int!' % temp_items[0])
                                            continue
                                        if temp_items[1].isdigit():
                                            temp_items[1] = int(temp_items[1])
                                            if temp_items[1] not in OpTypeMap.keys():
                                                #print('wrong value:%s is illegal !' % temp_items[1])
                                                continue
                                        else:
                                            print('wrong format:%s is not int!' % temp_items[0])
                                            continue
                                        if temp_items[2].isdigit():
                                            temp_items[2] = int(temp_items[2])
                                        else:
                                            print('wrong format:%s is not int!' % temp_items[2])
                                            continue
                                        temp_items[4] = temp_items[4].split(']')[0]
                                    else:
                                        print('wrong format:%s' % line)
                                        continue
                                    items = temp_items
                                    if(items[0]==oldID):
                                        node.opCount[OpTypeMap[items[1]]] += 1
                                        if self.getExtension(items[3]) not in \
                                                self.moduleStatistic[node.name].extensionDict[
                                                    OpTypeMap[items[1]]].keys():
                                            self.moduleStatistic[node.name].extensionDict[
                                                OpTypeMap[items[1]]][self.getExtension(items[3])] = 1
                                        else:
                                            self.moduleStatistic[items[4]].extensionDict[
                                                OpTypeMap[items[1]]][self.getExtension(items[3])] += 1
                                        if self.getExtension(items[3]) not in node.extensionDict[
                                            OpTypeMap[items[1]]].keys():
                                            node.extensionDict[OpTypeMap[items[1]]][
                                                self.getExtension(items[3])] = 1
                                        else:
                                            node.extensionDict[OpTypeMap[items[1]]][
                                                self.getExtension(items[3])] += 1
                                    else:
                                        if items[0] in treeNodes.keys():
                                            node=treeNodes[items[0]]
                                            node.opCount[OpTypeMap[items[1]]] += 1
                                            if self.getExtension(items[3]) not in \
                                                    self.moduleStatistic[node.name].extensionDict[
                                                        OpTypeMap[items[1]]].keys():
                                                self.moduleStatistic[node.name].extensionDict[
                                                    OpTypeMap[items[1]]][self.getExtension(items[3])] = 1
                                            else:
                                                self.moduleStatistic[node.name].extensionDict[
                                                    OpTypeMap[items[1]]][self.getExtension(items[3])] += 1
                                            if self.getExtension(items[3]) not in node.extensionDict[
                                                OpTypeMap[items[1]]].keys():
                                                node.extensionDict[OpTypeMap[items[1]]][
                                                    self.getExtension(items[3])] = 1
                                            else:
                                                node.extensionDict[OpTypeMap[items[1]]][
                                                    self.getExtension(items[3])] += 1
                                        else:
                                            if items[0]!=oldErrorModuleID:
                                                #print('Cant find %d module' %items[0])
                                                oldErrorModuleID=items[0]


                                # linkFileRead, items,lineCount = self.getLinkLine(file_open,items, lineCount)
                                # node = None
                                # if linkFileRead==False:
                                #     print("Link File error %s"%fileName)
                                #     continue
                                # else:
                                #     if items[0] not in treeNodes.keys():
                                #         node = ModuleInstance(items[0], int(items[1]), items[4],
                                #                               [0 for index in range(8)], items[2])
                                #         if items[4] not in self.moduleStatistic:
                                #             ms = ModuleStatistic(items[4])
                                #             self.moduleStatistic[items[4]] = ms
                                #         self.moduleStatistic[items[4]].count += 1
                                #         treeNodes[items[0]] = node
                                #         linkID = items[0]
                                #
                                #
                                # opFileRead, fop_items,opLineCount = self.getOpFileLine(fileOp_open,fop_items,opLineCount)
                                # if linkFileRead==False:
                                #     print("Op File error %s"%fileOpFile)
                                # else:
                                #     opID = fop_items[0]
                                #
                                # while True:
                                #     newRecord=False
                                #     if (linkID==-1 or linkID<opID) and linkFileRead == True:
                                #         linkFileRead,items,lineCount=self.getLinkLine(file_open,items,lineCount)
                                #         if items[0] not in treeNodes.keys():
                                #             node = ModuleInstance(items[0], int(items[1]), items[4],[0 for index in range(8)],items[2])
                                #             if items[4] not in self.moduleStatistic.keys():
                                #                 ms=ModuleStatistic(items[4])
                                #                 self.moduleStatistic[items[4]] = ms
                                #             self.moduleStatistic[items[4]].count += 1
                                #             treeNodes[items[0]] = node
                                #             newRecord = True
                                #     if (opID == -1 or linkID>=opID) and opFileRead == True:
                                #         opFileRead,fop_items,opLineCount=self.getOpFileLine(fileOp_open,fop_items,opLineCount)
                                #         newRecord=opFileRead
                                #     if (linkFileRead or opFileRead) !=True:
                                #         break
                                #     if ((lineCount + opLineCount) % 100 == 0):
                                #         print(".", end="")
                                #
                                #     if newRecord:
                                #         linkID = items[0]
                                #         opID = fop_items[0]
                                #         if linkID==opID:
                                #             node.opCount[OpTypeMap[fop_items[1]]] += 1
                                #             if self.getExtension(fop_items[3]) not in self.moduleStatistic[items[4]].extensionDict[OpTypeMap[fop_items[1]]].keys():
                                #                 self.moduleStatistic[items[4]].extensionDict[
                                #                 OpTypeMap[fop_items[1]]][self.getExtension(fop_items[3])] = 1
                                #             else:
                                #                 self.moduleStatistic[items[4]].extensionDict[
                                #                     OpTypeMap[fop_items[1]]][self.getExtension(fop_items[3])] += 1
                                #             if self.getExtension(fop_items[3]) not in node.extensionDict[
                                #                 OpTypeMap[fop_items[1]]].keys():
                                #                 node.extensionDict[OpTypeMap[fop_items[1]]][self.getExtension(fop_items[3])] = 1
                                #             else:
                                #                 node.extensionDict[OpTypeMap[fop_items[1]]][
                                #                     self.getExtension(fop_items[3])] += 1
                                #         if linkID>opID:
                                #             fop_temp.append(fop_items[:])
                                #         if linkID<opID:
                                #             continue
                                #
                                #
                                #
                                #
                                #
                                #         # if items[0]<fop_items[0]:
                                #         #     continue
                                #         # if items[0] > fop_items[0]:
                                #         #     fop_temp.append(fop_items[:])
                                #             #raise Exception('Fop check failed!File:%s Line:%d \n\t%s,%d,%d' % (
                                #             #        dirPaths[index] + '\\' + fileName, lineCount, line, items[0],fop_items[0]))
                                #
                                #         # while items[0]==fop_items[0] or fop_line=='':
                                #         #     node.opCount[OpTypeMap[fop_items[1]]]+=1
                                #         #     if self.getExtension(fop_items[3]) not in self.moduleStatistic[items[4]].extensionDict[OpTypeMap[fop_items[1]]].keys():
                                #         #         self.moduleStatistic[items[4]].extensionDict[
                                #         #             OpTypeMap[fop_items[1]]][self.getExtension(fop_items[3])] =1
                                #         #     else:
                                #         #         self.moduleStatistic[items[4]].extensionDict[
                                #         #             OpTypeMap[fop_items[1]]][self.getExtension(fop_items[3])] += 1
                                #         #     if self.getExtension(fop_items[3]) not in node.extensionDict[OpTypeMap[fop_items[1]]].keys():
                                #         #         node.extensionDict[OpTypeMap[fop_items[1]]][self.getExtension(fop_items[3])] =1
                                #         #     else:
                                #         #         node.extensionDict[OpTypeMap[fop_items[1]]][self.getExtension(fop_items[3])] += 1
                                #         #     fop_line = fileOp_open.readline()
                                #         #     if fop_line=='':
                                #         #         break
                                #         #     fop_items = re.split(',', fop_line)
                                #         #
                                #         #     if len(fop_items)==5:
                                #         #         if fop_items[0].isdigit():
                                #         #             fop_items[0]=int(fop_items[0])
                                #         #         else:
                                #         #             print('wrong format:%s is not int!'%fop_items[0])
                                #         #         if fop_items[1].isdigit():
                                #         #             fop_items[1] = int(fop_items[1])
                                #         #         else:
                                #         #             print('wrong format:%s is not int!' % fop_items[1])
                                #         #     else:
                                #         #         print('wrong format:%s'%fop_line)
                                #         #     continue
                                #
                                #
                                # for fop_rec in fop_temp:
                                #     if fop_rec[0] in treeNodes.keys():
                                #         treeNodes[fop_rec[0]].opCount[OpTypeMap[fop_items[1]]] += 1
                                #
                                #         if self.getExtension(fop_rec[3]) not in self.moduleStatistic[treeNodes[fop_rec[0]].name].extensionDict[OpTypeMap[fop_rec[1]]].keys():
                                #             self.moduleStatistic[treeNodes[fop_rec[0]].name].extensionDict[
                                #                 OpTypeMap[fop_rec[1]]][self.getExtension(fop_rec[3])] = 1
                                #         else:
                                #             self.moduleStatistic[treeNodes[fop_rec[0]].name].extensionDict[
                                #                 OpTypeMap[fop_rec[1]]][self.getExtension(fop_rec[3])] += 1
                                #         if self.getExtension(fop_rec[3]) not in treeNodes[fop_rec[0]].extensionDict[
                                #             OpTypeMap[fop_rec[1]]].keys():
                                #             treeNodes[fop_rec[0]].extensionDict[OpTypeMap[fop_rec[1]]][self.getExtension(fop_rec[3])] = 1
                                #         else:
                                #             treeNodes[fop_rec[0]].extensionDict[OpTypeMap[fop_rec[1]]][
                                #                 self.getExtension(fop_rec[3])] += 1
                                #     else:
                                #         print('Cant find %d module'%fop_rec[0])

                                file_open.close()
                                fileOp_open.close()
                                trees = []
                                if autoGenerateTree:
                                    for nodeIndex in treeNodes:
                                        treeNodes[nodeIndex].findParent(treeNodes)
                                    for node in rootNode.children:
                                        tree = Tree(node)
                                        trees.append(tree)
                                        #print("tree refcount append:%d" % sys.getrefcount(tree))

                                    # print('sleep begin!')
                                    # time.sleep(10)
                                    # print('sleep end!')
                                    for t in trees[:]:
                                        #print("tree refcount before:%d" % sys.getrefcount(t))
                                        t.root.getSubTreeOpCount()
                                        t.root.cutNode()
                                        if t.root.cutCheck():
                                            trees.remove(t)
                                            #print("tree refcount after:%d"%sys.getrefcount(t))
                                            del t
                                    treeNodes.clear()
                                    rootNode = TreeNode(-1, 0, 'ROOT')
                                    treeNodes[-1] = rootNode
                                    for t in trees[:]:

                                        t.getTreeNodes()
                                        if t.nodesCount>=nodeLimit:
                                            trees.remove(t)
                                            continue
                                        tn += 1
                                        nn+=t.nodesCount
                                        for node in t.nodes:
                                            treeNodes[node.ID]=node
                                    print('\t%d lines in %s' % (lineCount, fileName))
                                    self.allNodes.append(treeNodes)
                                    if self.treeNumber+tn>=treeNumberLimit:
                                        self.allTrees.append(trees[:treeNumberLimit-self.treeNumber])
                                        self.treeNumber=treeNumberLimit
                                        OverLoad=True
                                    else:
                                        self.allTrees.append(trees)
                                        self.treeNumber+=tn
                                    self.nodeNumber+=nn
                                #if withMerge==True:

                                #print('\t%d lines in %s' % (lineCount, fileName))
                                print("tree number:%d\nnode number:%d"%(tn,nn))
                                print("Total tree number:%d\nTotal node number:%d" % (self.treeNumber, self.nodeNumber))
                    if self.treeNumber>=treeNumberLimit:
                        OverLoad=True
                        break
                                # print('sleep begin!')
                                # time.sleep(10)
                                # print('sleep end!')
        print("Total tree number:%d\nTotal node number:%d"%(self.treeNumber,self.nodeNumber))
        self.extensionParse.unknowOutput()

    def getLinkLine(self,linkFile,items,lineCount):
        readSuccess=True
        while True:
            line=linkFile.readline()
            if line == "\n":
                continue
            if line == "":
                readSuccess=False
                break
            temp_items = re.split(',', line)
            lineCount += 1
            if len(temp_items) == 5:
                if temp_items[0].startswith('['):
                    temp_items[0] = temp_items[0].split('[')[1]
                if temp_items[0].isdigit():
                    temp_items[0] = int(temp_items[0])
                else:
                    #print('wrong format:%s is not int!' %temp_items[0])
                    continue
                if temp_items[1].isdigit():
                    temp_items[1] = int(temp_items[1])
                else:
                    #print('wrong format:%s is not int!' %temp_items[1])
                    continue
                if temp_items[2].isdigit():
                    temp_items[2] = int(temp_items[2])
                else:
                    #print('wrong format:%s is not int!' %temp_items[2])
                    continue
                temp_items[4] = temp_items[4].split(']')[0]
            else:
                #print('wrong format:%s' % line)
                continue
            items=temp_items
            break
        return readSuccess,items,lineCount

    def getOpFileLine(self,OpFile,items,lineCount):
        readSuccess=True
        while True:
            line=OpFile.readline()
            if line == "\n":
                continue
            if line == "":
                readSuccess=False
                break
            temp_items = re.split(',', line)
            lineCount += 1
            if len(temp_items) == 5:
                if temp_items[0].startswith('['):
                    temp_items[0] = temp_items[0].split('[')[1]
                if temp_items[0].isdigit():
                    temp_items[0] = int(temp_items[0])
                else:
                    #print('wrong format:%s is not int!' %temp_items[0])
                    continue
                if temp_items[1].isdigit():
                    temp_items[1] = int(temp_items[1])
                    if temp_items[1] not in OpTypeMap.keys():
                        #print('wrong value:%s is illegal !' % temp_items[1])
                        continue
                else:
                    #print('wrong format:%s is not int!' %temp_items[0])
                    continue
                if temp_items[2].isdigit():
                    temp_items[2] = int(temp_items[2])
                else:
                    #print('wrong format:%s is not int!' %temp_items[2])
                    continue
                temp_items[4] = temp_items[4].split(']')[0]
            else:
                #print('wrong format:%s' % line)
                continue
            items=temp_items
            break
        return readSuccess,items,lineCount






    def getAllNodes(self,dataBasePaths):

        for path in dataBasePaths:

            treeNodes={}
            treeNodes[-1]=self.rootTreeNode
            # treeNodes.append(self.rootTreeNode)
            conn = sqlite3.connect(path)
            print ("Opened database successfully")

            cursor = conn.execute("select ModuleID,ParentID,FileName,FileChangeCount,FileOpenCount,RegOpCount,"
                              "NetworkConnectionCount from TModuleCount;")
            for index,row in enumerate(cursor):
                mi=ModuleInstance(row[0],row[1],row[2],[row[3],row[4],row[5],row[6]])
                #treeNodes.append(mi)
                treeNodes[row[0]]=mi
                if index%100000==0:
                    print("%d nodes get\n"%index)
            conn.close()
            self.allNodes.append(treeNodes)
        return  self.allNodes

    def generateTrees(self):
        for nodeDict in self.allNodes:
            for nodeIndex in nodeDict:
                nodeDict[nodeIndex].findParent(nodeDict)
        for node in self.rootTreeNode.children:
            for treeRoot in node.children:
                t=Tree(treeRoot)
                self.allTrees.append(t)
        return self.allTrees

    def nodesPruning(self,merge,cut):
        print("%d trees"%len(self.allTrees))
        if cut:
            tn=0
            for t in self.allTrees[:]:
                t.root.getSubTreeOpCount()

                t.root.cutNode()
                tn+=1
                if t.root.cutCheck():
                    self.allTrees.remove(t)
            print("%d callCount with %d trees %d" % (ModuleInstance.callCount,tn,len(self.allTrees)))
        if merge:
            for t in self.allTrees:
                ##try:
                    t.root.merge()
                ##except:
                    ##print("for error")

    def treesFinalSettle(self):
        #self.allNodes[0].ID=0
        #newAllNodes = [self.allNodes[0]]
        #idConvetor = {-1:0}
        self.allNodes=[]
        for trees in self.allTrees:
            nodes=[]
            for t in trees:
                t.orderTreeNodes()
                t.getTreeNodes()
                t.root.parentID=-1
                nodes.append(t.nodes)
            self.allNodes.append(nodes)
        #     for node in t.nodes:
        #         if node.parentID!=None:
        #             idConvetor[node.ID] = len(newAllNodes)
        #             if node.parentID == -1:
        #                 node.parentID = 0
        #             else:
        #                 if node.parentID in idConvetor.keys():
        #                     node.parentID = idConvetor[node.parentID]
        #                 else:
        #                     print("%d"%node.parentID)
        #             node.ID=idConvetor[node.ID]
        #             newAllNodes.append(node)
        # self.allNodes=newAllNodes









