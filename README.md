# Trieur d'article

## Introduction 
L'idée de ce programme m'est venue en constatant les conséquences de mon téléchargement compulsif d'articles que je n'ai en général pas le temps de lire.
En effet, au fur et à mesure, s'accumulent dans un dossier "à lire" des articles dont je n'ai plus aucune idée du contenu. 
Parfois cependant, lorsqu'un temps libre se présente devant moi ou qu'une soif de connaissance m'assailli à 2h du matin alors que je devrais dormir, il m'arrive d'ouvrir cette caverne d'Alibaba qu'est ce dossier "à lire". 
Le problème est le suivant : à ce moment précis, ma curiosité se restreint à une certaine gamme limité de thématiques. 
Pour trouver la perle rare correspondant à mes attentes parmis les inombrables articles du dossier, il est alors nécessaire d'ouvrir un par un les articles, d'en lire l'astract jusqu'à ce qu'on trouve le bon. Une tâche ennuyeuse et rébarbative qui parfois (surtout à 2h du matin), me démotive finalement de la lecture. Automatiser celle ci s'est donc présenté très natuerellement comme une nécessité. 

L'intérêt du programme que j'ai créé est donc de pouvoir y voir clair dans cet amoncellement d'articles qu'un cerveau paresseux n'a aucun intérêt à trier. Pour ce faire, l'idée était de générer au sein du dossier "à lire" des sous dossiers contenant tous les articles présentant dans les premiers 500 mots un occurence donnée (*n*) d'un mot clef donné (*x*). À partir de ces deux informations renseignées dans la console, le programme doit donc : 
1. Extraire le contenu textuel 
