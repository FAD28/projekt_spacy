import re
import os
import spacy
BASEDIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Spacy:
	# def __init__(self):
	# 	pass

	def lemma_pd(dataframe):
		freude_lemma = []
		freude_text = []
		freude_pos = []
		freude_dict = {}
		nlp = spacy.load("de")
		#doc = nlp(df['freude'])
		for item in tqdm(dataframe):
		    doc = nlp(str(item))
		    for token in doc:
		        freude_lemma.append(token.lemma_)
		        freude_text.append(token.text)
		        freude_pos.append(token.pos_)
		freude_dict['lemma'] = freude_lemma
		freude_dict['text'] = freude_text
		freude_dict['position'] = freude_pos
		return freude_dict



class Emotionen_rklinger:

	def __init__(self):
		self.ekel_lexicon = []
		self.freude_lexicon = []
		self.furcht_lexicon = []
		self.trauer_lexicon = []
		self.ueberraschung_lexicon = []
		self.verachtung_lexicon = []
		self.wut_lexicon = []

	def show(self):
		print("	1.	Ekel")
		print("	2.	Freude")
		print("	3.	Furcht")
		print("	4.	Trauer")
		print("	5.	Überraschung")
		print("	6.	Verachtung")
		print("	7.	Wut")

	def load_ekel(self):
		self.ekel_file = open(os.path.join(BASEDIR+'/txtanalysis'+'/fundamental'+'/ekel.txt'), 'r')
		for item in self.ekel_file:
			low= item.lower() 
			rep= low.replace("\n","")
			self.ekel_lexicon.append(rep)
		return self.ekel_lexicon

	def load_freude(self):
		self.freude_file = open(os.path.join(BASEDIR+'/txtanalysis'+'/fundamental'+'/freude.txt'), 'r')
		for item in self.freude_file:
			low= item.lower() 
			rep= low.replace("\n","")
			self.freude_lexicon.append(rep)
		return self.freude_lexicon

	def load_furcht(self):
		self.furcht_file = open(os.path.join(BASEDIR+'/txtanalysis'+'/fundamental'+'/furcht.txt'), 'r')
		for item in self.furcht_file:
			low= item.lower() 
			rep= low.replace("\n","")
			self.furcht_lexicon.append(rep)
		return self.furcht_lexicon

	def load_trauer(self):
		self.trauer_file = open(os.path.join(BASEDIR+'/txtanalysis'+'/fundamental'+'/trauer.txt'), 'r')
		for item in self.trauer_file:
			low= item.lower() 
			rep= low.replace("\n","")
			self.trauer_lexicon.append(rep)
		return self.trauer_lexicon

	def load_ueberraschung(self):
		self.ueberraschung_file = open(os.path.join(BASEDIR+'/txtanalysis'+'/fundamental'+'/ueberraschung.txt'), 'r')
		for item in self.ueberraschung_file:
			low= item.lower() 
			rep= low.replace("\n","")
			self.ueberraschung_lexicon.append(rep)
		return self.ueberraschung_lexicon

	def load_verachtung(self):
		self.verachtung_file = open(os.path.join(BASEDIR+'/txtanalysis'+'/fundamental'+'/verachtung.txt'), 'r')
		for item in self.verachtung_file:
			low= item.lower() 
			rep= low.replace("\n","")
			self.verachtung_lexicon.append(rep)
		return self.verachtung_lexicon

	def load_wut(self):
		self.wut_file = open(os.path.join(BASEDIR+'/txtanalysis'+'/fundamental'+'/wut.txt'), 'r')
		for item in self.wut_file:
			low= item.lower() 
			rep= low.replace("\n","")
			self.wut_lexicon.append(rep)
		return self.wut_lexicon

	def extract_words(self,data, lexicon):
		sentiment_words = []
		for item in data: 
			for element in lexicon:
				if item == element:
					sentiment_words.append(item)
				else:
					continue
		return sentiment_words








