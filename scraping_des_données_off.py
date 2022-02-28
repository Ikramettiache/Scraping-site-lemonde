# -*- coding: utf-8 -*-
"""Scraping des données Off

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/182YplS88Fw6mjpa4QcF3Mt98uqiY0Fke
"""

pip install bs4

pip install dateparser

import logging

#Importer les packages nécessaires
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import datetime as dt
from pandas.core.frame import DataFrame
import dateparser

# récupérer le code HTML sous format text
def get_text(s):
   url="https://www.lemonde.fr/recherche/?search_keywords=crise&start_at=08/01/2022&end_at=08/02/2022&search_sort=date_desc&page="+str(s)
   rep = requests.get(url)
   if rep.ok:
     soup=BeautifulSoup(rep.text)
   else :
    print(" Erreur Request get")
  # if rep not ok ==> rep.text = ?  
   return rep.text

#Récupérer temps de lecture, catégorie, date de publication
def get_read_time_categorie(url2):
    catégorie=''
    date_de_publication=''
    temps_de_lecture=''
    rep = requests.get(url2)
    soup2=BeautifulSoup(rep.text)
    p=soup2.find('p',{'class':"meta__reading-time"})
    s=soup2.find('span',{'class':"meta__reading-time"})
    if p:
      temps_de_lecture=(re.sub("temps de lecture[-_/./,]*","",p.get_text().lower()))
    if s:
      # if p and s,first temps_de_lecture will  be overridden 
      temps_de_lecture=(re.sub("temps de lecture[-_/./,]*","",s.get_text().lower()))
    sections=soup2.findAll('section', {'class': True})
    for section in sections:
      if('zone' or 'article' or ('meta' and 'date') in section['class']):
        aa=section.findAll('a',{'class': True})
        span_date=section.findAll('span',{'class': 'meta__date'})
        for a in aa :
            if(("logo" or "article") in a['class'][0]):
              catégorie=a.text
              break
        for span in span_date:
           date_de_publication=dateparser.parse(re.sub("publié|le|à|[-_/./,]*|mis(e)* à* jour.*",'',(span.text).lower()))
      return catégorie,date_de_publication,temps_de_lecture

#Récupérer title2 depuis URL de l'article
def get_title_2(url):
  title2=''
 # p='-*[A-ZA-z0-9]+-[A-Za-z0-9]+'
  pattern='(/article/)([0-9]+/)+(-*[A-ZA-z0-9]+-[A-Za-z0-9]+)+_'
  m=re.search(pattern,url)
  if m:
    title2=re.sub('(/article/)([0-9]+/)+|-|_',' ',m.group())
    # return re.sub('(/article/)([0-9]+/)+|-|_',' ',m.group()).strip() -- bla matzidi title2
  return title2.strip()

#Récupérer title1, lien de l'article ainsi que les autres attributs et  les stocker dans une dataframe
def get_all_line_dataframe(rep,df):
  title=''
  categorie=date_de_publication=read_time=''
  soup=BeautifulSoup(rep)
  sections=soup.findAll('section')
  for section in sections:
    if(section['class'][0]=="teaser"):
        aa=section.findAll('a')
        titles=section.findAll('h3')
        for a in aa:
          urla=a['href']
          if '/article/'in a['href']:
            categorie,date_de_publication,read_time=get_read_time_categorie(urla)
            # else blach makadir walo
          else :
            continue
        for title in titles:
          title=title.text
    if categorie.strip()=='Économie'and not (pd.Series([title]).isin(df.title)[0]):
     title2=get_title_2(a['href'])
     df=df.append(
    {"title": title,
     "title2":title2,
     "categorie": categorie,
     "date":date_de_publication,
     "read":read_time,
     "lien":a['href']
     }, ignore_index=True)
        # had condition zidiha m3a if lawla and w safi  
     if(len(df)>=2):
       break
  return df

def main():
  df = pd.DataFrame(columns=['title','categorie','date','read','lien','title2'])
  s=1
  # hadi diriha 
  # for index in range(len(df)):
  #    df=get_all_line_dataframe(get_text(index),df)
  while len(df)<5:
    rep=get_text(s)
    df=get_all_line_dataframe(rep,df)
    s=s+1
    sh=logging.debug(df)

if __name__ == "__main__":
    main()

df = pd.DataFrame(columns=['title','categorie','date','read','lien','title2'])
s=1
  # hadi diriha 
  # for index in range(len(df)):
  #    df=get_all_line_dataframe(get_text(index),df)
while len(df)<2: 
    df=get_all_line_dataframe(get_text(s),df)
s=s+1
sh=logging.debug(df)

logging.info(sh)
logging.debug(df)

#Enregistrer dans un csv et créer dossier si not exist
import os

outname = 'myData.csv'

outdir = r'C:\file_csv'
if not os.path.exists(outdir):
    os.mkdir(outdir)

fullname = os.path.join(outdir, outname)    
with open(fullname, 'a') as f:
    df.to_csv(f, header=f.tell()==0,index=False)