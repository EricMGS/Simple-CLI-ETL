import psycopg2

class Tables():
    def __init__(self):
        self.conn = psycopg2.connect("host=localhost dbname=trabpython user=postgres password=root")
        self.cur = self.conn.cursor()

    def getTablesList(self, user):
        self.cur.execute(f"SELECT table_name FROM savedtables WHERE username='{user}'")
        return self.cur.fetchall()
    
    def getTable(self, user, name):
        self.cur.execute(f"SELECT table_html FROM savedtables WHERE username='{user}' and table_name='{name}'")
        result = self.cur.fetchone()
        if result == None:
            return -1 #Não existe tabela com esse nome
        return result[0]

    def updateTable(self, user, name, new):
        new = new.replace("'","&#39;")
        self.cur.execute(f"SELECT table_html FROM savedtables WHERE username='{user}' and table_name='{name}'")
        result = self.cur.fetchone()
        if result == None:
            return -1 #Não existe tabela com esse nome
        try:
            self.cur.execute(f"UPDATE savedtables SET table_html='{new}' WHERE username='{user}' AND table_name='{name}'")
            self.conn.commit()
            return 1 #tabela atualizada
        except:
            self.conn.rollback()
            return -2 #impossível atualizar tabela

    def createTable(self, user, name, new):
        new = new.replace("'","&#39;")
        self.cur.execute(f"SELECT table_html FROM savedtables WHERE username='{user}' and table_name='{name}'")
        result = self.cur.fetchone()
        if result != None:
            return -3 #tabela já existe
        try:
            self.cur.execute(f"INSERT INTO savedtables(username,table_html,table_name) VALUES('{user}','{new}','{name}')")
            self.conn.commit()
            return 2 #tabela adicionada
        except:
            self.conn.rollback()
            return -4 #impossível adicionar tabela

    def deleteTable(self, user, name):
        self.cur.execute(f"SELECT table_html FROM savedtables WHERE username='{user}' and table_name='{name}'")
        result = self.cur.fetchone()
        if result == None:
            return -1 #Não existe tabela com esse nome
        try:
            self.cur.execute(f"DELETE FROM savedtables WHERE username='{user}' and table_name='{name}'")
            self.conn.commit()
            return 3 #tabela excluida
        except:
            self.conn.rollback()
            return -5 #impossível excluir tabela
