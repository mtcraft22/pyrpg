import math
import os, os.path
import sys
from sys import argv
import random
import time
import copy
import json
from prettytable import PrettyTable

import pygame
from pygame.locals import *

class parameters:
	# nombre del juego
	game_name = "PyRPG"
	# mhp inicial, en nivel 1
	initial_mhp = 45
	# incremento de mhp por nivel
	increment_mhp = 5
	# mmp inicial, en nivel 1
	initial_mmp = 9
	# incremento de mmp por nivel
	increment_mmp = 1
	# ataque inicial, en nivel 1
	initial_atk = 32
	# incremento de ataque por nivel
	increment_atk = 8.625
	# defensa inicial, en nivel 1
	initial_def = 20
	# incremento de defensa por nivel
	increment_def = 5
	# magia inicial, en nivel 1
	initial_mat = 8
	# incremento de magia por nivel
	increment_mat = 4.3125
	# velocidad inicial, en nivel 1
	initial_spd = 32
	# incremento de velocidad por nivel
	increment_spd = 8.65625
	# suerte inicial, en nivel 1
	initial_lck = 32
	# incremento de suerte por nivel
	increment_lck = 8.5
	# Parámetros de curva de experiencia
	base_xp = 10
	extra_xp = 2
	accelerator_a = 1
	accelerator_b = 1
	# Parámetros de la fase de descanso
	inn_cost = 10
	# Variables caché
	t_gold = 0
	t_xp = 0
	# Diccionario de debilidades
	weakness = {
		"normal":	("fight"),
		"fight"	:	("flying","psychic","fairy"),
		"flying":	("rock","electric","ice"),
		"poison":	("ground","psychic"),
		"ground":	("water","grass","ice"),
		"rock"	:	("fight","steel","water","grass"),
		"bug"	:	("flying","rock","fire"),
		"ghost"	:	("ghost","dark"),
		"steel"	:	("fight","ground","fire"),
		"fire"	:	("ground","rock","water"),
		"water"	:	("grass","electric"),
		"grass"	:	("flying","poison","bug","fire","ice"),
		"electric":	("ground"),
		"psychic":	("bug","ghost","dark"),
		"ice"	:	("rock","steel","fire"),
		"dragon":	("ice","dragon","fairy"),
		"dark"	:	("fight","bug","fairy"),
		"fairy"	:	("poison","steel")
	}
	# Diccionario de resistencias
	resistances = {
		"normal":	(),
		"fight"	:	("rock","bug","dark"),
		"flying":	("fight","bug","grass"),
		"poison":	("fight","poison","bug","grass","fairy"),
		"ground":	("poison","rock"),
		"rock"	:	("normal","flying","posion","fire"),
		"bug"	:	("fight","ground","grass"),
		"ghost"	:	("poison","bug"),
		"steel"	:	("normal","flying","rock","bug","steel","grass","psychic","ice","dragon","fairy"),
		"fire"	:	("bug","steel","ice"),
		"water"	:	("steel","fire","water","ice"),
		"grass"	:	("ground","water","grass","electric"),
		"electric":	("steel","electric"),
		"psychic":	("fight","psychic"),
		"ice"	:	("ice"),
		"dragon":	("fire","water","grass","electric"),
		"dark"	:	("ghost","dark"),
		"fairy"	:	("fight","bug","dark")
	}
	# Diccionario de inmunidades
	immunities = {
		"normal":	("ghost"),
		"fight"	:	(),
		"flying":	("ground"),
		"poison":	(),
		"ground":	("electric"),
		"rock"	:	(),
		"bug"	:	(),
		"ghost"	:	("normal","fight"),
		"steel"	:	("poison"),
		"fire"	:	(),
		"water"	:	(),
		"grass"	:	(),
		"electric":	(),
		"psychic":	(),
		"ice"	:	(),
		"dragon":	(),
		"dark"	:	("psychic"),
		"fairy"	:	("dragon")
	}

class bcolors:
	GREEN = '\033[32m'
	DARKYELLOW = '\033[33m'
	YELLOW = '\033[93m'
	RED = '\033[31m'
	BLUE = '\033[34m'
	BOLD = '\033[1m'
	CLEAR = '\033[0m'
