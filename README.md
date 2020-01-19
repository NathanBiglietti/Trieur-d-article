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

Une fonction a été créée pour chacune de ces tâches. J'expliquerais donc le fonctionnement de chacune d'entre elles avant de commenter les instructions et l'exécution du programme et de conclure.

## 1) pdfparser
La majorité des articles scientifiques disponibles sur internet étant disponible au format pdf, j'ai décidé de travailler à partir de ce format.
Une difficulté s'est rapidement présentée à moi. Les pdfs sont en effet des fichiers binaires et non pas des fichiers textes, ce qui a pour conséquence que le contenu textuel d'un pdf n'est pas directement accessible. 

Pendant mes recherches, je suis tombé dans un forum (https://www.developpez.net/forums/d1599202/autres-langages/python/general-python/extraire-contenu-d-pdf-python/) sur ce message qui a failli me faire abandonner l'idée de travailler directement à partir du pdf : 

    "PDF is evil. Although it is called a PDF "document", it's nothing like Word or HTML document. PDF is 
    more like a graphic representation. PDF contents are just a bunch of instructions that tell how to place
    the stuff at each exact position on a display or paper. In most cases, it has no logical structure such 
    as sentences or paragraphs and it cannot adapt itself when the paper size changes. PDFMiner attempts to
    reconstruct some of those structures by guessing from its positioning, but there's nothing guaranteed to
    work. Ugly, I know. Again, PDF is evil."

Mon niveau en programmation ne me permettant pas de jouer avec le diable mais ne voyant aucun intérêt à un programme qui m'obligerais à convertir préalablement les pdf en txt avec un convertisseur en ligne pour ensuite devoir routrouver les pdfs correspondant aux fichiers txt mis dans le dossier (autant lire les abstracts si c'est pour faire tout ça), j'ai finalement décidé de subtiliser une fonction trouvé sur un autre forum (https://stackoverflow.com/questions/25665/python-module-for-converting-pdf-to-text) que j'ai légèrement adapté afin de le rendre plus compréhensible.

La fonction se présente comme il suit : 
```
def pdfparser(article):
    #extrait le contenu textuel d'un pdf 
    fp = open(article, 'rb')
    manager = PDFResourceManager()
    retstr = io.StringIO()
    laparams = LAParams()
    device = TextConverter(manager, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(manager, device)
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        texte_brut =  retstr.getvalue()
    return texte_brut
```
Pour faire simple, pdfparser ouvre un article dont on lui indique le path en argument, pour ensuite interpréter page par page le pdf et enfin retourner le texte brut. La fonction "TextConverter" permet ici de spécifier dans la fonction "PDFPageInterpreter" le mode d'interprétation des pages analysées, indiquant que l'on souhaite extraire le contenu textuel du pdf. Par ailleurs, l'objet retstr indique ici que l'on souhaite retourner une chaine de caractères (string). 

Pour être tout à fait honnête avec vous, le rôle des autres arguments nécessaires au fonctionnement de "TextConverter" (à savoir "manager" et "laparams") reste pour moi assez obscur. Peu d'informations sont en effet disponibles sur internet, à part des examples ne m'avançant pas à grand chose, ce qui a limité ma compréhension des fonctions de PDFMiner dans la limite du temps imparti. J'ai néanmoins préféré poursuivre avec une fonction plus ou moins obscure plutôt que de changer de projet. 

## 2) pre_traitement
Le contenu textuel extrait par pdfparser est un texte brut dont la structure ne permet pas encore le traitement souhaité. En effet, il présente : 
1. Des signes de ponctuations et d'autres symboles non alphabétiques. Ceux ci ne sont d’aucun intérêt pour la tâche qui nous occupe.
2. Des mots dont la certaines lettres sont en majuscule. Ces mots seront traités comme différents que leur version tout en minuscule, ce qui biaiserait la tâche que nus souhaitons accomplir. 
3. Le texte est présenté comme un bloc (une seule chaine de caractère ou string), alors que nous souhaitons cibler un mot en particulier.

Il est donc nécessaire de traiter le texte brut pour le transformer en une liste de mots (isolés les uns des autres comme différentes chaines de caractères contenus dans la liste) tout en minuscule et ne présentant aucun symbole non alphabétique. Pour ce faire, j’ai utilisé le package nltk (Natural Language Toolkit). 

La fonction se présente de la façon suivante : 
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
Ici, la fonction "RegexpTokenizer" nous permet ici de désigner un mode de tokénisation du texte brut. Autrement dit, elle nous permet d'indiquer quelle règle sera suivie de façon systématique pour créer les sous chaines de caractères de la nouvelle liste sur la base du texte brut (qui on le rappelle, consiste en une seule et unique chaine de caractères). Ici l’argument "w+" permet d’indiquer que l’on ne retiendra que les mots, ce qui nous permet non seulement d'isoler les mots les uns des autres (chacun correspodant alors à une chaine de caractère), mais également de retirer les symboles non alphabétiques. En utilisant ce tokenizer que nous avons défini en appliquant au texte la méthode .tokenize() liée au tokenizer, nous pouvons alors créer une liste de mots isolés les uns des autres.

À ce stade, on obtient donc une liste contenant des mots dont certains peuvent toujours contenir des lettres majuscules. Pour palier à ce problème, j'ai créé une boucle for ajoutant grace à la méthode .append() à une liste vide ("words") les mots de la liste "tokens" mis en minuscule grace à la méthode .lower(). La fonction retourne alors une liste de mots tour en minuscule.

Une autre tâche classique de prétraitement de texte avec nltk consiste à retirer les stopwords, c'est à dire les mots courant tels que "ce", "un", "ou", qui ne sont pas porteurs de sens. Bien qu'ils ne soient pas utiles à notre tâche, il ne me semblait pas fondamentalement nécessaire de retier ces stopwords. De plus, je souhaitais que le programme puisse fonctionner autant sur des articles en anglais que sur des articles en français, ce qui aurait rendu compliqué la tâche si j'avais souhaité retirer les stopwords, puisqu'il aurait été nécessaire de détecter la langue afin de savoir quelle liste de stopwords utiliser, ou alors de retirer les stopwords des deux langues, ce qui pourrait potentiellement biaiser la tâche (par exemple si je cherche des articles en français sur le sens de l'agentivité dans le sport collectif et que j'ulitise le mot "but" comme mot clef, celui si serait retiré de la liste parce qu'il s'agit d'un stopword anglais). 

## 3) keyword_test

```
def keyword_test(liste_d_articles, key, nombre):
    #crée une liste contenant tous les acticles dont l'occurence du mot clef dans les 500 premiers mots est supérieure au         nombre souhaité 
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

## 5) Instructions 

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
## 6) Execution 

## Conclusion

conclure sur la réalisation et le fonctionnement du programme, évoquer ses limites

retirer les stop words + 500 mots + words.lower (sur tout les mots, plus efficace boucle if) = plus de rapidité 

pb des premières pages 

