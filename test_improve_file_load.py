
import os,platform


directories=[]
if platform.system()=="Windows":
    directories=[".\\enemies",".\\items",".\\skills"]
else:
    directories=["./enemies","./items","./skills"]
    
   



class files():
    def __init__(self,file,mode):
        self.file=file
        self.direcion=None
        self.directory=None
        self.content=None   
        self.mode=mode
    def set_format(self):
        for i in directories:
            if self.file in os.listdir(i):
                self.directory= i
            else:
                continue 
        self.direcion=self.directory + "\\" + self.file
        with open (self.direcion,self.mode) as a :
            self.content=a.readlines()
    def set_items(self):
        if self.directory== ".\enemies":
            
skills=files(mode="r",file="fireball.txt")
skills.set_format()
print(skills.content)


