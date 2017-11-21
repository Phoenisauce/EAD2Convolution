import os
import re
from TreeNode import TreeNode
from Tree import Tree
from ModuleInstance import ModuleInstance
from Extension import Extension

OpTypeMap={6:0,7:1,8:2,11:3}
class ReadPredictFile:
    def __init__(self):
        self.allTreeNodes=[]
        self.allTrees =[]
        self.extensionParse=Extension()
        return

    def getExtension(self,filePath):
        return self.extensionParse.getExtension(filePath)

    def getAllSubFiles(self,basePath):
        fileNameList=[]
        fileDirPathList=[]
        for dirPath, dirNames, fileNames in os.walk(basePath):
            print("Directory%s" % (dirPath))
            fileDirPathList.append(dirPath)
            for fileName in fileNames:
                print("File%s"%fileName)
            fileNameList.append(fileNames)
        return fileDirPathList,fileNameList

    def fileToTree(self):
        dirPaths, fileNames = self.getAllSubFiles('d:\\EADData\\data_to_train_all_data')
        readcount = 0


        for index, dirPath in enumerate(dirPaths):
            for fileName in fileNames[index]:
                #if not fileName.startswith("nj-albert-ji_iexplore_train"):
                #    continue
                if readcount>5:
                    break
                readcount+=1
                fileOpen=open(dirPath + '\\' + fileName, 'r', encoding='UTF-8')
                print('Reading %s'%(dirPath + '\\' + fileName))
                emptyLineCount=0
                Trees = []
                modulefileOpList = []
                moduleChain = []
                modulelist = []
                totalFileOplist = []
                readChain=True
                ID=0
                for line in fileOpen:
                    if line=="" or line=="\n":
                        emptyLineCount+=1
                        readChain=True
                        if emptyLineCount == 1:
                            modulelist.append(moduleChain)
                            totalFileOplist.append(modulefileOpList)
                            moduleChain=[]
                            modulefileOpList=[]
                        if emptyLineCount == 2:
                            module=ModuleInstance(ID,-1,'iexplore.exe',[0 for index in range(8)],3)
                            tree=Tree(module)
                            Trees.append(tree)
                            ID+=1

                            for index1,mc in enumerate(modulelist):
                                temp=module
                                for m in mc[::-1]:
                                    check=False
                                    for tempchild in temp.children:
                                        if tempchild.name==m:
                                            check=True
                                            temp=tempchild
                                            break
                                    if check:
                                        continue
                                    else:
                                        newmodule=ModuleInstance(ID,temp.ID,m,[0 for index in range(8)],3)
                                        ID+=1
                                        temp.children.append(newmodule)
                                        newmodule.parent=temp
                                        temp=newmodule
                                for fileOp in totalFileOplist[index1]:
                                    temp.opCount[OpTypeMap[fileOp['OpType']]] += 1
                                    if self.getExtension(fileOp['filepath']) not in temp.extensionDict[OpTypeMap[fileOp['OpType']]].keys():
                                        temp.extensionDict[OpTypeMap[fileOp['OpType']]][
                                            self.getExtension(fileOp['filepath'])] = 1
                                    else:
                                        temp.extensionDict[OpTypeMap[fileOp['OpType']]][
                                            self.getExtension(fileOp['filepath'])] += 1
                            modulefileOpList = []
                            moduleChain = []
                            modulelist = []
                            totalFileOplist = []
                        continue
                    if readChain:
                        modules = re.split(',', line)
                        moduleChain=[]
                        for module in modules[:len(modules)-1]:
                            ss=re.split('\\\\',module)
                            moduleName=ss[len(ss)-1]
                            moduleChain.append(moduleName)
                        readChain=False
                        emptyLineCount=0
                    else:
                        ss=re.split(',',line)
                        if ss[1]=='1':
                            modulefileOpList.append({'filepath':ss[3],'OpType':int(ss[2])})
                        emptyLineCount = 0
                        ###
                if len(modulelist)!=0:
                    module = ModuleInstance(ID, -1, 'iexplore.exe', [0 for index in range(8)], 3)
                    tree = Tree(module)
                    Trees.append(tree)
                    ID += 1

                    for index1, mc in enumerate(modulelist):
                        temp = module
                        for m in mc[::-1]:
                            check = False
                            for tempchild in temp.children:
                                if tempchild.name == m:
                                    check = True
                                    temp = tempchild
                                    break
                            if check:
                                continue
                            else:
                                newmodule = ModuleInstance(ID, temp.ID, m, [0 for index in range(8)], 3)
                                ID += 1
                                temp.children.append(newmodule)
                                newmodule.parent = temp
                                temp = newmodule
                        for fileOp in totalFileOplist[index1]:
                            temp.opCount[OpTypeMap[fileOp['OpType']]] += 1
                            if self.getExtension(fileOp['filepath']) not in temp.extensionDict[
                                OpTypeMap[fileOp['OpType']]].keys():
                                temp.extensionDict[OpTypeMap[fileOp['OpType']]][
                                    self.getExtension(fileOp['filepath'])] = 1
                            else:
                                temp.extensionDict[OpTypeMap[fileOp['OpType']]][
                                    self.getExtension(fileOp['filepath'])] += 1
                fileOpen.close()
                for t in Trees[:]:
                    # print("tree refcount before:%d" % sys.getrefcount(t))
                    t.root.getSubTreeOpCount()
                    t.root.cutNode()
                    if t.root.cutCheck():
                        Trees.remove(t)
                        # print("tree refcount after:%d"%sys.getrefcount(t))
                        del t
                for t in Trees[:]:
                    t.getTreeNodes()
                self.allTrees.append(Trees)


