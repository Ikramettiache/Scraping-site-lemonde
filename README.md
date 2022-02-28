# Scraping-site-lemonde

L'objectif est de récupérer sur le site lemonde.fr les 50 articles les plus récents qui  :
    - résultent de la recherche du mot clé "crise"
    - font partie de la catégorie " Économie" 

Pour chaque article, on récupérera dans un DataFrame Pandas (avec une ligne par article)
- le titre (nom de colonne "title")
- l'URL (nom de colonne "URL")
- le temps de lecture (nom de colonne "reading_time")
- Obtenir le temps de lecture médian, ainsi que le nombre d'articles par temps de lecture.
- Retrouver les titres d'article à partir des URL (via des expressions régulières, créer une colonne "title_2")
- Ajouter une colonne avec la date de chaque article, au format pertinent
