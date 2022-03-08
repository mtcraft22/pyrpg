import copy
import math
import os
import os.path
import random
import sys
import time
'''
import os
import time
import win32api
'''a = 0
l1 = []

while a < 10:
    os.system("cls")
    l1.append("█")
    print("".join(l1))
    a += 1
    time.sleep(1)'''
while True:
    a = win32api.GetKeyState(0x25)
    aa = win32api.GetKeyState(0x27)
    if a < 0:
        print("viva phyton")
    elif aa < 0:
        print("viva phyton2")
    time.sleep(0.1)'''

''' pip install pywin32'''
from prettytable import PrettyTable


class Parameters:
	# nombre del juego
	game_name = "PyRPG"
	# mhp inicial, en nivel 1
	initial_mhp = 10
	# incremento de mhp por nivel
	increment_mhp = 1.3
	# mmp inicial, en nivel 1
	initial_mmp = 7
	# incremento de mmp por nivel
	increment_mmp = 1.0
	# ataque inicial, en nivel 1
	initial_atk = 5
	# incremento de ataque por nivel
	increment_atk = 1.2
	# defensa inicial, en nivel 1
	initial_def = 2
	# incremento de defensa por nivel
	increment_def = 0.8
	# magia inicial, en nivel 1
	initial_mat = 4
	# incremento de magia por nivel
	increment_mat = 0.7
	# velocidad inicial, en nivel 1
	initial_spd = 4
	# incremento de velocidad por nivel
	increment_spd = 0.9
	# suerte inicial, en nivel 1
	initial_lck = 2
	# incremento de suerte por nivel
	increment_lck = 0.6
	# Parámetros de curva de experiencia
	base_xp = 10
	extra_xp = 2
	accetr_a = 1
	accetr_b = 1
	# Parámetros de la fase de descanso
	inn_cost = 10
	# Diccionario de debilidades
	weakness = {
		"normal":	"fight",
		"fight"	:	("flying", "psychic", "fairy"),
		"flying":	("rock", "electric", "ice"),
		"poison":	("ground", "psychic"),
		"ground":	("water", "grass", "ice"),
		"rock"	:	("fight", "steel", "water", "grass"),
		"bug"	:	("flying", "rock", "fire"),
		"ghost"	:	("ghost", "dark"),
		"steel"	:	("fight", "ground", "fire"),
		"fire"	:	("ground", "rock", "water"),
		"water"	:	("grass", "electric"),
		"grass"	:	("flying", "poison", "bug", "fire", "ice"),
		"electric":	"ground",
		"psychic":	("bug", "ghost", "dark"),
		"ice"	:	("rock", "steel", "fire"),
		"dragon":	("ice", "dragon", "fairy"),
		"dark"	:	("fight", "bug", "fairy"),
		"fairy"	:	("poison", "steel")
	}
	# Diccionario de resistencias
	resistances = {
		"normal":	(),
		"fight"	:	("rock", "bug", "dark"),
		"flying":	("fight", "bug", "grass"),
		"poison":	("fight", "poison", "bug", "grass", "fairy"),
		"ground":	("poison", "rock"),
		"rock"	:	("normal", "flying", "poison", "fire"),
		"bug"	:	("fight", "ground", "grass"),
		"ghost"	:	("poison", "bug"),
		"steel"	:	("normal", "flying", "rock", "bug", "steel", "grass", "psychic", "ice", "dragon", "fairy"),
		"fire"	:	("bug", "steel", "ice"),
		"water"	:	("steel", "fire", "water", "ice"),
		"grass"	:	("ground", "water", "grass", "electric"),
		"electric":	("ground", "steel", "electric"),
		"psychic":	("fight", "psychic"),
		"ice"	:	"ice",
		"dragon":	("fire", "water", "grass", "electric"),
		"dark"	:	("ghost", "dark"),
		"fairy"	:	("fight", "bug", "dark")
	}
	# Diccionario de inmunidades
	immunities = {
		"normal":	"ghost",
		"fight"	:	(),
		"flying":	"ground",
		"poison":	(),
		"ground":	"electric",
		"rock"	:	(),
		"bug"	:	(),
		"ghost"	:	("normal", "fight"),
		"steel"	:	"poison",
		"fire"	:	(),
		"water"	:	(),
		"grass"	:	(),
		"electric":	(),
		"psychic":	(),
		"ice"	:	(),
		"dragon":	(),
		"dark"	:	"psychic",
		"fairy"	:	"dragon"
	}


