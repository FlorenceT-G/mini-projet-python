#!/usr/bin/env python3
# -*- encoding : utf-8 -*-

import json 
import collections
import argparse
import sys

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
	
	# f = open("moviebd_small.json", "r") 
	with open(args.file_in) as f:
		for line in f:
			tmp = json.loads(line)
			
			if "year" in tmp:			
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
	
	with open('directors.json', 'w',  encoding="utf8") as d:
		json.dump(directors, d)
	
	with open('actors.json', 'w', encoding='utf8') as a:
		json.dump(actors, a)

def actor(actor_input):
	# créé une liste au format CSV à partir de actors.json recensant le nombre de films par année
	# year, nbfilm
	# 1987; 2
	# ...	
	
	actor_choisi = collections.defaultdict()

	with open("actors.json") as f:
		if actor_input:
			for year in f[actor_input]:
				acteur_choisi[f[year]] = 1
			
'''def director():
	# même chose que pour acteur(), à partir de directors.json'''


if __name__ == "__main__":
	if(sys.argv == 1):
		print("Erreur, aucun arguments.")
	else:
		if (args.file_in != None):
			create(args.file_in)
			sys.exit()
		if (args.actor != None):
			actor(args.actor)
			sys.exit()
		if (args.director != None):
			director(args.director)
			sys.exit()

