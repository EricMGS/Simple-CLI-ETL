# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 19:06:54 2021

@author: erics
"""

import pandas as pd
import numpy as np
import requests
import pandasql as ps
import csv

class ETL():
    def __init__(self):
        self.table = None
        self.previous = None
        #pd.options.display.width = 0

    def loadCSV(self, file:str, encoding:str, separator:str) -> int:
        try:
            open(file, 'r')
        except:
            return -1 #arquivo inválido
        if encoding not in ['utf-8','latin-1']:
            return -2 #encoding inválido
        if len(separator) != 1:
            return -3 #separador inválido
        try:
            self.table = pd.read_csv(file, encoding=encoding, sep=separator, quoting=csv.QUOTE_ALL)
            self.table = self.table.replace(np.nan, '', regex=True)
            return 1 #arquivo aberto com sucesso
        except:
            return -4 #impossível abrir o arquivo
        
        
    def loadXLS(self, file:str) -> int:
        try:
            open(file, 'r')
        except:
            return -1 #arquivo inválido
        try:
            self.table = pd.read_excel(file)
            self.table = self.table.replace(np.nan, '', regex=True)
            return 1 #arquivo aberto com sucesso
        except:
            return -4 #impossível abrir o arquivo
        
    def loadJSON(self, file:str, encoding:str) -> int:
        try:
            open(file, 'r')
        except:
            return -1 #arquivo inválido
        if encoding not in ['utf-8','latin-1']:
            return -2 #encoding inválido
        try:
            self.table = pd.read_json(file, encoding=encoding)
            self.table = self.table.replace(np.nan, '', regex=True)
            return 1 #arquivo aberto com sucesso
        except:
            return -4 #impossível abrir o arquivo

    def loadJSONweb(self, url:str) -> int:
        try:
            response = requests.get(url=url)
        except:
            return -6 #impossível obter url
        try:
            data = response.json()
            self.table = pd.DataFrame(data, index=[0])
            self.table = self.table.replace(np.nan, '', regex=True)
            return 2 #url carregada com sucesso
        except:
            return -7 #impossível carregar conteúdo

    def loadHTML(self, html:str) -> int:
        try:
            self.table = pd.read_html(html)[0]
            self.table = self.table.replace(np.nan, '', regex=True)
            return 1 #arquivo aberto com sucesso
        except:
            return -4 #impossível abrir o arquivo

    def showTable(self):
        if type(self.table) != pd.DataFrame:
            return -5 #tabela não carregada
        #return self.table.to_html()
        return self.table

    def exportCSV(self, path, encoding, separator):
        if encoding not in ['utf-8','latin-1']:
            return -2 #encoding inválido
        if len(separator) != 1:
            return -3 #separador inválido
        try:
            self.table.to_csv(path+'.zip', encoding=encoding, sep=separator, compression='zip')
            return 3 #arquivo exportado com sucesso
        except:
            return -8 #impossível exportar o arquivo

    def exportXLS(self, path):
        try:
            self.table.to_excel(path)
            return 3 #arquivo exportado com sucesso
        except:
            return -8 #impossível exportar o arquivo

    def exportJSON(self, path):
        try:
            self.table.to_json(path+'.zip', compression='zip')
            return 3 #arquivo exportado com sucesso
        except:
            return -8 #impossível exportar o arquivo


    def query(self, q):
        tabela = self.table
        self.previous = tabela
        try:
            self.table = ps.sqldf(q)
            return 3 #query executada
        except:
            return -8 #Impossível executar query

    def undo(self):
        if self.table.equals(self.previous):
            return -9 #impossível desfazer
        self.table = self.previous
        return 4 #desfeito
        
