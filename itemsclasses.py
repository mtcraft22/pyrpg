import os
from prettytable import PrettyTable

'''aqui se define la bases del juego: propiedades comunes de 
de los items , habilidades e entidades del juego; y los colores 
de escape ansi y otros aspectos generales del juego'''
class pyrpg_master ():
    def __init__(self):
        os.system("color")
        colors={
            "GREEN":'\033[32m',#colores de escape
            "DARKYELLOW" : '\033[33m',
            "YELLOW" : '\033[93m',
            "RED" : '\033[31m',
            "BLUE" : '\033[34m',
            "BOLD" : '\033[1m',
            "CLEAR" : '\033[0m'
        }
    name=""#nombre de item , entidad o habilidad
    description=""#descripcion de item , entidad o habilidad
    e1 = ""#variables de entorno 1-3
    e2 = ""
    e3 = ""
class item(pyrpg_master):#propiedades especificas de los items
    items={}#lista de los items
    cost = 0#cuanto dinero cuesta
    hpr = 0#cuantos ps restaura
    mpr = 0#uantos pm restaura
class skill (pyrpg_master):#propiedades especificas de las habilidades
    skills={}#lista de habilidades
    mpc = 0
    pwr = 0
    element = ""
    heals = False
    level = 0
pyrpg=pyrpg_master()


