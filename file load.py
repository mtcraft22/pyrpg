import os
import json

lista_items = os.listdir(".\\items")
lista_habilidades = os.listdir(".\\skills")
lista_enemigos = os.listdir(".\\enemies")


class Padre_Items:
    os.chdir(".\\items")
    items_cargados={}
    for i in lista_items:
        with open(i, "r") as co:
            al = json.loads(co.readline())
        items_cargados[i] = al
    os.chdir("..\\")


class Padre_Skills:
    os.chdir(".\\skills")
    items_cargados={}
    for i in lista_items:
        with open(i, "r") as co:
            al = json.loads(co.readline())
        items_cargados[i] = al
    os.chdir("..\\")


class Padre_Enemies:
    os.chdir("\\enemies")
    items_cargados = {}
    for i in lista_items:
        with open(i, "r") as co:
            al = json.loads(co.readline())
        items_cargados[i] = al
    os.chdir("..\\")



for i in Padre_Items.items_cargados:
    print(Padre_Items.items_cargados[i]["cost"])
