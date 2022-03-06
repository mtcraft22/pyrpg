import itemsclasses 
import os,platform


directories=[]
if platform.system()=="Windows":
    directories=[".\enemies",".\items",".\skills"]
else:
    directories=["./enemies","./items",". /skills"]
os.chdir(".\items")
lista_items=os.listdir()

print(lista_items)


