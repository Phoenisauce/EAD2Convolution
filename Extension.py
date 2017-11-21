import xml.dom.minidom
from ProcessLog import ProcessLog
import logging
import os
import re
class Extension:
    leveltoweight={'default':2,'safe':1}
    def __init__(self,extensionParseFilePath="Extension.xml"):
        self.ExtensionDict={}
        self.ExtensionWeight={}
        self.unknowExtension={}
        dom=None
        try:
            self.logger=logging.getLogger(ProcessLog.loggerName)
        except:
            print("Error:cant find proper log file.")
        try:
            dom=xml.dom.minidom.parse(extensionParseFilePath)
        except:
            self.logger.critical("Cant read extension parse xml file.Please check!")
            os._exit(1)
        root=dom.documentElement
        classes=root.getElementsByTagName('class')
        for classnode in classes:
            classtype=classnode.getAttribute('type')
            classlevel=classnode.getAttribute('level')
            nodedata=classnode.firstChild.data
            if classlevel in Extension.leveltoweight.keys():
                weight=Extension.leveltoweight[classlevel]
            else:
                weight=Extension.leveltoweight['default']
            self.ExtensionWeight[classtype]=weight
            ss=re.split('[\n ,]',nodedata)
            ss=[item for item in filter(lambda x: x != '', ss)]
            for s in ss:
                self.ExtensionDict[s]=classtype

    def getExtension(self,filePath):
        fileName = re.split('\\\\', filePath)
        fileName = fileName[len(fileName) - 1]
        items = re.split('\.', fileName)
        if len(items) == 0 or len(items) == 1:
            return "None"
        else:
            s=items[len(items) - 1]
            s=s.lower()
            if s in self.ExtensionDict.keys():
                return self.ExtensionDict[s]
            else:
                if s not in self.unknowExtension.keys():
                    self.unknowExtension[s]=1
                else:
                    self.unknowExtension[s]+=1
                return "None"

    def unknowOutput(self,unknowExtensionFile='unknowExtension.txt'):
        file=open(unknowExtensionFile,'w')
        for key in self.unknowExtension.keys():
            file.write("%s:%d\n"%(key,self.unknowExtension[key]))
        file.close()