class Bcolors:  # implementado todos los colores
	GREEN = '\033[32m'
	DARK_YELLOW = '\033[33m'
	YELLOW = '\033[93m'
	RED = '\033[31m'
	BLUE = '\033[34m'
	BOLD = '\033[1m'
	CLEAR = '\033[0m'


def initialize_enemies():
	el = []
	os.chdir('./enemies')
	for i in os.listdir(f'{os.getcwd()}'):
		file = open(i, "rt")
		new_enemy = Enemy()
		for x in file.readlines():
			line = x
			k = line.split("=")[0]
			v = line.split("=")[1]

			if k == "name":
				new_enemy.name = v.rstrip("\n")
			elif k == "element":
				new_enemy.element = v.rstrip("\n")
			elif k == "mhp":
				new_enemy.mhp = int(v)
				new_enemy.hp = int(v)
			elif k == "mmp":
				new_enemy.mmp = int(v)
				new_enemy.mp = int(v)
			elif k == "atk":
				new_enemy.attack = int(v)
			elif k == "def":
				new_enemy.defense = int(v)
			elif k == "mat":
				new_enemy.magic = int(v)
			elif k == "spd":
				new_enemy.spd = int(v)
			elif k == "lck":
				new_enemy.lck = int(v)
			elif k == "gold":
				new_enemy.gold = int(v)
			elif k == "xp":
				new_enemy.xp = int(v)
			elif k == "weight":
				new_enemy.weight = int(v)
			elif k == "floor":
				new_enemy.floor = int(v)
		el.append(new_enemy)
		print(f'Cargado el archivo de datos del enemigo: {i}')
	os.chdir('..')
	return el


def initialize_floor():
	for e in enemy_pool:
		w = e.weight
		# ¿Podrá encontrarse al monstruo?
		if main_player.floor >= e.floor:
			while w >= random.randrange(1, 10):
				w -= 10
				enemy_list.append(copy.deepcopy(e))
			# for i in range(e.weight):
			# enemy_list.append(copy.deepcopy(e))
		random.shuffle(enemy_list)


def initialize_player():
	p = Player()
	p.name = ""
	p.mhp = 10
	p.hp = 10
	p.mmp = 7
	p.mp = 7
	p.attack = 5
	p.defense = 2
	p.magic = 3
	p.speed = 4
	p.luck = 2
	return p


def initialize_shop_items():
	si = []
	os.chdir('./items')
	for i in os.listdir(f'{os.getcwd()}'):
		file = open(i, "rt")
		new_item = Item()
		for x in file.readlines():
			line = x
			k = line.split("=")[0]
			v = line.split("=")[1]

			if k == "name":
				new_item.name = v.rstrip("\n")
			elif k == "description":
				new_item.description = v.rstrip("\n")
			elif k == "cost":
				new_item.cost = int(v)
			elif k == "hpr":
				new_item.hpr = int(v)
			elif k == "mpr":
				new_item.mpr = int(v)
			elif k == "e1":
				new_item.e1 = v.rstrip("\n")
			elif k == "e2":
				new_item.e2 = v.rstrip("\n")
			elif k == "e3":
				new_item.e3 = v.rstrip("\n")
		si.append(new_item)
		print(f'Cargado el archivo de datos del objeto: {i}')
	os.chdir('..')
	return si


def initialize_skills():
	sl = []
	os.chdir('./skills')
	for i in os.listdir(f'{os.getcwd()}'):
		file = open(i, "rt")
		new_skill = Skill()
		for x in file.readlines():
			line = x
			k = line.split("=")[0]
			v = line.split("=")[1]

			if k == "name":
				new_skill.name = v.rstrip("\n")
			elif k == "description":
				new_skill.description = v.rstrip("\n")
			elif k == "mpc":
				new_skill.mpc = int(v)
			elif k == "pwr":
				new_skill.pwr = int(v) // 10
			elif k == "element":
				new_skill.element = v.rstrip("\n")
			elif k == "heals":
				new_skill.heals = v.lower() == "true"
			elif k == "level":
				new_skill.level = int(v)
			elif k == "e1":
				new_skill.e1 = v.rstrip("\n")
			elif k == "e2":
				new_skill.e2 = v.rstrip("\n")
			elif k == "e3":
				new_skill.e3 = v.rstrip("\n")
		sl.append(new_skill)
		print(f'Cargado el archivo de datos de la habilidad: {i}')
	os.chdir('..')
	return sl