# Guardar partida
def save_game(filename=""):
	try:
		with open(f"{filename}.json", 'w') as savefile:
			save_dict = {}
			save_dict["name"] = main_player.name
			save_dict["element"] = main_player.element
			save_dict["hp"] = main_player.hp
			save_dict["mp"] = main_player.mp
			save_dict["level"] = main_player.level
			save_dict["gold"] = main_player.gold
			save_dict["xp"] = main_player.xp
			save_dict["floor"] = main_player.floor

			save_items = []
			for i in main_player.items:
				save_items.append(copy.deepcopy(i.__dict__))
			# print(save_items)
			save_dict["items"] = copy.deepcopy(save_items)
			savefile.write(json.dumps(save_dict))
	except:
		print(f"{bcolors.RED}ERROR{bcolors.CLEAR}: Algo salió mal en el intento guardado.")
	else:
		print("Partida guardada con éxito.")
	time.sleep(1)		
	os.system("cls")
# Cargar partida
def load_game(filename=""):
	try:
		with open(f"{filename}", 'r') as savefile:
			json_content = json.loads(savefile.readline())
			p = player()
			p.name = json_content["name"]
			p.element = json_content["element"]
			p.hp = json_content["hp"]
			p.mp = json_content["mp"]
			p.level = json_content["level"]
			p.gold = json_content["gold"]
			p.xp = json_content["xp"]
			p.floor = json_content["floor"]
			for i in json_content["items"]:
				p.items.append(item(i))
			return copy.deepcopy(p)
	except:
		print(f"{bcolors.RED}ERROR{bcolors.CLEAR}: El fichero es inexistente o su contenido no es válido.")
		sys.exit()

def initialize_enemies():
	el = []
	os.chdir('./enemies/')
	for i in os.listdir(f'{os.getcwd()}'):
		if os.path.isfile(i):
			file = open(i,"rt",encoding="UTF-8")
			raw = json.loads(file.read())
			newenemy = enemy(raw)
			el.append(newenemy)
			print(f'Cargado el archivo de datos del enemigo: {i}')
	os.chdir('..')
	return el

def initialize_floor():
	for e in enemy_pool:
		w = e.weight
		# ¿Podrá encontrarse al monstruo?
		if main_player.floor >= e.floor:
			while w >= random.randrange(1,10):
				w -= 10
				enemy_list.append(copy.deepcopy(e))
			#for i in range(e.weight):
			#	enemy_list.append(copy.deepcopy(e))
		random.shuffle(enemy_list)


def initialize_player():
	p = player()
	p.name = ""
	p.element = "normal"
	p.mhp = parameters.initial_mhp
	p.hp = p.mhp
	p.mmp = parameters.initial_mmp
	p.mp = p.mmp
	p.attack = parameters.initial_atk
	p.defense = parameters.initial_def
	p.magic = parameters.initial_mat
	p.speed = parameters.initial_spd
	p.luck = parameters.initial_lck
	return p

def initialize_shop_items():
	si = []
	os.chdir('./items')
	for i in os.listdir(f'{os.getcwd()}'):
		if os.path.isfile(i):
			file = open(i,"rt",encoding="UTF-8")
			raw = json.loads(file.read())
			newitem = item(raw)
			si.append(newitem)
			print(f'Cargado el archivo de datos del objeto: {i}')
	os.chdir('..')
	return si

def initialize_skills():
	sl = []
	os.chdir('./skills')
	for i in os.listdir(f'{os.getcwd()}'):
		if os.path.isfile(i):
			file = open(i,"rt",encoding="UTF-8")
			raw = json.loads(file.read())
			newskill = skill(raw)	
			sl.append(newskill)
			print(f'Cargado el archivo de datos de la habilidad: {i}')
	os.chdir('..')
	return sl

def initialize_states():
	sl = []
	os.chdir('./states')
	for i in os.listdir(f'{os.getcwd()}'):
		if os.path.isfile(i):
			file = open(i,"rt",encoding="UTF-8")
			raw = json.loads(file.read())
			newstate = state(raw)
			sl.append(newstate)
			print(f'Cargado el archivo de datos del estado: {i}')
	os.chdir('..')
	return sl

