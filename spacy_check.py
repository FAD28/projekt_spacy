import spacy
from spacy import displacy
import time
from txtanalysis.utils import DataWrangling as DW
from txtanalysis.utils import DataCleaner as DC
from txtanalysis.emotion import Emotionen_rklinger
import random 
import matplotlib
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup as bs
import datetime
import pandas as pd
import csv
from tqdm import tqdm
import networkx as nx
import numpy as np
import os
rklinger = Emotionen_rklinger()
print(" Start rklinger ")
now = datetime.datetime.now()
date = now.strftime("%d-%m-%Y")

testtext = ['Türkische Soldaten sterben durch Luftangriffe in Idlib','Die türkische Regierung hat nach dem Tod mehrerer Soldaten eine Sondersitzung einberufen.', 'Unklar war zunächst ob die Attacke von Russland oder Syrien ausging.']

nlp = spacy.load('de')
# doc = nlp(rawtext)
# for token in doc: 
# 	print(token.text, "------", token.dep_, "-------", token.pos_)



# for item in rawtext:
def create_linklist(link):
	"""
	Use it just once a day for not making to much requests
	"""
	data = requests.get(link).text
	# file = open(f'links_taz-{date}.txt','w+')
	# writer = csv.writer(file)
	soup = bs(data, 'lxml')
	links = []
	for element in soup.find_all('a',class_="text-black block"):
		if element.has_attr("href"):
			link = element.attrs['href']
			links.append(link)
	df = pd.DataFrame(links)
	# print(df)
	df.to_csv(f'links_taz-{date}.txt', header= 'data')
	print("** File created. Check it please!")
	return links

def open_links(file):
	file = pd.read_csv(file, names= ["data"])
	# print(file)
	data = [i for i in file['data']]
	# print(len(data))
	# print(data)
	# x = random.randint(1, 79)
	y = 42
	while y < len(data) :
		print(y)
		if y == 20:
			time.sleep(20)
		page = requests.get(data[y]).text
		time.sleep(4)
		soup = bs(page, 'lxml')
		article = {}
		# print(data[x])

		print("____****____")

		article_text = []
		for element in soup.find_all('p'):
			text= element.text
			article_text.append(text)

		article['text'] = article_text
		print(len(article['text']))

		
		header1 = data[y].replace("https://www.spiegel.de/","")
		header = header1.replace("/","_")

		article['header'] = data[y]
		df = pd.DataFrame.from_dict(article['text'])
		print(df)
		df.to_csv(f'{header}.csv')
		print("time sleep")
		time.sleep(5)
		y +=1

def define_headers(file):
	# Das brauchen wir eigentlich außerhalb aber ich bin irgendwie zu müde gerade (und jetzt 25 ;) ) 
	headers = pd.read_csv(file)
	header = []
	x = 0 
	for item in headers['0']:
		item2 = item.replace("https://www.spiegel.de/","")
		item3 = item2.replace("/","_")
		header.append(item3)
	return header


def open_data(headerz):
	pandas_data = pd.read_csv(f'{headerz}.csv', names=['index','text'])
	data = pandas_data['text']
	data_liste = [i for i in data]
	clean_data = DC.clean_list(data_liste)

	return clean_data

def cleaning(data):
	data2 = []
	for item in data:
		item1 = item.replace("nur € pro monat","")
		item2 = item1.replace("spiegel+ wird über ihren itunesaccount abgewickelt und mit kaufbestätigung bezahlt stunden vor ablauf verlängert sich das abo automatisch um einen monat zum preis von zurzeit € in den einstellungen ihres itunesaccounts können sie das abo jederzeit kündigen um spiegel+ außerhalb dieser app zu nutzen müssen sie das abo direkt nach dem kauf mit einem spiegelidkonto verknüpfen mit dem kauf akzeptieren sie unsere allgemeinen geschäftsbedingungen und datenschutzerklärung","")
		item3 = item2.replace("jederzeit kündbar","")
		item4 = item3.replace("des wöchentlichen magazins","")
		item5 = item4.replace("zu allen inhalten auf all ihren geräten","")
		item6 = item5.replace("ihre vorteile mit spiegel+","")
		item7 = item6.replace("besondere reportagen analysen und hintergründe zu themen die unsere gesellschaft bewegen – von reportern aus aller welt","")
		item8 = item7.replace("alle bereits erschienen folgen dieses podcasts finden sie hier bei audible","")
		item9 = item8.replace("melden sie sich an und diskutieren sie mit","")
		item10 = item9.replace("aus dem wöchentlichen magazin","")
		item11 = item10.replace("jederzeit online kündbar","")
		item12 = item11.replace("in dieser woche","")
		item13 = item12.replace("dpa","")
		data2.append(item13)
	return data2

