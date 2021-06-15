# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 09:18:25 2021

@author: erics
"""

from textwrap import dedent
from login import Login
from etl import ETL
from macros import Macros
import os, sys
import edit

class UI():
    def __init__(self):
        self.menu = 'main'
        self.system = os.name
        self.stop = False
        self.user = ''
        self.password = ''
        self.loginController = Login()
        self.etlController = ETL()
        self.macroController = Macros()
        self.message = '' #envia uma mensagem para a próxima tela

    def start(self):
        while self.stop == False:
            if self.menu == 'main':
                self.mainMenu(self.message)
            elif self.menu == 'login':
                self.loginMenu(self.message)
            elif self.menu == 'signup':
                self.signupMenu(self.message)
            elif self.menu == 'main_logged':
                self.loggedMenu(self.message)
            elif self.menu == 'login_confs':
                self.confsMenu(self.message)
            elif self.menu == 'load_table':
                self.loadtableMenu(self.message)
            elif self.menu == 'export':
                self.exportMenu(self.message)
            elif self.menu == 'commands':
                self.commandsMenu(self.message)
            elif self.menu == 'exec_command':
                self.executeCommandMenu(self.message)

    def setMessage(self, message):
        self.message = message
    def resetMessage(self):
        self.message = ''
        
    def clear(self):
        os.system('cls' if self.system == 'nt' else 'clear')

    def logout(self):
        self.__init__()

    def getOption(self, text, options:list, message):
        choosen = None
        self.clear()
        print(message)
        self.resetMessage()
        while choosen not in options:
            print(dedent(text))
            choosen = input('Digite a opção desejada: ')
            if choosen not in options:
                self.clear()
                print('Opção inválida')
        return choosen

    def mainMenu(self, message):
        text = """
            Bem vindo ao Simple CLI ETL

            1 - Login
            2 - Cadastrar
            3 - Sair
            """
        option = self.getOption(text, ['1','2', '3'], message)
        if option == '1':
            self.menu = 'login'
        elif option == '2':
            self.menu = 'signup'
        elif option == '3':
            self.clear()
            self.stop = True
    
    def loginMenu(self, message):
        text = f"""
            Login

            1 - Definir usuário ({self.user})
            2 - Definir senha ({'*'*len(self.password)})
            3 - Logar
            4 - Voltar
            """
        option = self.getOption(text,['1','2','3','4'], message)
        if option == '1':
            self.clear()
            self.user = input('Digite o usuario: ')
        elif option == '2':
            self.clear()
            self.password = input('Digite a senha: ')
        elif option == '3':
            loginResponse = self.loginController.tryLogin(self.user, self.password)
            if loginResponse == -1:
                self.setMessage('Usuário não existe')
            elif loginResponse == -2:
                self.setMessage('Senha errada')
            elif loginResponse == 1:
                self.menu = 'main_logged'
        elif option == '4':
            self.menu = 'main'

    def signupMenu(self, message):
        text = f"""
            Cadastrar

            1 - Definir usuário ({self.user})
            2 - Definir senha ({'*'*len(self.password)})
            3 - Cadastrar
            4 - Voltar
            """
        option = self.getOption(text,['1','2','3','4'], message)
        if option == '1':
            self.clear()
            self.user = input('Digite o usuario: ')
        elif option == '2':
            self.clear()
            self.password = input('Digite a senha: ')
        elif option == '3':
            response = self.loginController.createLogin(self.user, self.password)
            if response == -3:
                self.setMessage('Usuário inválido')
            elif response == -4:
                self.setMessage('Senha inválida')
            elif response == -5:
                self.setMessage('Usuário já existe')
            elif response == 2:
                self.menu = 'login'
                self.setMessage('Cadastrado')
        elif option == '4':
            self.menu = 'main'

    def loggedMenu(self, message):
        text = f"""
            Olá {self.user}

            1 - Carregar tabela
            2 - Ver tabela
            3 - Comandos salvos
            4 - Escrever comando
            5 - Exportar tabela
            6 - Desfazer
            7 - Configurações de login
            8 - Deslogar
            9 - Sair
            """
        option = self.getOption(text,['1','2','3','4','5','6','7','8','9'], message)
        if option == '1':
            self.menu = 'load_table'
        elif option == '2':
            response = self.etlController.showTable()
            if type(response) == int and response == -5:
                self.setMessage('Tabela não carregada')
            else:
                '''path = os.path.abspath('table.html')
                url = 'file://' + path
                with open(path, 'w') as f:
                    f.write(response)
                    webbrowser.open(url)'''
                self.clear()
                input(response)
        elif option == '3':
            self.menu = 'commands'
        elif option == '4':
            self.menu = 'exec_command'
        elif option == '5':
            self.menu = 'export'
        elif option == '6':
            response = self.etlController.undo()
            if response == -9:
                self.setMessage('Impossível desfazer')
            elif response == 4:
                self.setMessage('Desfeito')
        if option == '7':
            self.menu = 'login_confs'
        if option == '8':
            self.logout()
        elif option == '9':
            self.clear()
            self.stop = True

    def confsMenu(self, message):
        text = f"""
            Configurações da conta

            1 - Alterar senha
            2 - Excluir conta
            3 - Voltar
            """
        option = self.getOption(text, ['1','2','3'], message)
        if option == '1':
            self.clear()
            newPassword = input('Digite a nova senha: ')
            response = self.loginController.changePassword(newPassword)
            if response == -4:
                self.setMessage('Senha inválida')
            elif response == -6:
                self.setMessage('É preciso logar antes')
            elif response == 4:
                self.setMessage('Senha alterada')
        elif option == '2':
            response = self.loginController.deleteUser()
            if response == -6:
                self.setMessage('É preciso logar antes')
            elif response == 5:
                self.setMessage('Usuário excluído')
                self.logout()
        elif option == '3':
            self.menu = 'main_logged'

    def loadtableMenu(self, message):
        text = f"""
            Carregamento de tabela

            1 - Carregar CSV
            2 - Carregar XLS
            3 - Carregar Json
            4 - Carregar Json da Web
            5 - Voltar
            """
        option = self.getOption(text, ['1','2','3','4','5'], message)
        if option == '1':
            self.clear()
            file = input('Digite o caminho do arquivo: ')
            self.clear()
            encoding = input('Digite o encoding (utf-8, latin-1): ')
            self.clear()
            separator = input('Digite o separador: ')
            response = self.etlController.loadCSV(file, encoding, separator)
            if response == -1:
                self.setMessage('Arquivo inválido')
            elif response == -2:
                self.setMessage('Encoding inválido')
            elif response == -3:
                self.setMessage('Separador inválido')
            elif response == -4:
                self.setMessage('Impossível carregar o arquivo')
            elif response == 1:
                self.menu = 'main_logged'
                self.setMessage('Tabela carregada')
        elif option == '2':
            self.clear()
            file = input('Digite o caminho do arquivo: ')
            response = self.etlController.loadXLS(file)
            if response == -1:
                self.setMessage('Arquivo inválido')
            elif response == -4:
                self.setMessage('Impossível carregar o arquivo')
            elif response == 1:
                self.menu = 'main_logged'
                self.setMessage('Tabela carregada')
        elif option == '3':
            self.clear()
            file = input('Digite o caminho do arquivo: ')
            self.clear()
            encoding = input('Digite o encoding (utf-8, latin-1): ')
            response = self.etlController.loadJSON(file, encoding)
            if response == -1:
                self.setMessage('Arquivo inválido')
            elif response == -4:
                self.setMessage('Impossível carregar o arquivo')
            elif response == 1:
                self.menu = 'main_logged'
                self.setMessage('Tabela carregada')
        elif option == '4':
            self.clear()
            url = input('Digite a url: ')
            response = self.etlController.loadJSONweb(url)
            if response == -6:
                self.setMessage('Impossível obter url')
            elif response == -7:
                self.setMessage('Impossível carregar conteúdo da url')
            elif response == 2:
                self.menu = 'main_logged'
                self.setMessage('Tabela carregada')
        elif option == '5':
            self.menu = 'main_logged'

    def exportMenu(self, message):
        text = """
            Exportação

            1 - CSV
            2 - XLS
            3 - JSON
            4 - Voltar
            """
        option = self.getOption(text, ['1','2','3','4'], message)
        if option == '1':
            self.clear()
            path = input('Digite o caminho do arquivo: ')
            self.clear()
            encoding = input('Digite o encoding (utf-8, latin-1): ')
            self.clear()
            separator = input('Digite o separador: ')
            response = self.etlController.exportCSV(path, encoding, separator)
            if response == -2:
                self.setMessage('Encoding inválido')
            elif response == -3:
                self.setMessage('Separador inválido')
            elif response == -8:
                self.setMessage('Impossível exportar a tabela')
            elif response == 3:
                self.menu = 'main_logged'
                self.setMessage('Tabela exportada')
        elif option == '2':
            self.clear()
            path = input('Digite o caminho do arquivo: ')
            self.clear()
            response = self.etlController.exportXLS(path)
            if response == -8:
                self.setMessage('Impossível exportar a tabela')
            elif response == 3:
                self.menu = 'main_logged'
                self.setMessage('Tabela exportada')
        elif option == '3':
            self.clear()
            path = input('Digite o caminho do arquivo: ')
            self.clear()
            response = self.etlController.exportJSON(path)
            if response == -8:
                self.setMessage('Impossível exportar a tabela')
            elif response == 3:
                self.menu = 'main_logged'
                self.setMessage('Tabela exportada')
        elif option == '4':
            self.menu = 'main_logged'

    def commandsMenu(self, message):
        text = """
            Comandos

            1 - Listar
            2 - Executar
            3 - Editar
            4 - Criar
            5 - Excluir
            6 - Voltar
            """
        option = self.getOption(text, ['1','2','3','4','5','6'], message)
        if option == '1':
            if self.loginController.loggedUser == None:
                self.setMessage('Nenhum usuario logado')
            else:
                try:
                    self.clear()
                    macros = self.macroController.getMacrosList(self.loginController.loggedUser)
                    if macros == None:
                        self.setMessage('Nenhuma macro')
                    else:
                        for m in macros:
                            print(m[0])
                        input('\nTecle enter para voltar...')
                except:
                    self.setMessage('Erro: Impossível listar macros')
        elif option == '2':
            if self.loginController.loggedUser == None:
                self.setMessage('Nenhum usuario logado')
            else:
                self.clear()
                name = input('Digite o nome da macro: ')
                try:
                    macro = self.macroController.getMacro(self.loginController.loggedUser, name)
                    if macro == -1:
                        self.setMessage('Não existe macro com esse nome')
                    else:
                        response = self.etlController.query(macro)
                        if response == -8:
                            self.setMessage('Impossível executar query')
                        elif response == 3:
                            self.setMessage('Query executada')
                except:
                    self.setMessage('Erro: Impossível executar macro')
        elif option == '3':
            if self.loginController.loggedUser == None:
                self.setMessage('Nenhum usuario logado')
            else:
                self.clear()
                name = input('Digite o nome da macro: ')
                try:
                    macro = self.macroController.getMacro(self.loginController.loggedUser, name)
                    if macro == -1:
                        self.setMessage('Não existe macro com esse nome')
                    else:
                        command = self.openEditor(macro)
                        response = self.macroController.updateMacro(self.loginController.loggedUser, name, command)
                        if response == -2:
                            self.setMessage('Impossível atualizar a macro')
                        elif response == 1:
                            self.setMessage('Macro atualizada')
                except:
                    self.setMessage('Erro: Impossível editar macro')
        elif option == '4':
            if self.loginController.loggedUser == None:
                self.setMessage('Nenhum usuario logado')
            else:
                self.clear()
                name = input('Digite o nome da macro: ')
                try:
                    macro = self.macroController.getMacro(self.loginController.loggedUser, name)
                    if macro != -1:
                        self.setMessage('Já existe macro com esse nome')
                    else:
                        command = self.openEditor()
                        response = self.macroController.createMacro(self.loginController.loggedUser, name, command)
                        if response == -3:
                            self.setMessage('Já existe macro com esse nome')
                        elif response == -4:
                            self.setMessage('Impossível criar macro')
                        elif response == 2:
                            self.setMessage('Macro criada')
                except:
                    self.setMessage('Erro: Impossível criar macro')
        elif option == '5':
            if self.loginController.loggedUser == None:
                self.setMessage('Nenhum usuario logado')
            else:
                self.clear()
                name = input('Digite o nome da macro: ')
                try:
                    macro = self.macroController.getMacro(self.loginController.loggedUser, name)
                    if macro == -1:
                        self.setMessage('Não existe macro com esse nome')
                    else:
                        response = self.macroController.deleteMacro(self.loginController.loggedUser, name)
                        if response == -1:
                            self.setMessage('Não existe macro com esse nome')
                        elif response == -5:
                            self.setMessage('Impossível excluir macro')
                        elif response == 3:
                            self.setMessage('Macro excluída')
                except:
                    self.setMessage('Erro: Impossível excluir macro')
        elif option == '6':
            self.menu = 'main_logged'


    def openEditor(self, txt=''):
        file = open('edit.txt', 'w')
        file.write(txt)
        file.close()
        edit.edit('edit.txt')
        file = open('edit.txt', 'r')
        lines = file.readlines()
        text = ' '.join(lines).replace('\n','')
        return text
        

    def executeCommandMenu(self, message):
        '''self.clear()
        print('Escreva o comando, para sair use a sequência de teclas:')
        print('Windows: CTRL+Z\nUNIX: CTRL+D\n')
        read = sys.stdin.readlines()
        command = ' '.join(read).replace('\n','')'''
        command = self.openEditor()
        response = self.etlController.query(command)
        if response == -8:
            self.setMessage('Impossível executar query')
        elif response == 3:
            self.setMessage('Query executada')
        self.menu = 'main_logged'

        
        
            
ui = UI()
ui.start()