def update_player_stats(p,r=True):
	p.mhp = math.floor(parameters.increment_mhp * p.level + parameters.initial_mhp)
	p.mmp = math.floor(parameters.increment_mmp * p.level + parameters.initial_mmp)
	if r:
		p.hp += math.floor(parameters.increment_mhp * p.level)
		p.hp = min(p.hp, p.mhp)
		p.mp += math.floor(parameters.increment_mmp * p.level)
		p.mp = min(p.mp, p.mmp)
	p.attack = math.floor(parameters.increment_atk * p.level + parameters.initial_atk)
	p.defense = math.floor(parameters.increment_def * p.level + parameters.initial_def)
	p.magic = math.floor(parameters.increment_mat * p.level + parameters.initial_mat)
	p.speed = math.floor(parameters.increment_spd * p.level + parameters.initial_spd)
	p.luck = math.floor(parameters.increment_lck * p.level + parameters.initial_lck)

# Clase base esencial para cualquier participante en la batalla
class battler():
	name = ""
	element = "normal"
	mhp = 0
	hp = 0
	mmp = 0
	mp = 0
	attack = 0
	defense = 0
	magic = 0
	speed = 0
	luck = 0
	gold = 0
	xp = 0
	temp_xp = 0
	level = 1
	floor = 1
	states = []
	did_attack = False
	# Dibuja una barra de vida.
	# scale: escala de la barra (a mayor valor, más grande será la barra).
	def draw_hp_bar(self,scale):
		print(f"{self.name} [",end="")
		color = bcolors.CLEAR
		p = self.hp/self.mhp
		if (p <= 0.2):
			color = bcolors.RED
		elif (p <= 0.5 and p > 0.2):
			color = bcolors.DARKYELLOW
		elif (p > 0.5):
			color = bcolors.GREEN
		for i in range(max(math.ceil(p*scale), 0)):
			print(color+"█", end=bcolors.CLEAR)
		for i in range(max(math.floor(scale-p*scale), 0)):
			print(" ",end="")
		print("] ",end="")
		print(f"{self.hp}/{self.mhp} PS\n")
	# Dibuja una barra de magia.
	# scale: escala de la barra (a mayor valor, más grande será la barra).
	def draw_mp_bar(self,scale):
		if self.mmp <= 0:
			return
		for i in range(len(self.name) + 1):
			print(" ", end="")
		print("[",end="")
		color = bcolors.BLUE
		p = self.mp/self.mmp
		for i in range(max(math.ceil(p*scale), 0)):
			print(color+"█", end=bcolors.CLEAR)
		for i in range(max(math.floor(scale-p*scale), 0)):
			print(" ",end="")
		print("] ",end="")
		print(f"{self.mp}/{self.mmp} PM\n")
		

# Clase del jugador
class player(battler):
	items = []
	def __init__(self):		
		name = ""
		element = "normal"
		self.mhp = parameters.initial_mhp
		self.hp = self.mhp
		self.mmp = parameters.initial_mmp
		self.mp = self.mmp
		self.attack = parameters.initial_atk
		self.defense = parameters.initial_def
		self.magic = parameters.initial_mat
		self.speed = parameters.initial_spd
		self.luck = parameters.initial_lck
		self.gold = 0
		self.xp = 0
		self.level = 1
		self.floor = 1

# Clase del enemigo
class enemy(battler):
	def __init__(self, d):
		self.name = d["name"]
		self.element = d["element"]
		self.mhp = d["mhp"]
		self.hp = d["mhp"]
		self.mmp = d["mmp"]
		self.mp = d["mmp"]
		self.attack = d["atk"]
		self.defense = d["def"]
		self.magic = d["mat"]
		self.speed = d["spd"]
		self.luck = d["lck"]
		self.gold = d["gold"]
		self.xp = d["xp"]
		self.weight = d["weight"]
		self.floor = d["floor"]
		self.skills = d["skills"]
		self.max_encounters = d["max_encounters"]

class skill:
	def __init__(self, d):
		self.name = d["name"]
		self.description = d["description"]
		self.mpc = d["mpc"]
		self.pwr = d["pwr"] // 10
		self.element = d["element"]
		self.heals = d["heals"]
		self.level = d["level"] # set it to -1 if the skill cannot be learnt by the player (i.e., enemy/boss unique skills).
		self.effects = d["effects"]