def update_player_stats():
	main_player.mhp = math.floor(Parameters.increment_mhp * main_player.level + Parameters.initial_mhp)
	main_player.hp += math.floor(Parameters.increment_mhp * main_player.level)
	main_player.mmp = math.floor(Parameters.increment_mmp * main_player.level + Parameters.initial_mmp)
	main_player.mp += math.floor(Parameters.increment_mmp * main_player.level)
	main_player.attack = math.floor(Parameters.increment_atk * main_player.level + Parameters.initial_atk)
	main_player.defense = math.floor(Parameters.increment_def * main_player.level + Parameters.initial_def)
	main_player.magic = math.floor(Parameters.increment_mat * main_player.level + Parameters.initial_mat)
	main_player.speed = math.floor(Parameters.increment_spd * main_player.level + Parameters.initial_spd)
	main_player.luck = math.floor(Parameters.increment_lck * main_player.level + Parameters.initial_lck)

# Clase base esencial para cualquier participante en la batalla


class Battler:
	name = ""
	element = ""
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
	weight = 0
	floor = 1
	# Dibuja una barra de vida.
	# scale: escala de la barra (a menor valor, más grande será la barra).

	def draw_hp_bar(self, scale):
		print(f"{self.name} [", end="")
		color = Bcolors.CLEAR
		p = self.hp/self.mhp
		if p <= 0.2:
			color = Bcolors.RED
		elif 0.5 >= p > 0.2:
			color = Bcolors.DARK_YELLOW
		elif p > 0.5:
			color = Bcolors.GREEN
		for i in range(max(math.ceil(self.hp/scale), 0)):
			print(color+"█", end=Bcolors.CLEAR)
		for i in range(max(math.floor((self.mhp-self.hp)/scale), 0)):
			print(" ", end="")
		print("] ", end="")
		print(f"{self.hp}/{self.mhp} PS\n")
	# Dibuja una barra de magia.
	# scale: escala de la barra (a menor valor, más grande será la barra).

	def draw_mp_bar(self, scale):
		if self.mmp <= 0:
			return
		for i in range(len(self.name) + 1):
			print(" ", end="")
		print("[", end="")
		color = Bcolors.BLUE
		for i in range(max(math.ceil(self.mp/scale), 0)):
			print(color+"█", end=Bcolors.CLEAR)
		for i in range(max(math.floor((self.mmp-self.mp)/scale), 0)):
			print(" ", end="")
		print("] ", end="")
		print(f"{self.mp}/{self.mmp} PM\n")
		

# Clase del jugador

class Player(Battler):
	items = []

# Clase del enemigo


class Enemy(Battler):
	pass


class Skill:
	name = ""  # implementado
	description = ""  # implementado
	mpc = 0  # implementado
	pwr = 0  # implementado
	element = ""  # implementado
	heals = False  # implementado
	level = 0  # implementado
	e1 = ""  # implementado
	e2 = ""  # implementado
	e3 = ""  # implementado


class Item:
	name = ""  # implementado
	description = ""  # implementado
	cost = 0  # implementado
	hpr = 0  # implementado
	mpr = 0  # implementado
	e1 = ""  # implementado
	e2 = ""  # iplementado
	e3 = ""  # implementado


battlers = []


def perform_attack(attacker, target):
	print(f"¡{attacker.name} ataca a {target.name}!\n")
	damage = max(attacker.attack - target.defense, 1)
	target.hp -= damage
	print(f"¡{target.name} recibió {damage} puntos de daño!")
	target.draw_hp_bar(1)
	target.draw_mp_bar(1)
	if target.hp > 0:
		# Sigue vivo
		pass
	else:
		# Enemigo derrotado
		print(f"¡{target.name} ha sido asesinado!")


def cast_skill(caster, skill, target):
	print(f"¡{caster.name} lanza {skill.name}!")
	caster.mp -= skill.mpc
	caster.draw_mp_bar(1)
	m = 1
	print(f"{skill.element} VS {target.element}")
	if skill.element in Parameters.weakness[target.element]:
		print("¡Es muy eficaz!")
		m *= 2
	if skill.element in Parameters.resistances[target.element]:
		print("No es muy eficaz...")
		m /= 2
	if skill.element in Parameters.immunities[target.element]:
		print(f"No afecta a {target.name}...")
		m *= 0
	damage = int(skill.pwr * caster.magic * m)
	target.hp -= damage
	if damage > 0:
		print(f"¡{target.name} recibió {damage} puntos de daño!")
		target.draw_hp_bar(1)
	if target.hp > 0:
		# Sigue vivo
		pass
	else:
		# Enemigo derrotado
		print(f"¡{target.name} ha sido asesinado!")


