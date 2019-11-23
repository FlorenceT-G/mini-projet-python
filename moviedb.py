#!/usr/bin/env python3
# -*- coding : utf8 -*-

import json ; import collections ; import argparse ; import sys ; import csv ; import operator

parser = argparse.ArgumentParser(description='') 
parser.add_argument('-c', '--create-from-db', dest="file_in") # ajout de l'option -c / --create-from-db avec destination "file_in"
parser.add_argument('-a', '--actor', dest="actor") # ajout de l'option -a / --acteur avec destination "actor"
parser.add_argument('-d', '--director', dest="director") # ajout de l'option -d / --director avec destination "director"

args = parser.parse_args() # on parse les arguments 

def create(file):
	"""Ouvre le contenu d'une base de données de films au chemin spécifié 'file", les tries grâce à des dictionnaire puis créer les fichiers .json adaptés"""

	actors = collections.defaultdict() 	# dictionnaire stockant les acteurs et une liste de films dans lesquels il a joué
	directors = collections.defaultdict() # dictionnaire stockant les réalisateurs avec une liste de films qu'ils ont réalisé
	tmp = {} # dictionnaire temporaire dans lequel sont stockées les lignes ouvertes par json.loads()

	try: # bloc de gestion des erreurs pour l'ouverture des fichiers .json
		with open(args.file_in) as f: # ouvre le fichier spécifié
			for line in f: # boucle sur chaque ligne du fichier
				tmp = json.loads(line) # chaque ligne est ouverte avec json.loads et est stockées dans tmp

				if ("year" in tmp) and ("directors" in tmp): # si les clés "year" et "directors" se trouvent dans la ligne		
					for tmp_act in tmp["cast"]: # alors pour chaque acteurs de la clé "cast"
						if tmp_act not in actors: # si le nom de cet acteur n'est pas déjà stocké dans le dictionnaire "actors"
							actors[tmp_act] = [(tmp['title'], tmp['year'])] # alors on créé la clé acteur et on lui assigne les valeurs 'title' et 'year' associée
						else: # sinon, si l'acteur se trouve déjà en tant que clé dans le dictionnaire
							actors[tmp_act].append((tmp['title'], tmp['year'])) # alors, on ajoute le nouveau film et la nouvelle année à la clé acteur

					for tmp_directors in tmp["directors"]: # pour chaque clé "directeur"
						if tmp_directors not in directors: # si la clé n'existe pas déjà dans le dictionnaire alors
							directors[tmp_directors] = [(tmp['title'], tmp['year'])] # la clé est ajoutée avec comme valeur 'title' et 'year'
						else: # sinon, si le réalisateur se trouve déjà en tant que clé
							directors[tmp_directors].append((tmp['title'], tmp['year'])) # alors on ajoute les nouvelles valeurs

	except(FileNotFoundError, IOError): # si il y a eu les erreurs spécifiées lors du bloc try
		print("Le fichier spécifié n'existe pas ou le chemin d'accès est erronné.") # alors print message d'erreur
		exit # puis on quitte le programme

	try: # bloc de gestion d'erreur pour la création du fichier directors.json
		with open('directors.json', 'w',  encoding="utf8") as d: # on crée un fichier json appelé directors.json
			json.dump(directors, d, ensure_ascii=False) # dans lequel on y copie le dictionnaire "directors"
	except(PermissionError): # s'il n'y a pas la permission d'écrire dans le répertoire alors
		print("Erreur lors de l'écriture du fichier directors.json. Permission non accordée.")
		exit
	
	try: # bloc de gestion d'erreur pour la création du fichier actors.json
		with open('actors.json', 'w', encoding='utf8') as a:  # on crée un fichier json appelé actors.json
			json.dump(actors, a, ensure_ascii=False) # dans lequel on y copie le dictionnaire "actors"
	except(PermissionError):
		print("Erreur lors de l'écriture du fichier actors.json. Permission non accordée.")
		exit

# ======================================================================================================= #