class item:
	def __init__(self, d):
		self.name = d["name"]
		self.description = d["description"]
		self.cost = d["cost"]
		self.hpr = d["hpr"]
		self.mpr = d["mpr"]
		self.effects = d["effects"]

class state:
	def __init__(self, d):
		self.name = d["name"]
		self.display_name = d["display-name"]
		self.description = d["description"]
		self.restrictions = d["restrictions"]
		self.effects = d["effects"]
		self.messages = d["messages"]
		self.health_color = d["health-color"]

battlers = []

def deal_damage(t, d):
	t.hp -= d

def perform_attack(attacker, target):
	print(f"¡{attacker.name} ataca a {target.name}!\n")
	damage = max(attacker.attack - target.defense, 1)
	deal_damage(target, damage)
	print(f"¡{target.name} recibió {damage} puntos de daño!")
	target.draw_hp_bar(10)
	target.draw_mp_bar(10)
	if (target.hp > 0):
		# Sigue vivo
		pass
	else:
		# Enemigo derrotado
		print(f"¡{target.name} ha sido asesinado!")
		if target in current_enemies:			
			parameters.t_gold += target.gold
			parameters.t_xp += target.xp
			current_enemies.remove(target)

def cast_skill(caster, skill, target):
	print(f"¡{caster.name} usa {bcolors.YELLOW + skill.name + bcolors.CLEAR}!")
	if caster == main_player:
		caster.mp -= skill.mpc
		caster.draw_mp_bar(10)
	m = 1
	# print(f"{skill.element} VS {target.element}")
	if skill.element in parameters.weakness[target.element]:
		print("¡Es muy eficaz!")
		m *= 2
	if skill.element in parameters.resistances[target.element]:
		print("No es muy eficaz...")
		m /= 2
	if skill.element in parameters.immunities[target.element]:
		print(f"No afecta a {target.name}...")
		m *= 0
	damage = int(skill.pwr * caster.magic * m)
	deal_damage(target, damage)
	if damage > 0:
		print(f"¡{target.name} recibió {damage} puntos de daño!")
		target.draw_hp_bar(10)
	for s in skill.effects:
		if s["chance"] >= random.random() * 100:
			apply_state(target, s)
	if (target.hp > 0):
		# Sigue vivo
		pass
	else:
		# Enemigo derrotado
		print(f"¡{target.name} ha sido asesinado!")
		if target in current_enemies:			
			parameters.t_gold += target.gold
			parameters.t_xp += target.xp
			current_enemies.remove(target)

def apply_state(target, state):
	if state in target.states:
		# No se aplicará el estado si el objetivo ya lo posee.
		# TODO: Mecánica de 'stacking' de estados.
		return
	state_ref = get_state_by_name(state["name"])
	target.states.append(state_ref)
	for m in state_ref.messages:
		if m["name"] == "battler-got-effect":
			base_message = m["message"]
			print(base_message.replace("{0}", target.name))
			break

def apply_effect(t, e, m):
	if e["name"] == "health-damage":
		d = e["value"]
		if e["relative"]:
			d = t.mhp * d // 100
		deal_damage(t, d)
		print(m.replace("{0}", t.name))
		t.draw_hp_bar(10)
	if e["name"] == "cannot-attack":
		t.did_attack = True
		print(m.replace("{0}", t.name))


def get_skill_by_name(name):
	for s in skill_list:
		if s.name == name:
			return s
	return None

def get_state_by_name(name):
	for s in state_list:
		if s.name == name:
			return s
	return None

def check_level():
	if (main_player.xp >= parameters.base_xp * math.pow(main_player.level, parameters.accelerator_a + parameters.accelerator_b) + math.pow(main_player.level - 1, parameters.extra_xp)):
		main_player.temp_xp = main_player.xp
		main_player.xp -= (main_player.xp >= parameters.base_xp * math.pow(main_player.level, parameters.accelerator_a + parameters.accelerator_b) + math.pow(main_player.level - 1, parameters.extra_xp))
		main_player.level += 1
		print(f"¡Subiste de nivel! Ahora eres nivel {main_player.level}.")
		update_player_stats(main_player)
		for s in skill_list:
			if main_player.level == s.level:
				print(f"¡Has aprendido {s.name}!")

def recover_hp(target,amount):
	target.hp = min(target.hp + amount, target.mhp)

