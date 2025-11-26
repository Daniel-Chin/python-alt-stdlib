'''
Data type that stores file directory structure. 
'''
import os

class Folder:
    __slots__=('name','child','parent','sub_folder','sub_file')
    
    def __init__(self,name='',parent='root'):
        self.name=name
        self.parent=parent
        self.child=[]
        self.sub_folder=[]
        self.sub_file=[]
    
    def addFile(self,name):
        newFile=File(name,self)
        self.child.append(newFile)
        self.sub_file.append(newFile)
    
    def addFolder(self,name):
        newFolder=Folder(name,self)
        self.child.append(newFolder)
        self.sub_folder.append(newFolder)
        return newFolder
    
    def display(self,depth=0):
        if depth==0:
            print(self.name)
        for i in self.sub_file:
            print('|'*depth,i.name)
        for i in self.sub_folder:
            print('|'*depth+'-'+i.name)
            i.display(depth+1)

class File:
    __slots__=('name','parent')
    
    def __init__(self,name,parent):
        self.name=name
        self.parent=parent

def mirror(path):
    root=Folder(path)
    before_cwd=os.getcwd()
    os.chdir(path)
    _getFullDir(root)
    os.chdir(before_cwd)
    return root

def _getFullDir(folder):
    for i in os.listdir():
        if os.path.isfile(i):
            folder.addFile(i)
        else:
            newFolder=folder.addFolder(i)
            os.chdir(i)
            _getFullDir(newFolder)
            os.chdir('..')
