import urllib.request
from bs4 import BeautifulSoup
import nltk
import string
from nltk.probability import FreqDist #para a lista de frequencia
from collections import defaultdict
from heapq import nlargest
from nltk.corpus import wordnet as wn
import mysql.connector
from datetime import datetime
from datetime import date


class Crawler:



    def tratarcampo(self,campo, valor):
        print("Campo e valor NOVO:::-:::::: >>>>>> ")
        matriz = []
        matriz = str(campo).split(',')
        print("EXIBE A MATRIZ:::")
        print(matriz)
        if len(matriz) == 0:
            if valor != "":
                matriz.append(valor)
        else:
            valor = str(valor)
            if valor not in matriz:
                matriz.append(valor)

        mstr = ''
        for m in matriz:
            if m != "":
                mstr += str(m) + ','
        return mstr



    def inserirStemmer(self,mid,palavrastokens):
        docs = ''
        connection  = self.conectarbanco()
        cursor = connection.cursor()
        for pal in palavrastokens:
            print(pal)
            cursor.execute("SELECT * FROM dados_grama where palavra = '"+pal+"'")
            resultado = cursor.fetchall()
            print("RESULTADOOOOOOOOOOOOOOOOOOOOOOOOOO -----> ")
            print(resultado)

            if not resultado:
                sql = "INSERT INTO dados_grama (palavra, documentos) VALUES (%s, %s)"
                data = (
                    pal,
                    mid
                )
                cursor.execute(sql, data)
                connection.commit()
            else:
                for resultadob in resultado:
                    print(resultadob[0])
                    print(resultadob[1])
                    print(resultadob[2])
                    print("mostra o ID ::: ")
                    print(mid)
                    # chama a função para tratar o campo com os ids.
                    adicionarValor = self.tratarcampo(resultadob[2],mid)
                    sql_update = """Update dados_grama set documentos = %s where id = %s"""
                    data = (adicionarValor,resultadob[0])
                    cursor.execute(sql_update,data)
                    connection.commit()
                    # -----------------------------

    def conectarbanco(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mestrado_chatbot"
        )
        return connection

    def gravarDB(self,data,hora,titulo,resumo,dataatual,stops):
        connection = self.conectarbanco() #pega a conexão com o banco de dados
        cursor = connection.cursor()
        sql = "INSERT INTO dados_chatbot (data, hora, titulo,resumo,data_cadastro) VALUES (%s, %s, %s, %s, %s)"
        data = (
            data,
            hora,
            titulo,
            resumo,
            dataatual
        )
        cursor.execute(sql, data)
        connection.commit()
        mid = cursor.lastrowid
        print(mid)
        cursor.close()
        connection.close()
        self.inserirStemmer(mid,stops)

    def definedata(self,data):
        # quebrando a data :::
        data = str(data)
        datab = data.split(" ")
        print("DATA GLOBOOOOOOOO")
        print(datab)
        print(datab[3])
        datadados = datab[2].split('/')
        datadadosb = datadados[2] + '-' + datadados[1] + '-' + datadados[0]
        return datadadosb


    def definehora(self,data):
        # quebrando a data :::
        data = str(data)
        datab = data.split(" ")

        print("DTAAA")
        print(datab)
        print(datab[3])
        datadados = datab[2].split('/')
        datadadosb = datadados[2] + '-' + datadados[1] + '-' + datadados[0]
        print(datadadosb)
        hora = datab[3].split('h')
        novahora = hora[0] + ':' + hora[1]
        return novahora


    def definedataCNN(self,data):
        # quebrando a data :::
        data = str(data)
        datab = data.split(" ")
        datadados = datab[0].split('/')
        datadadosb = datadados[2] + '-' + datadados[1] + '-' + datadados[0]
        return datadadosb

    def definehoraCNN(self,data):
        # quebrando a data :::
        data = str(data)
        datab = data.split(" ")
        novahora = datab[1]
        return novahora

    def palavrasteamer(self,palavras):
        stemmer = nltk.stem.RSLPStemmer()
        for p in palavras:
            print(p, " : ", stemmer.stem(p))

    def quebrar_nltk(self,texto,titulo,data,hora,stopwords):
        minhas_sentencas = nltk.sent_tokenize(texto)
        palavras_tokenizadas = nltk.word_tokenize(texto.lower())
        palavras_sem_stopwords = [palavra for palavra in palavras_tokenizadas if palavra not in stopwords]
        tagged = nltk.pos_tag(palavras_sem_stopwords)
        entities = nltk.chunk.ne_chunk(tagged)
        self.palavrasteamer(palavras_sem_stopwords)
        repeticoes = FreqDist(palavras_sem_stopwords)
        sentencas_importantes = defaultdict(int)
        for i, sentenca in enumerate(minhas_sentencas):
            for palavra in nltk.word_tokenize(sentenca.lower()):
                if palavra in repeticoes:
                    sentencas_importantes[i] += repeticoes[palavra]
        idx_sentencas_importantes = nlargest(2, sentencas_importantes, sentencas_importantes.get)
        resumo = ''
        for i in sorted(idx_sentencas_importantes):
            resumo = resumo + minhas_sentencas[i]+ '\r\n'
        print(resumo)

        #quebrando a data :::
        data  = str(data)
        datadadosb = data
        print(datadadosb)
        novahora = hora
        #formatando a data
        hoje = datetime.now()
        data_hora_atual = hoje.strftime("%Y-%m-%d, %H:%M:%S")
        print(data_hora_atual)
        self.gravarDB(datadadosb,novahora,titulo,resumo,data_hora_atual,palavras_sem_stopwords)