def recover_mp(target,amount):
	target.mp = min(target.mp + amount, target.mmp)

def do_enemy_turn(enemy):
	if enemy.did_attack:
		return
	# Turno del enemigo
	print(f"[Turno de {enemy.name}]")
	enemy.did_attack = True
	for s in enemy.skills:
		if s["weight"] > random.random() * 100:
			cast_skill(enemy, get_skill_by_name(s["name"]), main_player)
			return
	perform_attack(enemy, main_player)

current_enemies = []

def start_battle_loop():
	initialize_floor()
	print(f"[PISO {main_player.floor}]")
	while len(enemy_list) > 0:
		random.shuffle(enemy_list)
		main_enemy = enemy_list[0]
		for i in range(0, random.randint(1, main_enemy.max_encounters)):
			enemy = copy.deepcopy(main_enemy)
			enemy.name = enemy.name + " " + chr(ord('A') + i)
			current_enemies.append(enemy)
		if len(current_enemies) > 1:
			print("¡Varios enemigos aparecieron!")
			for e in current_enemies:
				e.draw_hp_bar(10)
		else:
			print(f"¡{main_enemy.name} apareció!")
			current_enemies[0].draw_hp_bar(10)
		time.sleep(1)
		while main_player.hp > 0:
			# El enemigo atacará antes si es más veloz que el jugador.
			for e in current_enemies:
				if e.speed > main_player.speed:
					do_enemy_turn(e)
			if main_player.hp <= 0:
				break
			# Turno del jugador
			print(f"[Turno de {main_player.name}]")
			print(f"{bcolors.YELLOW}¿Qué desea hacer?{bcolors.CLEAR}")
			print("1. Atacar")
			print("2. Habilidad")
			# print("3. Defender")
			print("4. Objeto")
			opcion = input("Elige [1-4]: ")
			if opcion == "1":
				print("Selecciona un objetivo: ")
				i = 0
				for e in current_enemies:
					i += 1
					print(f"{i} > ", end="")
					e.draw_hp_bar(10)
				try:
					target = input(f"Elige [1-{i}] (o 0 para cancelar): ")
					if target == "0":
						continue
					perform_attack(main_player, current_enemies[int(target) - 1])
				except:
					print(bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + bcolors.CLEAR)
					continue
			elif opcion == "2":
				# Menú de habilidad
				table = PrettyTable()
				table.field_names = ["Nº","Nombre","Descripción","Coste"]
				i = 0
				player_skill_list = []			
				for s in skill_list:
					# Si la habilidad es propia de los monstruos, no será incluido en la lista de habilidades.
					if main_player.level >= s.level and s.level != -1:
						player_skill_list.append(copy.deepcopy(s))
				if len(player_skill_list) > 0:
					for s in player_skill_list:
						i += 1
						table.add_row([i, s.name, s.description, str(s.mpc) + " PM"])
					print(table)
					try:
						opcion2 = input(f"Selecciona una habilidad [1-{i}] (o 0 para cancelar): ")
						if opcion2 == "0":
							continue
						if int(opcion2) - 1 > i:
							print(bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + bcolors.CLEAR)
							continue
						selected_skill = player_skill_list[int(opcion2) - 1]
						if main_player.mp >= selected_skill.mpc:
							print("Selecciona un objetivo: ")
							i = 0
							for e in current_enemies:
								i += 1
								print(f"{i} > ", end="")
								e.draw_hp_bar(10)
							try:
								target = input(f"Elige [1-{i}] (o 0 para cancelar): ")
								if target == "0":
									continue
								cast_skill(main_player, selected_skill, current_enemies[int(target) - 1])
							except:
								print(bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + bcolors.CLEAR)
								continue
						else:
							print(bcolors.RED + "PM Insuficientes.\n" + bcolors.CLEAR)
							continue
					except:
						print(bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + bcolors.CLEAR)
						continue
				else:
					print("No has aprendido ninguna habilidad.")
					continue
			elif opcion == "4":
				# Menú de objeto
				table = PrettyTable()
				table.field_names = ["Nº","Nombre","Descripción"]
				i = 0
				if len(main_player.items) > 0:
					for e in main_player.items:
						i += 1
						table.add_row([i, e.name, e.description])
					print(table)
					try:
						opcion2 = input(f"Selecciona un objeto [1-{i}] (o 0 para cancelar): ")
						if opcion2 == "0":
							continue
						if int(opcion2) - 1 > len(main_player.items):
							print(bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + bcolors.CLEAR)
							continue
						selected_item = main_player.items[int(opcion2) - 1]
						print(f"¡{main_player.name} usa {selected_item.name}!")
						if selected_item.hpr > 0:
							recover_hp(main_player, selected_item.hpr)
							print(f"¡{main_player.name} recupera {selected_item.hpr} PS!")
							main_player.draw_hp_bar(10)
						if selected_item.mpr > 0:
							recover_mp(main_player, selected_item.mpr)
							print(f"¡{main_player.name} recupera {selected_item.mpr} PM!")
						main_player.items.pop(int(opcion2) - 1)
					except TypeError:
						print(bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + bcolors.CLEAR)
						continue
				else:
					print("No tienes objetos.")
					continue
			else:
				print(bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + bcolors.CLEAR)
				continue
			# Si el jugador tiene algún estado de fin de turno, se le aplicará.
			for s in main_player.states:
				for e in s.effects:
					if e["lapse"] == "after-turn":
						base_message = ""
						for m in s.messages:
							if m["name"] == "effect-persists":
								base_message = m["message"]
								break
						apply_effect(main_player, e, base_message)
			if (len(current_enemies) == 0):
				break
			# El enemigo atacará después si es más lento que el jugador.
			for e in current_enemies:
				if e.speed <= main_player.speed:
					do_enemy_turn(e)
				e.did_attack = False
		if (main_player.hp > 0):
			print(f"¡Ganaste! Recibes {parameters.t_gold} oro y {parameters.t_xp} PE.\n")
			main_player.gold += parameters.t_gold
			main_player.xp += parameters.t_xp
			parameters.t_gold = 0
			parameters.t_xp = 0
			enemy_list.pop(0)
			check_level()
			os.system("pause")
			os.system("cls")
		else:
			print(bcolors.RED)
			print("===========================")
			print("=====FIN DE LA PARTIDA=====")
			print("===========================")
			print(bcolors.CLEAR)
			time.sleep(1)
			sys.exit()
	print(f"=====¡PISO {main_player.floor} COMPLETADO!=====\n")
	main_player.floor += 1