def actor(actor_input):
	"""Créé une liste au format CSV à partir de actors.json recensant le nombre de films par année d'un acteur donné"""

	actor_choisi = {} # initialisation du dictionnaire spécifique à l'acteur choisi par l'utilisateur
	nbr_films_annee = {} # initialisation du dictionnaire qui contiendra l'année et le nombre de films
	csv_columns=["Année", "Nombre de films"]
	
	actor_input = actor_input.lower() # on passe la chaîne de caractères entrée par l'utilisateur en minuscule
	prenom_nom = actor_input.split() # creation d'une liste contenant le nom et le prénom de l'acteur

	prenom = prenom_nom[0] # stocke le prénom dans une variable
	nom = prenom_nom[1] # strocke le nom dans une autre vrariable
	
	prenom = prenom.capitalize() # Capitalisation du prenom
	nom = nom.capitalize() # Capitalisation du nom
	
	actor_input = prenom + " " + nom # concaténation afin d'obtnir une chaîne de caractères qui va pouvoir être reconnue

	csv_file = prenom + "_" + nom + ".csv" # concaténation afin d'obtenir une chaîne de caractère de modèle : Prénom_Nom.csv

	try: # bloc gestion d'erreur pour l'ouverture du fichier actor.json
		with open("actors.json") as f: # on ouvre le fichier actors.json 
			for line in f: # pour chaque ligne du fichier
				acteur_choisi = json.loads(line) # le dictionnaire acteur_choisi prend la ligne ouverte avec json.loads
	except(FileNotFoundError, IOError): # sauf si fichier pas trouvé
		print("Le fichier spécifié n'existe pas ou le chemin d'accès est erronné.")
		exit

	if actor_input not in acteur_choisi: # si l'acteur choisi par l'utilisateur n'est pas trouvé
		try: # bloc gestion d'erreur
			with open(csv_file, 'w' ,newline='') as csvfile: # on créé un fichier Prénom_Nom.csv
				csvfile.write("none") # qui ne contient que "non"
		except(PermissionError): # sauf s'il n'y a pas la permission d'écrire
			print("Le programme n'a pas pu s'exécuter.")
			exit
	
	else: # sinon, si le bloc try s'est exécuté avec succès
		for film, annee in acteur_choisi[actor_input]: # alors, pour chaque film et chaque année de l'acteur choisi
			if annee in nbr_films_annee: # si l'année est déjà dans le dictionnaire nbr_films_annee
				nbr_films_annee[annee] += 1 # alors la valeur associée à l'année augmente de 1
			else: # sinon
				nbr_films_annee[annee] = 1 # l'année est rajoutée dans le dictionnaire et prends la valeur 1

		try: # bloc gestion d'erreur pour l'écriture du fichier Prénom_Nom.csv
			with open(csv_file, 'w' ,newline='') as csvfile: # on créé un fichier Prénom_Nom.csv
				writer = csv.writer(csvfile)
				writer.writerow(["Année", "NbFilms"]) # la première ligne contient Année,NbFilms
				for annee, nbfilms in nbr_films_annee.items(): # pour pour toutes les années et le nombre de films dans le dictionnaire nbr_films_annee
					writer.writerow([annee, nbfilms]) # on écrit l'année et le nombre de films associé
		except(PermissionError):
			print("Erreur lors de l'écriture du fichier. Permission non accordée.")
			exit		

# ======================================================================================================= #

def director(director_input):
	"""Créé une liste au format CSV à partir de directors.json recensant le nombre de films par année d'un acteur donné"""

	director_choisi = {}
	nbr_films_annee = {}
	csv_columns=["Année", "Nombre de films"]
	
	director_input = director_input.lower() # on passe la chaîne de caractères entrée par l'utilisateur en minuscule
	prenom_nom = director_input.split() # creation d'une liste contenant le nom et le prénom de l'acteur

	prenom = prenom_nom[0] # stocke le prénom dans une variable
	nom = prenom_nom[1] # strocke le nom dans une autre vrariable
	
	prenom = prenom.capitalize() # Capitalisation du prenom
	nom = nom.capitalize() # Capitalisation du nom
	
	director_input = prenom + " " + nom # concaténation afin d'obtnir une chaîne de caractères qui va pouvoir être reconnue

	csv_file = prenom + "_" + nom + ".csv" # concaténation afin d'obtenir une chaîne de caractère de modèle : Prénom_Nom.csv

	try: # bloc gestion d'erreur pour l'ouverture du fichier director.json
		with open("directors.json") as f: # on ouvre le fichier directors.json 
			for line in f:
				director_choisi = json.loads(line)
	except(FileNotFoundError, IOError):
		print("Le fichier spécifié n'existe pas ou le chemin d'accès est erronné.")

	if director_input not in director_choisi:
		try:
			with open(csv_file, 'w' ,newline='') as csvfile:
				csvfile.write("none")
		except(PermissionError):
			print("Erreur lors de l'écriture du fichier. Permission non accordée.")
			exit
	
	else:
		for film, annee in director_choisi[director_input]:
			if annee in nbr_films_annee:
				nbr_films_annee[annee] += 1
			else:
				nbr_films_annee[annee] = 1

		try:
			with open(csv_file, 'w' ,newline='') as csvfile:
				writer = csv.writer(csvfile)
				writer.writerow(["Année", "NbFilms"])
				for annee, nbfilms in nbr_films_annee.items():
					writer.writerow([annee, nbfilms])
		except(PermissionError):
			print("Erreur lors de l'écriture du fichier. Permission non accordée.")
			exit		
					
# ======================================================================================================= #

if __name__ == "__main__":
	"""vérifie le nombre d'arguments donné à l'appel du programme et exécute différentes fonctions suivant les options données"""

	if(len(sys.argv) == 1):
		print("Erreur, aucun arguments.")
	elif(len(sys.argv) > 3):
		print("Erreur, le nombre d'argument donné est erronné.")
	else:
		if (args.file_in != None): # si un fichier a été passé en argument avec l'option -c / --create-from-db
			create(args.file_in) # alors on appel la fonction create() et on lui passe le nom du fichier en argument
			sys.exit() # puis, une fois que la fonction a fini, le programme s'arrête
		if (args.actor != None): # si un argument a été passé avec l'option -a / --actor
			actor(args.actor) # alors on appel la fonction actor() avec argument d'entrée le nom de l'acteur
			sys.exit() # arrêt du programme
		if (args.director != None): # # si un argument a été passé avec l'option -d / --director
			director(args.director) # on appel la fonction director() avec en argument d'entrée le nom du directeur
			sys.exit() # arrêt du programme
