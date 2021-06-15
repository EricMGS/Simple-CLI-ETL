import psycopg2

class Macros():
    def __init__(self):
        self.conn = psycopg2.connect("host=localhost dbname=trabpython user=postgres password=root")
        self.cur = self.conn.cursor()

    def getMacrosList(self, user):
        self.cur.execute(f"SELECT command_name FROM macros WHERE username='{user}'")
        return self.cur.fetchall()
    
    def getMacro(self, user, name):
        self.cur.execute(f"SELECT command FROM macros WHERE username='{user}' and command_name='{name}'")
        result = self.cur.fetchone()
        if result == None:
            return -1 #Não existe macro com esse nome
        return result[0]

    def updateMacro(self, user, name, new:str):
        self.cur.execute(f"SELECT command FROM macros WHERE username='{user}' and command_name='{name}'")
        result = self.cur.fetchone()
        if result == None:
            return -1 #Não existe macro com esse nome
        try:
            self.cur.execute(f"UPDATE macros SET command='{new}' WHERE username='{user}' AND command_name='{name}'")
            self.conn.commit()
            return 1 #macro atualizada
        except:
            self.conn.rollback()
            return -2 #impossível atualizar macro

    def createMacro(self, user, name, new:str):
        self.cur.execute(f"SELECT command FROM macros WHERE username='{user}' and command_name='{name}'")
        result = self.cur.fetchone()
        if result != None:
            return -3 #Macro já existe
        try:
            self.cur.execute(f"INSERT INTO macros(username,command,command_name) VALUES('{user}','{new}','{name}')")
            self.conn.commit()
            return 2 #macro adicionada
        except:
            self.conn.rollback()
            return -4 #impossível adicionar macro

    def deleteMacro(self, user, name):
        self.cur.execute(f"SELECT command FROM macros WHERE username='{user}' and command_name='{name}'")
        result = self.cur.fetchone()
        if result == None:
            return -1 #Não existe macro com esse nome
        try:
            self.cur.execute(f"DELETE FROM macros WHERE username='{user}' and command_name='{name}'")
            self.conn.commit()
            return 3 #macro excluida
        except:
            self.conn.rollback()
            return -5 #impossível excluir macro
