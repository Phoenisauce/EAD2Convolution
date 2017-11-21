from ModuleInstance import  ModuleInstance
OpTypeNum=7
class ModuleStatistic:
    def __init__(self,name):
        self.name=name
        self.count=0
        self.fopCount=[0 for i in range(OpTypeNum)]
        self.extensionDict=[{} for i in range(OpTypeNum)]


