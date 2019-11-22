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
	
	with open('directors.json', 'w',  encoding="utf8") as d: # on crée un fichier json appelé directors.json
		json.dump(directors, d) # dans lequel on y copie le dictionnaire "directors"
	
	with open('actors.json', 'w', encoding='utf8') as a: # # on crée un fichier json appelé actors.json
		json.dump(actors, a) # dans lequel on y copie le dictionnaire "actors"

def actor(actor_input):
	# créé une liste au format CSV à partir de actors.json recensant le nombre de films par année
	# year, nbfilm
	# 1987; 2
	# ...

	print(actor_input)
	actor_choisi = {}
	nbr_films_annee = {}
	csv_columns=["Année", "Nombre de films"]

	with open("actors.json") as f:
		for line in f:
			acteur_choisi = json.loads(line)

	for film, annee in acteur_choisi[actor_input]:
		if annee in nbr_films_annee:
			nbr_films_annee[annee] += 1
		else:
			nbr_films_annee[annee] = 1
	
	prenom_nom = actor_input.split()

	prenom = prenom_nom[0]
	nom = prenom_nom[1]

	ordonnee_nbr_films_annee = sorted(nbr_films_annee.items(), key=operator.itemgetter(0))
	print(ordonnee_nbr_films_annee)

	csv_file = actor_input + ".csv"

	with open(csv_file, 'w' ,newline='') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
		writer.writeheader()
		for films in ordonnee_nbr_films_annee:
			writer.writerow(films)
			
'''def director():
	# même chose que pour acteur(), à partir de directors.json'''

if __name__ == "__main__":

	print(len(sys.argv))
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
