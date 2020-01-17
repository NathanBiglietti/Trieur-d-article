# Trieur d'article

## Introduction 
L'idée de ce programme m'est venue en constatant les conséquences de mon téléchargement compulsif d'articles que je n'ai en général pas le temps de lire.
En effet, au fur et à mesure, s'accumulent dans un dossier "à lire" des articles dont je n'ai plus aucune idée du contenu. 
Parfois cependant, lorsqu'un temps libre se présente devant moi ou qu'une soif de connaissance m'assailli à 2h du matin alors que je devrais dormir, il m'arrive d'ouvrir cette caverne d'Alibaba qu'est ce dossier "à lire". 
Le problème est le suivant : à ce moment précis, ma curiosité se restreint à une certaine gamme limité de thématiques. 
Pour trouver la perle rare correspondant à mes attentes parmis les inombrables articles du dossier, il est alors nécessaire d'ouvrir un par un les articles, d'en lire l'astract jusqu'à ce qu'on trouve le bon. Une tâche ennuyeuse et rébarbative qui parfois (surtout à 2h du matin), me démotive finalement de la lecture. Automatiser celle ci s'est donc présenté très natuerellement comme une nécessité. 

L'intérêt du programme que j'ai créé est donc de pouvoir y voir clair dans cet amoncellement d'articles qu'un cerveau paresseux n'a aucun intérêt à trier. Pour ce faire, l'idée était de générer au sein du dossier "à lire" des sous dossiers contenant tous les articles présentant dans leurs premiers 500 mots un occurence donnée (*n*) d'un mot clef donné (*x*). À partir de ces deux informations renseignées dans la console, le programme doit donc : 
1. Extraire le contenu textuel d'articles donnés au format pdf
2. Traiter ce contenu textuel pour qu'il soit analysable
3. Retenir les articles contenant *n* fois le mot *x* dans leurs 500 premiers mots 
4. Créer un dossier à partir des articles retenus

Une fonction a été créée pour chacune de ces tâches. J'expliquerais donc le fonctionnement de chacune d'entre elles avant de commenter l'exécution du programme et de conclure.

## 1) pdfparser
```
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
```

## 2) pre_traitement

```
def pre_traitement(text) :
    #transforme le texte en liste de mots en minuscule
    tokenizer = nltk.tokenize.RegexpTokenizer("\w+")
    tokens = tokenizer.tokenize(text)
    words = []
    for word in tokens:
        words.append(word.lower())
    return words
```

## 3) keyword_test

```
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
```

## 4) create_final_folder

```
def create_final_folder(articles_recherchés):
    #crée un nouveau dossier dans le dossier A_LIRE contenant des copies des articles de la liste
    try :
        os.mkdir(keyword)
    except OSError :
        print(os.strerror(OSError.errno))
    for article in articles_recherchés:
        shutil.copy(article, keyword + "/" + "copie_" + article)
```

## 5) Exécution 

```
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
```

## Conclusion

conclure sur la réalisation et le fonctionnement du programme, évoquer ses limites
