import urllib.request
from bs4 import BeautifulSoup
import nltk
import string
from nltk.probability import FreqDist #para a lista de frequencia
from collections import defaultdict
from heapq import nlargest
from nltk.corpus import wordnet as wn
import pymysql
import mysql.connector
from classcrawler import Crawler
from datetime import datetime
from datetime import date

stopwords = set(nltk.corpus.stopwords.words('portuguese') + list(string.punctuation))


def abrirLinkGlobo(mlink,titulo,crawler):
    crawler = Crawler()
    html2 = urllib.request.urlopen(mlink)
    objPagina2 = BeautifulSoup(html2, features="html.parser")
    conteudo = objPagina2.findAll("p",{"class":"content-text__container"})
    dataPub = objPagina2.find("p",{"class":"content-publication-data__updated"})

    datab = dataPub.getText()
    data = crawler.definedata(datab)
    hora = crawler.definehora(datab)

    texto_completo = ''
    for g in conteudo:
        texto_completo = texto_completo + g.getText()
    crawler.quebrar_nltk(texto_completo,titulo,data,hora,stopwords)
    print("")

# ------------------------- Executa link da Página Principal
def crawlerGlobo():
    html = urllib.request.urlopen("https://g1.globo.com/bemestar/vacina/index.ghtml")
    objPagina = BeautifulSoup(html,features="html.parser")
    links = objPagina.findAll("a",{"class":"feed-post-link"})
    for x in links:
        #print('PEGANDO O TITULO'+x.getText())
        if 'href' in x.attrs:
            abrirLinkGlobo(x.attrs['href'],x.getText(),stopwords)


##  -------------------------------------------------------------------------
# https://www.cnnbrasil.com.br/tudo-sobre/coronavirus/

def abrirLinkCNN(mlink,titulo,crawler):
    crawler = Crawler()
    html2 = urllib.request.urlopen(mlink)
    objPagina2 = BeautifulSoup(html2, features="html.parser")
    conteudo = objPagina2.findAll("p",{"class":"post__excerpt"})
    #print(conteudo)
    dataPub = objPagina2.find("span",{"class":"post__data"})
    datab = dataPub.getText().split()
    dataformatada = datab[0]+' '+datab[2]
    data = crawler.definedataCNN(dataformatada)
    hora = crawler.definehoraCNN(dataformatada)
    texto_completo = ''
    for g in conteudo:
        texto_completo = texto_completo + g.getText()
    print(texto_completo)
    crawler.quebrar_nltk(texto_completo,titulo,data,hora,stopwords)
    #print("")

def crawlerCNN():
    html = urllib.request.urlopen("https://www.cnnbrasil.com.br/tudo-sobre/coronavirus/")
    objPagina = BeautifulSoup(html,features="html.parser")
    links = objPagina.findAll("a",{"class":"home__list__tag"})
    for x in links:
        #print('PEGANDO O TITULO'+x.getText())
        if 'href' in x.attrs:
            print(x.attrs['href'])
            abrirLinkCNN(x.attrs['href'],x.getText(),stopwords)

## EXECUTANDO A CHAMADA PARA O CRAWLER DAS NOTICIAS DA GLOBO SOBRE AS VACINAS.
crawlerGlobo()
crawlerCNN()