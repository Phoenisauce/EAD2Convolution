import re
class DataGet:
    def readFile(self,filePath,format,separator=','):
        file_open=open(filePath,'r', encoding='UTF-8')
        formatLength=len(format)
        dataSet=[]
        for line in file_open:
            items = re.split(separator, line)

            if items[0]=='':
                items.remove(items[0])
            if len(items)<formatLength:
                continue
            if len(items)>formatLength:
                items=items[0:formatLength]
            formatCheck=True
            for index,item in enumerate(items):
                if format[index]=='int':
                    if item.isdigit():
                        items[index]=int(item)
                    else:
                        formatCheck=False
                        break
            if formatCheck:
                dataSet.append(items)
        file_open.close()
        return dataSet





    def rowDataFilter(self,line,format):
        formatLength = len(format)
        items = re.split(' ', line)
        if len(items) != formatLength:
            return None
        else:
            formatCheck = True
            for index, item in enumerate(items):
                if format[index] == 'int':
                    if item.isdigit():
                        item = int(item)
                    else:
                        formatCheck = False
                        break
            if formatCheck:
                return items
            else:
                return None
