#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 19:53:04 2020

@author: macbookdenathan
"""

import nltk
import os 
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
import glob
import shutil

def pdfparser(data):
    #extrait le contenu textuel d'un pdf 
    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()
    return data

def pre_traitement(text) :
    #transforme le texte en liste de mots en minuscule
    tokenizer = nltk.tokenize.RegexpTokenizer("\w+")
    tokens = tokenizer.tokenize(text)
    words = []
    for word in tokens:
        words.append(word.lower())
    return words

def keyword_test(liste_d_articles, key, nombre):
    #crée une liste contenant tous les acticles dont l'occurence du mot clef dans les 500 premiers mots est supérieure au nombre souhaité 
    articles_recherchés = []
    compteur = 0
    for article in liste_d_articles :  
        texte_brut = pdfparser(article)
        texte_traité = pre_traitement(texte_brut)
        liste = texte_traité[0:500]
        for mot in  liste : 
            if mot == key :
                compteur = compteur + 1
                if compteur == nombre : 
                    articles_recherchés.append(article)
        compteur = 0
    return articles_recherchés

def create_final_folder(articles_recherchés):
    #crée un nouveau dossier dans le dossier A_LIRE contenant des copies des articles de la liste
    try :
        os.mkdir(keyword)
    except OSError :
        print(os.strerror(OSError.errno))
    for article in articles_recherchés:
        shutil.copy(article, keyword + "/" + "copie_" + article)
 
path = "/Users/macbookair/Desktop/A_LIRE"
#chemin absolu vers le dossier contanant les articles au format .pdf

os.chdir(path)
#change le répertoire de travail, le dossier A_LIRE étant maintenant le répertoire de travail

liste_de_pdf = glob.glob("*.pdf")
#genère une liste contenant tous les noms des pdf du dossier

keyword = input("Entrez le mot clef :")
#demande le mot clef

occurence = int(input("Entrez l'occurence souhaitée du mot clef :"))
#demande l'occurence souhaitée du mot clef

articles_recherchés = keyword_test(liste_de_pdf, keyword, occurence)

create_final_folder(articles_recherchés)

articles_dans_dossier = str(articles_recherchés)
print("Un nouveau dossier "+ keyword + " contenant les articles " + articles_dans_dossier + " a été créé dans votre dossier A_LIRE.")
print("Merci, et à bientot !")