def break_time_loop():
	print("Atisbaste un campamento. Sin pensarlo, entraste a la posada.")
	print(f"{bcolors.YELLOW}Posadero Pepito{bcolors.CLEAR}: ¡Bienvenido a la posada! ¿Qué te trae por aquí?")
	while True:
		# Bucle del campamento
		print("1. Continuar la exploración")
		print("2. Pasar la noche")
		print("3. Ir a la tienda")
		print("4. Realizar chequeo")
		print("5. Guardar")
		print("9. Salir del juego")
		opcion = input("Elige [1-5 o 9]: ")
		print("")
		if opcion == "1":
			print(f"{bcolors.YELLOW}Posadero Pepito{bcolors.CLEAR}: Si abandonas la posada, no podrás volver a menos que venzas a todos los monstruos antes de volver. ¿Estás seguro?")
			confirmacion = input("Elige [s/N]: ")
			if (confirmacion == "s" or confirmacion == "S"):
				print(f"{bcolors.YELLOW}Posadero Pepito{bcolors.CLEAR}: Ya veo. En ese caso, ¡cuídate!")
				os.system("pause")
				os.system("cls")
				break
			else:
				continue
		elif opcion == "2":
			print(f"{bcolors.YELLOW}Posadero Pepito{bcolors.CLEAR}: Serán {parameters.inn_cost} monedas de oro. ¿Quieres pasar la noche aquí?")
			confirmacion = input("Elige [s/N]: ")
			if (confirmacion == "s" or confirmacion == "S"):
				if (main_player.gold >= parameters.inn_cost):
					main_player.gold -= parameters.inn_cost
					print("Descansando...\n")
					time.sleep(2)
					recover_hp(main_player, 9999)
					recover_mp(main_player, 9999)
					print("Te sientes lleno de energía.")
					os.system("pause")
					os.system("cls")
				else:
					print(f"{bcolors.YELLOW}Posadero Pepito{bcolors.CLEAR}: Hmm... Me parece que no tienes suficiente dinero. Vuelve cuando tengas más.")
					os.system("pause")
					os.system("cls")
			else:
				continue
		elif opcion == "3":
			while True:
				# Bucle de la tienda
				
				print(f"{bcolors.YELLOW}Tendero José{bcolors.CLEAR}: ¡Hola! ¿En que puedo ayudarle?")
				print(f"Dinero disponible: {main_player.gold}")
				print("1. Comprar")
				# TODO: posibilidad de vender un objeto que no necesites.
				# print("2. Vender")
				print("3. Salir")
				opcion2 = input("Elige [1-3]: ")
				if opcion2 == "1":
					while True:
						table = PrettyTable()
						table.field_names = ["Nº","Nombre","Precio","Descripción"]
						i = 0
						for e in shop_item_list:
							i += 1
							table.add_row([i, e.name, e.cost, e.description])
						print(table)
						try:
							opcion3 = input(f"Elige [1-{i}] (o 0 para cancelar): ")
							if opcion3 == "0":
								break
							if int(opcion3) > i:
								print(bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + bcolors.CLEAR)
								continue
							selected_item = shop_item_list[int(opcion3)-1]
							print(f"¿Quieres comprar {selected_item.name} por {selected_item.cost} monedas de oro?")
							confirmacion = input("Elige [s/N]: ")
							if (confirmacion == "s" or confirmacion == "S"):
								if (main_player.gold >= selected_item.cost):
									main_player.gold -= selected_item.cost
									main_player.items.append(selected_item)
									print(f"¡Compraste {selected_item.name}!")
									print(f"Dinero disponible: {main_player.gold}")
								else:
									print(f"{bcolors.YELLOW}Tendero José{bcolors.CLEAR}: Hmm... Me parece que no tienes suficiente dinero. Vuelve cuando tengas más.")
									os.system("pause")
									os.system("cls")
							else:
								continue
						except:
							print(bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + bcolors.CLEAR)
				elif opcion2 == "3":
					print(f"{bcolors.YELLOW}Tendero José{bcolors.CLEAR}: ¡Gracias por su compra!")
					os.system("pause")
					os.system("cls")
					break
		elif opcion == "5":
			save_game(parameters.game_name)
			continue
		elif (opcion == "9"):
			print(f"{bcolors.RED}ATENCIÓN{bcolors.CLEAR}: Cualquier dato no guardado se perderá. ¿Salir de {parameters.game_name}?")
			confirmacion = input("Elige [s/N]: ")
			if (confirmacion == "s" or confirmacion == "S"):
				os.system("cls")
				sys.exit()
			else:
				continue
		else:
			print(bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + bcolors.CLEAR)
			continue
		print(f"{bcolors.YELLOW}Posadero Pepito{bcolors.CLEAR}: ¡Hola, viajero!")