def check_level():
	if main_player.xp >= Parameters.base_xp * math.pow(main_player.level, Parameters.accetr_a + Parameters.accetr_b) + math.pow(main_player.level - 1, Parameters.extra_xp):
		main_player.temp_xp = main_player.xp
		main_player.xp -= (main_player.xp >= Parameters.base_xp * math.pow(main_player.level, Parameters.accetr_a + Parameters.accetr_b) + math.pow(main_player.level - 1, Parameters.extra_xp))
		main_player.level += 1
		print(f"¡Subiste de nivel! Ahora eres nivel {main_player.level}.")
		update_player_stats()
		for s in skill_list:
			if main_player.level == s.level:
				print(f"¡Has aprendido {s.name}!")


def recover_hp(target, amount):
	target.hp = min(target.hp + amount, target.mhp)


def recover_mp(target, amount):
	target.mp = min(target.mp + amount, target.mmp)


def start_battle_loop():
	initialize_floor()
	print(f"[PISO {main_player.floor}]")
	while len(enemy_list) > 0:
		random.shuffle(enemy_list)
		main_enemy = enemy_list[0]
		print(f"¡Un {main_enemy.name} te ataca!")
		main_enemy.draw_hp_bar(1)
		while main_player.hp > 0:
			# Turno del jugador
			print(f"[Turno de {main_player.name}]")
			print(f"{Bcolors.YELLOW}¿Qué desea hacer?{Bcolors.CLEAR}")
			print("1. Atacar")
			print("2. Habilidad")
			# print("3. Defender")
			print("4. Objeto")
			opcion = input("Elige [1-4]: ")
			if opcion == "1":
				perform_attack(main_player, main_enemy)
			elif opcion == "2":
				# Menú de habilidad
				table = PrettyTable()
				table.field_names = ["Nº", "Nombre", "Descripción", "Coste"]
				i = 0
				player_skill_list = []			
				for s in skill_list:
					if main_player.level >= s.level:
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
							print(Bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + Bcolors.CLEAR)
							continue
						selected_skill = player_skill_list[int(opcion2) - 1]
						if main_player.mp >= selected_skill.mpc:
							cast_skill(main_player, selected_skill, main_enemy)
						else:
							print(Bcolors.RED + "PM Insuficientes.\n" + Bcolors.CLEAR)
							continue
					except:
						print(Bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + Bcolors.CLEAR)
				else:
					print("No has aprendido ninguna habilidad.")
					continue
			elif opcion == "4":
				# Menú de objeto
				table = PrettyTable()
				table.field_names = ["Nº", "Nombre", "Descripción"]
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
							print(Bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + Bcolors.CLEAR)
							continue
						selected_item = main_player.items[int(opcion2) - 1]
						print(f"¡{main_player.name} usa {selected_item.name}!")
						if selected_item.hpr > 0:
							recover_hp(main_player, selected_item.hpr)
							print(f"¡{main_player.name} recupera {selected_item.hpr} PS!")
							main_player.draw_hp_bar(1)
						if selected_item.mpr > 0:
							recover_mp(main_player, selected_item.mpr)
							print(f"¡{main_player.name} recupera {selected_item.hpr} PM!")
						main_player.items.pop(int(opcion2) - 1)
					except:
						print(Bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + Bcolors.CLEAR)
				else:
					print("No tienes objetos.")
					continue
			else:
				print(Bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + Bcolors.CLEAR)
				continue
			if main_enemy.hp <= 0:
				break
			# Turno del enemigo
			print(f"[Turno de {main_enemy.name}]")
			perform_attack(main_enemy, main_player)
		if main_player.hp > 0:
			print(f"¡Ganaste! Recibes {main_enemy.gold} oro y {main_enemy.xp} PE.\n")
			main_player.gold += main_enemy.gold
			main_player.xp += main_enemy.xp
			enemy_list.pop(0)
			check_level()
			os.system("pause")
			os.system("cls")
		else:
			print(Bcolors.RED)
			print("===========================")
			print("=====FIN DE LA PARTIDA=====")
			print("===========================")
			print(Bcolors.CLEAR)
			time.sleep(1)
			sys.exit()
	print(f"=====¡PISO {main_player.floor} COMPLETADO!=====\n")
	main_player.floor += 1


