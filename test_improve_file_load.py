from encodings import utf_8
import os 
class files():
    def __init__(self,dir,mode):
        self.dir=dir
        self.mode=mode
        self.file_name="file_name"
    def get_cotent(self):
        with open(self.dir,self.mode,utf=utf_8) as a:
            self.content=a.readlines()


skills=files(mode="r",dir="skills\\fireball.txt")
skills.get_cotent()
print(skills.content)
