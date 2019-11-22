#!/usr/bin/env python3
# -*- encoding : utf-8 -*-

import json ; import collections ; import argparse ; import sys ; import csv ; import operator

parser = argparse.ArgumentParser(description='')
parser.add_argument('-c', '--create-from-db', dest="file_in")
parser.add_argument('-a', '--actor', dest="actor")
parser.add_argument('-d', '--director', dest="director")

args = parser.parse_args()

def create(file):
	#dictionnaire stockant les acteurs et une liste de films dans lesquels il a joué
	actors = collections.defaultdict()
	#dictionnaire stockant les réalisateurs avec une liste de films qu'ils ont réalisé
	directors = collections.defaultdict()
	
	tmp = {}

	try:
		with open(args.file_in) as f:
			for line in f:
				tmp = json.loads(line)

				if ("year" in tmp) and ("directors" in tmp):			
					for tmp_act in tmp["cast"]:
						if tmp_act not in actors:
							actors[tmp_act] = [(tmp['title'], tmp['year'])]
						else:
							actors[tmp_act].append((tmp['title'], tmp['year']))

					for tmp_directors in tmp["directors"]:
						if tmp_directors not in directors:
							directors[tmp_directors] = [(tmp['title'], tmp['year'])]
						else:
							directors[tmp_directors].append((tmp['title'], tmp['year']))

	except(FileNotFoundError, IOError):
		print("Le fichier spécifié n'existe pas ou le chemin d'accès est erronné.")
		exit
	else:	
			
		try:
			with open('directors.json', 'w',  encoding="utf8") as d: # on crée un fichier json appelé directors.json
				json.dump(directors, d) # dans lequel on y copie le dictionnaire "directors"
		except(PermissionError):
			print("Le programme n'a pas pu s'exécuter.")
			#raise
			exit
		try:
			with open('actors.json', 'w', encoding='utf8') as a:  # on crée un fichier json appelé actors.json
				json.dump(actors, a) # dans lequel on y copie le dictionnaire "actors"
		except(PermissionError):
			print("Le programme n'a pas pu s'exécuter.")
			#raise
			exit

# ======================================================================================================= #

def actor(actor_input):
	# créé une liste au format CSV à partir de actors.json recensant le nombre de films par année
	# year, nbfilm
	# 1987; 2
	# ...

	#print(actor_input)

	actor_choisi = {}
	nbr_films_annee = {}
	csv_columns=["Année", "Nombre de films"]

	prenom_nom = actor_input.split() # creation d'une liste contenant le nom et le prénom de l'acteur passé en argument

	prenom = prenom_nom[0] # stocke le prénom dans une variable
	nom = prenom_nom[1] # strocke le nom dans une autre vrariable

	csv_file = prenom + "_" + nom + ".csv" # concaténation afin d'obtenir un modèle : Prénom_Nom.csv

	try:
		with open("actors.json") as f:
			for line in f:
				acteur_choisi = json.loads(line)
	except(FileNotFoundError, IOError):
		print("Le fichier spécifié n'existe pas ou le chemin d'accès est erronné.")

	if actor_input not in acteur_choisi:
		try:
			with open(csv_file, 'w' ,newline='') as csvfile:
				csvfile.write("none")
		except(PermissionError):
			print("Le programme n'a pas pu s'exécuter.")
			raise
	
	else:
		# print(acteur_choisi)

		for film, annee in acteur_choisi[actor_input]:
			if annee in nbr_films_annee:
				nbr_films_annee[annee] += 1
			else:
				nbr_films_annee[annee] = 1

		# ordonnee_nbr_films_annee = sorted(nbr_films_annee.items(), key=operator.itemgetter(0))
		# print(ordonnee_nbr_films_annee)

		# print(nbr_films_annee)

		try:
			with open(csv_file, 'w' ,newline='') as csvfile:
				writer = csv.writer(csvfile)
				writer.writerow(["Année", "NbFilms"])
				for annee, nbfilms in nbr_films_annee.items():
					writer.writerow([annee, nbfilms])
		except(PermissionError):
			print("Le programme n'a pas pu écrire les nouveaux fichiers.")
			raise			

# ======================================================================================================= #

def director(director_input):

	directeur_choisi = {}
	nbr_film_annee = {}

	prenom_nom = director_input.split()
	prenom = prenom_nom[0] ; nom = prenom_nom[1]
	csv_file = prenom + "_" + nom + ".csv"


	try:
		with open("directors.json") as f:
			for line in f:
				directeur_choisi = json.loads(line)
	except(FileNotFoundError, IOError):
		print("Le fichier spécifié n'existe pas ou le chemin d'accès est erronné.")
		raise
		exit
	else:
		if director_input not in directeur_choisi:
			with open(csv_file, 'w' ,newline='') as csvfile:
				csvfile.write("none")
		else:
			for film, annee in directeur_choisi[director_input]:
				if annee in nbr_films_annee:
					nbr_films_annee[annee] += 1
				else:
					nbr_films_annee[annee] = 1

		# ordonnee_nbr_films_annee = sorted(nbr_films_annee.items(), key=operator.itemgetter(0))
		# print(ordonnee_nbr_films_annee)
		# print(nbr_films_annee)

		try:
			with open(csv_file, 'w' ,newline='') as csvfile:
				writer = csv.writer(csvfile)
				writer.writerow(["Année", "NbFilms"])
				for annee, nbfilms in nbr_films_annee.items():
					writer.writerow([annee, nbfilms])
		except(PermissionError):
			print("Le programme n'a pas pu s'exécuter.")
			raise
	finally:
		print("Fin de l'exécution de la fonction.")

# ======================================================================================================= #

if __name__ == "__main__":

	# print(len(sys.argv))
	if(sys.argv == 1):
		print("Erreur, aucun arguments.")
	else:
		if (args.file_in != None):
			print("Vous avez choisi la création d'une base de donnée !")
			create(args.file_in)
			sys.exit()
		if (args.actor != None):
			actor(args.actor)
			sys.exit()
		if (args.director != None):
			director(args.director)
			sys.exit()