def break_time_loop():
	print("Atisbaste un campamento. Sin pensarlo, entraste a la posada.")
	print(f"{Bcolors.YELLOW}Posadero Pepito{Bcolors.CLEAR}: ¡Bienvenido a la posada! ¿Qué te trae por aquí?")
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
			print(f"{Bcolors.YELLOW}Posadero Pepito{Bcolors.CLEAR}: Si abandonas la posada, no podrás volver a menos que venzas a todos los monstruos antes de volver. ¿Estás seguro?")
			confirmacion = input("Elige [s/N]: ")
			if confirmacion == "s" or confirmacion == "S":
				print(f"{Bcolors.YELLOW} Posadero Pepito{Bcolors.CLEAR}: Ya veo. En ese caso, ¡cuídate!")
				os.system("pause")
				os.system("cls")
				break
			else:
				continue
		elif opcion == "2":
			print(f"{Bcolors.YELLOW}Posadero Pepito{Bcolors.CLEAR}: Serán {Parameters.inn_cost} monedas de oro. ¿Quieres pasar la noche aquí?")
			confirmacion = input("Elige [s/N]: ")
			if confirmacion == "s" or confirmacion == "S":
				if main_player.gold >= Parameters.inn_cost:
					main_player.gold -= Parameters.inn_cost
					print("Descansando...\n")
					time.sleep(2)
					recover_hp(main_player, 9999)
					recover_mp(main_player, 9999)
					print("Te sientes lleno de energía.")
					os.system("pause")
					os.system("cls")
				else:
					print(f"{Bcolors.YELLOW}Posadero Pepito{Bcolors.CLEAR}: Hmm... Me parece que no tienes suficiente dinero. Vuelve cuando tengas más.")
					os.system("pause")
					os.system("cls")
			else:
				continue
		elif opcion == "3":
			while True:
				# Bucle de la tienda
				
				print(f"{Bcolors.YELLOW}Tendero José{Bcolors.CLEAR}: ¡Hola! ¿En que puedo ayudarle?")
				print(f"Dinero disponible: {main_player.gold}")
				print("1. Comprar")
				# TODO: posibilidad de vender un objeto que no necesites.
				# print("2. Vender")
				print("3. Salir")
				opcion2 = input("Elige [1-3]: ")
				if opcion2 == "1":
					while True:
						table = PrettyTable()
						table.field_names = ["Nº", "Nombre", "Precio", "Descripción"]
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
								print(Bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + Bcolors.CLEAR)
								continue
							selected_item = shop_item_list[int(opcion3)-1]
							print(f"¿Quieres comprar {selected_item.name} por {selected_item.cost} monedas de oro?")
							confirmacion = input("Elige [s/N]: ")
							if confirmacion == "s" or confirmacion == "S":
								if main_player.gold >= selected_item.cost:
									main_player.gold -= selected_item.cost
									main_player.items.append(selected_item)
									print(f"¡Compraste {selected_item.name}!")
									print(f"Dinero disponible: {main_player.gold}")
								else:
									print(f"{Bcolors.YELLOW}Tendero José{Bcolors.CLEAR}: Hmm... Me parece que no tienes suficiente dinero. Vuelve cuando tengas más.")
									os.system("pause")
									os.system("cls")
							else:
								continue
						except:
							print(Bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + Bcolors.CLEAR)
				elif opcion2 == "3":
					print(f"{Bcolors.YELLOW}Tendero José{Bcolors.CLEAR}: ¡Gracias por su compra!")
					os.system("pause")
					os.system("cls")
					break
		elif opcion == "9":
			print(f"{Bcolors.RED}ATENCIÓN{Bcolors.CLEAR}: Cualquier dato no guardado se perderá. ¿Salir de {Parameters.game_name}?")
			confirmacion = input("Elige [s/N]: ")
			if confirmacion == "s" or confirmacion == "S":
				os.system("cls")
				sys.exit()
			else:
				continue
		else:
			print(Bcolors.RED + "OPCIÓN NO VÁLIDA.\n" + Bcolors.CLEAR)
			continue
		print(f"{Bcolors.YELLOW}Posadero Pepito{Bcolors.CLEAR}: ¡Hola, viajero!")


def start_game(save_file):
	if save_file is not None:
		print("¡Bienvenido de nuevo!")
		return
	else:
		# Aquí pedimos un nombre para el personaje
		print(f"¡Bienvenido a {Parameters.game_name}!")
		name = input("Introduce tu nombre: ")
		main_player.name = name
		print(f"Empezando partida como {name}...\n")
		# ¡Empieza el juego!
		while True:
			start_battle_loop()
			break_time_loop()


print(Bcolors.CLEAR)
random.seed()

game_started = False
enemy_pool = []
main_player = initialize_player()

enemy_list = []
shop_item_list = initialize_shop_items()

skill_list = initialize_skills()

# Limpiamos la pantalla y empezamos una partida nueva.
time.sleep(1)
os.system("cls")
start_game(None)