def return_clean(header):
	x = 0 
	file = []
	print("Anzahl der Links=",len(header))
	while x < len(header):
		try:
			data= open_data(header[int(f'{x}')])
			# time.sleep(2)
			# print("checkpoint")
			clean_data = cleaning(data)
			file.append(clean_data)
			# print(len(file))
			# time.sleep(2)
			# print("_______")
		except:
			# print("ENDE")
			pass
		x+=1
	# data1= open_data(header[1])
	# clean_data0 = cleaning(data0)
	# clean_data1 = cleaning(data1)
	# print(clean_data0)
	# print(clean_data1)
	file_final = DW.merge_data(file)
	return file_final

def print_pd_zwischenresult(data):
	return data.to_csv('first_result.csv')
def load_zwischenresult(data):
	file = pd.read_csv(data)
	return file 

def show_len():
	print("	1.	Ekel", len(ekel_words))
	print("	2.	Freude", len(freude_words))
	print("	3.	Furcht",len(furcht_words))
	print("	4.	Trauer", len(trauer_words))
	print("	5.	Überraschung",len(ueberraschung_words))
	print("	6.	Verachtung", len(verachtung_words))
	print("	7.	Wut", len(wut_words))

def try_to_get_information(data):
	for item in data: 
		doc = nlp(item)
		print("*** _______________________________________________________________ ***")
		for token in doc:
			print(token.text, "------", token.dep_, "-------", token.pos_)
		# time.sleep(2)
		# print("next iteration <----")

def get_relations(data):
	"""
	Die Daten kommen als Liste mit einzelnen Sätzen als Items
	"""
	# Ziel:			Einheiten in einem Satz erkennen und zusammenhänge zwischen Subjekt-Objekt und Prädikat ausgeben
	relations = []
	data_dict = {}
	for item in data:
		print("------>",item, "<------")
		doc = nlp(item)
		x = 0
		while x < len(data):
			subjekt_liste = []
			prädikat_liste = []
			objekt_liste = []
			for tok in doc: 

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
				# time.sleep(.1)
				for item in so_zip:
					relations.append(item)
				for item in sp_zip:
					relations.append(item)
				for item in op_zip:
					relations.append(item)
				x +=1
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



# splited_data = DW.split_data(rawtext)
# stopwords = DW.load_stopwords()
# clean_data = DW.remove_stopwords(splited_data, stopwords)
# print(clean_data)
# merged_data = [" ".join(clean_data)]
# print(merged_data)

"""
----> EXECUTION ***
"""
link = "https://www.spiegel.de/"
file = f'links_taz-{date}.txt'
try_to_get_information(testtext)
get_relations(testtext)
create_linklist(link)
open_links(file)

header = define_headers(file)
one_file = return_clean(header)

data_mitna= pd.DataFrame(one_file, columns= ['text'])
data = data_mitna.drop_duplicates()
data2 = data['text']







#### SPLIT & STOPWÖRTER ####
shaped_data = DW.split_data(data2)
print(len(shaped_data))
my_stp = ['bpk','archives','alinari']
stopwords = DW.load_stopwords(my_stp)
redux = DW.remove_stopwords(shaped_data, stopwords)
print(len(redux))






#### EMOTION LEXIKON ####
print("   #### EMOTION LEXIKON ####    ")
rklinger.show()
ekel_lexicon = rklinger.load_ekel()
freude_lexicon = rklinger.load_freude()
furcht_lexicon = rklinger.load_furcht()
trauer_lexicon = rklinger.load_trauer()
ueberraschung_lexicon = rklinger.load_ueberraschung()
verachtung_lexicon = rklinger.load_verachtung()
wut_lexicon = rklinger.load_wut()

ekel_words = rklinger.extract_words(redux, ekel_lexicon)
freude_words = rklinger.extract_words(redux, freude_lexicon)
furcht_words = rklinger.extract_words(redux, furcht_lexicon)
trauer_words = rklinger.extract_words(redux, trauer_lexicon)
ueberraschung_words = rklinger.extract_words(redux, ueberraschung_lexicon)
verachtung_words = rklinger.extract_words(redux, verachtung_lexicon)
wut_words = rklinger.extract_words(redux, wut_lexicon)

emotion_dict={'ekel': ekel_words, 'freude': freude_words, 'furcht': furcht_words,'trauer': trauer_words, 'ueberraschung': ueberraschung_words, 'verachtung': verachtung_words, 'wut': wut_words}
# print(emotion_dict)
show_len()
DW.tfidf_calculate(redux)

print_pd_zwischenresult(data)



"""
Versuche einen Infinity loop über plotten zu machen. Nicht gut. Habe jetzt ein Link https://www.youtube.com/watch?time_continue=1034&v=Ercd-Ip5PfQ&feature=emb_title
"""
# fabi = 0 
# while fabi < 25:
# 	hl, = plt.plot([random.randint(1,10)], [random.randint(1,10)])
# 	new_data = ([random.randint(1,10)], [random.randint(1,10)])
# 	infinity_plot(hl, new_data)
# 	print("sleep 123")
# 	# time.sleep(3)
# 	print(fabi)
# 	fabi +=1






