import re
import os, math
import itertools
from textblob_de import TextBlobDE as tbde
from textblob_de.lemmatizers import PatternParserLemmatizer
from tqdm import tqdm
_lemmatizer = PatternParserLemmatizer()
BASEDIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class DataCleaner:

	def __init__(self):
		pass

	def clean_list(liste):
		"""
		Säubert eine Liste und entfernt alle Punctuations, Emojis, Japanische, Kyrillische und Chinesische Zeichen
		Außerdem wird jedes item lower gemacht

		: param		liste: 		eine liste ['Lorem ipsum ..']
		: return	liste: 		gibt eine saubere liste zurück
		"""
		cleaned_list = []
		for item in liste:
			item2 = item.lower()
			item3 = re.sub(r"[-()\"#/@;:<>{~|.?!,´`]","",item2)
			item4 = item3.replace('„'," ")
			item5 = item4.replace("“"," ")
			item6 = item5.replace("·"," ")
			item7 = item6.replace(r"\n"," ")
			item8 = re.sub(r"\n", " ", item7)
			item9 = re.sub('👍',' ', item8)
			item10 = re.sub('😀',' ',item9)
			item11 = re.sub('😊',' ',item10)
			item12 = re.sub('😉',' ',item11)
			item13 = re.sub('🙄',' ',item12)
			item14 = re.sub('😃',' ',item13)
			item15 = re.sub('😁',' ',item14)
			item16 = item15.replace('übersetzung anzeigen','')
			item17 = re.sub('🏻', ' ',item16)
			item18 = re.sub('🏼',' ',item17)
			item19 = re.sub(r'[ء-ي0-9ﭐ-﷿ﹰ-ﻼ]', '', item18)
			item20 = re.sub(r'[А-я]+','', item19)
			item21 = re.sub(r'[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]','',item20)
			item22 = item21.replace("'","")
			item23 = item22.replace("_","")
			item24 = item23.replace(" "," ")
			item25 = item24.strip('')
			cleaned_list.append(' '.join(item25.split())) # <----- überflüssige whitespaces entfernen
		return cleaned_list

class DataWrangling:

	def __init__(self):
		pass

	def load_stopwords(my_stopword= ['Tajin']):
	    """
	    Ladet die Stopwords list und fügt sie mit der liste der eigenen Stopwörtern zusammen

	    :param		stopwords 		eine file .txt mit den Stopwörtern
	    :param		my_stopwords	eine liste mit eigenen Stopwords ['Lorem','Ipsum',..]
	    :return		stopwords_list	eine Liste mit den Stopwörtern (alle klein)
	    """
	    path= os.path.join(BASEDIR+'/txtanalysis'+'/STP_de.txt')
	    file = open(path,'r',encoding="utf8")
	    stopwords_list =[]
	    read_g = file.readlines()
	    for x in read_g:
	        sub_string = re.sub(r"(?<=[a-z])\r?\n","", x)
	        stp_word = sub_string.replace("\n","")
	        stopwords_list.append(stp_word.lower())
	    own_stopword = [y.lower() for y in my_stopword]
	    stopwords_list = stopwords_list + own_stopword 

	    return stopwords_list

	def split_data(data):
		shaped1_data = [i.split() for i in data]
		shaped_list = list(itertools.chain.from_iterable(shaped1_data))
		return shaped_list

	def merge_data(data):
		return list(itertools.chain.from_iterable(data))

	def remove_stopwords(my_list, stopwords):
		'''
		Funktioniert irgendwie nur mit split() items 
		'''
		data = [x for x in my_list if x not in stopwords]
		return data

	def tfidf_calculate(clean_data):
		"""
        Errechnet den Tfidf von in jeweils 1/3 geteilte Abschnitte des sliste_n 

        : param clean_data: liste 
        """
		blob_wtf = tbde(str(clean_data))
		blob_lemma = _lemmatizer.lemmatize(str(blob_wtf))
		sliste_n = [x for (x,y) in blob_lemma if y not in ('N')]
		def tf(word, blob):
			return blob.words.count(word) / len(blob.words)
		def n_containing(word, bloblist):
			return sum(1 for blob in bloblist if word in blob.words)
		def idf(word, bloblist):
			return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))
		def tfidf(word, blob, bloblist):
			return tf(word, blob) * idf(word, bloblist)
		nb1 = int(len(clean_data) * 0.333)
		nb2 = nb1 * 2
		nb3 = len(clean_data)
		doku1= tbde(str(sliste_n[0:nb1]))
		doku2= tbde(str(sliste_n[nb1:nb2]))
		doku3= tbde(str(sliste_n[nb2:nb3]))

		bloblist = [doku1,doku2,doku3]
		for i, item in enumerate(bloblist):
		   
		   print("Top words in document {}".format(i + 1))
		   
		   scores = {word: tfidf(word, item, bloblist) for word in item.words}
		   
		   sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
		   
		   for element, score in sorted_words[:3]:
		       
		       print("\tWord: {}, TF-IDF: {}".format(element, round(score, 4)))
		return sliste_n