def start_game(save_file):
	game_started = True
	if save_file is not None:
		update_player_stats(main_player,r=False)
		print(f"¡Bienvenido de nuevo, {main_player.name}!\n")
		print(f"Nivel {main_player.level}")
		print(f"{main_player.gold} Oro")
		print(f"Piso {main_player.floor}\n")
		i = input("¿Eres tú? [s/N]: ").lower()
		if i == "s":
			print(f"Reanudando partida como {main_player.name}...")
			time.sleep(2)
			os.system("cls")
			while True:
				break_time_loop()
				start_battle_loop()
		else:
			sys.exit()
			return
	else:
		# Aquí pedimos un nombre para el personaje
		print(f"¡Bienvenido a {parameters.game_name}!")
		name = input("Introduce tu nombre: ")
		main_player.name = name
		print(f"Empezando partida como {name}...\n")
		# ¡Empieza el juego!
		while True:
			start_battle_loop()
			break_time_loop()

pygame.init()

print(bcolors.CLEAR)
random.seed()

game_started = False
enemy_pool = []

enemy_pool = initialize_enemies()

enemy_list = []
shop_item_list = initialize_shop_items()

skill_list = initialize_skills()

state_list = initialize_states()

# Limpiamos la pantalla y empezamos una partida nueva.
time.sleep(1)
os.system("cls")
if len(argv) > 1:
	main_player = load_game(argv[1])
	start_game(argv[1])
else:
	main_player = player()
	start_game(None)