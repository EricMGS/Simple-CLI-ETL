# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 09:18:53 2021

@author: erics
"""

import psycopg2

class Login():
    def __init__(self):
        self.loggedUser = None
        self.conn = psycopg2.connect("host=localhost dbname=trabpython user=postgres password=root")
        self.cur = self.conn.cursor()
    
    def tryLogin(self, user:str, password:str) -> int:
        self.cur.execute(f"SELECT * FROM login WHERE username='{user}'")
        result = self.cur.fetchone()
        if result == None:
            return -1 #Usuario não existe
        if result[2] != password:
            return -2 #Senha errada
        self.loggedUser = user
        return 1 #Login bem sucedido

    def createLogin(self, user:str, password:str) -> int:
        if user == '':
            return -3 #Usuário inválido
        if password == '':
            return -4 #Senha inválida
        self.cur.execute(f"SELECT * FROM login WHERE username='{user}'")
        result = self.cur.fetchone()
        if result != None:
            return -5 #Usuario já existente
        self.cur.execute(f"INSERT INTO login(username,password) VALUES('{user}','{password}')")
        self.conn.commit()
        return 2 #Criação de usuário bem sucedida

    def logout(self):
        if self.loggedUser == None:
            return -6 #Não loggado
        self.loggedUser = None
        return 3 #Logout bem sucedido

    def changePassword(self, newPassword:str) -> int:
        if self.loggedUser == None:
            return -6 #Não loggado
        if newPassword == '':
            return -4 #Senha inválida
        self.cur.execute(f"UPDATE login SET password={newPassword} where username='{self.loggedUser}'")
        self.conn.commit()
        return 4 #Senha alterada

    def deleteUser(self) -> int:
        if self.loggedUser == None:
            return -6 #Não loggado
        self.cur.execute(f"DELETE FROM login WHERE username='{self.loggedUser}'")
        self.conn.commit()
        self.loggedUser =  None
        return 5 #Usuário deletado
