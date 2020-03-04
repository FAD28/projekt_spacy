import spacy
import time
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

testdaten = ['Erste Migranten machen sich offenbar von der Türkei Richtung EU-Grenze auf',' In Mugla hätten einige Gummiboote mitgebracht.','Die staatliche Nachrichtenagentur Anadolu berichtete dass sich Migranten in den Städten Izmir Mugla und Canakkale sammelten für die Reise Richtung EU.','Zuvor hatte die türkische Regierung erklärt sie wolle syrische Flüchtlinge auf dem Weg nach Europa nicht mehr aufhalten.','Eskaliert war die Lage nach einem syrischen Luftangriff in Idlib in der Nacht auf Freitag bei dem mindestens 33 türkische Soldaten getötet worden waren.','Die Türkei die in dem Konflikt islamistische Rebellen unterstützt hat dort Beobachtungsposten.']
peter = ['Die Katze frisst den Hund.', 'Meine Katze heißt Charlie','Mein Freund heißt Charlie und er läuft über Wasser.', 'Fabian programmierte das Programm sehr gut.', 'Charlie ist ein Affe.', 'Er soll den Insassen seiner Jugendstrafanstalt Handys, Cannabis und härtere Drogen besorgt haben','Linkenpolitiker Bodo Ramelow will am Mittwoch Ministerpräsident werden.','Migranten aus Lateinamerika müssen monatelang in mexikanischen Grenzstädten auf ihren US-Asylprozess warten -	 wo ihnen Gewalt und Entführungen drohen']
nlp = spacy.load('de')
def get_relations(data):
	"""
	Die Daten kommen als Liste mit einzelnen Sätzen als Items
	"""
	# Ziel:			Einheiten in einem Satz erkennen und zusammenhänge zwischen Subjekt-Objekt und Prädikat ausgeben
	# data= filter(None, input_data)
	relations = []
	data_dict = {}
	counter = 1 
	for item in data:
		print(" SATZNUMMER: ", counter, " / ", len(data))
		print("------>",item, "<------")
		
		doc = nlp(item)
		print(len(item))
		x = 0
		while x < len(item):
			subjekt_liste = []
			prädikat_liste = []
			objekt_liste = []
			for tok in doc: 
				print("TOKEN----->",tok)
				# Hier werden einzelne Wörter durchgegeben
				if tok.pos_ == 'NOUN':
					if tok.dep_.startswith("o") == True:
						# print("Objekt + NOUN:",tok.text)	
						objekt_liste.append(tok.text+"-"+tok.dep_)				# <---- Objekt 1
					if tok.dep_.startswith("s") == True:
						# print("Subjekt + NOUN:", tok.text)
						subjekt_liste.append(tok.text+"-"+tok.dep_)				# <---- Subjekt 1
					if tok.dep_ == "nk":
						# print("Objekt + NOUN (nk):", tok.text)
						objekt_liste.append(tok.text+"-"+tok.dep_)					 # <--- Objekt 2
				if tok.pos_ == 'PROPN':
					if tok.dep_.startswith("o") == True:
						# print("Objekt + PROPN:",tok.text)
						objekt_liste.append(tok.text+"-"+tok.dep_)					# <--- Objekt 3
					if tok.dep_.startswith("s") == True:
						# print("Subjekt + PROPN:", tok.text)
						subjekt_liste.append(tok.text+"-"+tok.dep_)				# <---- Subjekt 2
					if tok.dep_ == "pnc":
						# print("Subjekt + PROPN (pnc):", tok.text)
						subjekt_liste.append(tok.text+"-"+tok.dep_)				# <---- Subjekt 3
					if tok.dep_ == "nk":
						# print("Objekt + PROPN (nk):", tok.text)
						objekt_liste.append(tok.text +"-" +tok.dep_)				# <--- Objekt 4
				if tok.pos_ == 'VERB':
					# print("VERB:",tok.text)
					prädikat_liste.append(tok.text+"-"+tok.dep_)					# <----  Prädikat 1
					if tok.dep_ == 'ROOT':
						# print("VERB + ROOT:", tok.text)
						prädikat_liste.append(tok.text+"-"+tok.dep_)			# <----  Prädikat 2
				so_zip = list(zip(subjekt_liste, objekt_liste))
				sp_zip = list(zip(subjekt_liste, prädikat_liste))
				op_zip = list(zip(objekt_liste, prädikat_liste))
				print("ZIP: 	Subjekt-Objekt		", so_zip, "                     ", x)
				print("ZIP 2:	Subjekt-Prädikat	", sp_zip, "                     ", x)
				print("ZIP 3: 	Objekt-Prädikat		", op_zip, "                     ", x)
				time.sleep(.1)
				for item in so_zip:
					relations.append(item)
				for item in sp_zip:
					relations.append(item)
				for item in op_zip:
					relations.append(item)
				x +=1
		counter += 1
		relation_results= [t for t in (set(tuple(i) for i in relations))]
		data_dict = {'subjekt': subjekt_liste, 'prädikat': prädikat_liste,'objekt':objekt_liste}
	print("RELATIONS: __________________")
	print(relation_results)
	file = open("relations.txt", 'w')
	file.write('\n'.join('{},{}'.format(x[0],x[1]) for x in relation_results))
	return relation_results

def show_phrase(data):
	for item in data:
		doc = nlp(item)
		for tok in doc:
			print(tok.text,"------",tok.dep_, "-------",tok.pos_)

def read_relations(file):
	with open(file) as f:
		mylist = [tuple(map(str, i.split(','))) for i in f]
	print(mylist)
	return mylist


def plot_network(data):
	print("PLOTTING:")
	print(data)
	G = nx.Graph()
	G.add_edges_from(data)
	nx.draw(G, with_labels= True)
	plt.show()



# data_dict = get_relations(testdaten)
print("____________________________________")
# time.sleep(2)
# print(data_dict)
print("____________________________________")
relations_file = "relations.txt"
# data_dict= read_relations(peter)
show_phrase(peter) 
data_dict =get_relations(peter)
# show_phrase(testdaten)
plot_network(data_dict)

