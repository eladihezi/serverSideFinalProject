
import MySQLdb

class MyConnectionDBClass():
    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1","root","root",'test1' )
        self.cursor = self.db.cursor()

    def InsertQuery(self,query):
        #example : query = ("INSERT INTO employees( firstname, lastname) VALUES (\"IGOR1\",\"MAMORSKI1\");")
        #cursor.execute(query)
        #db.commit()
        return "TODO"
    
    def SelectQuery(self,query):
        #example : query = ("SELECT * FROM employees ;")
        result = "error"
        try :
            self.cursor.execute(query)
            result = self.cursor
        except : 
            pass
        return result

    def __del__(self):
        self.cursor.close()
        self.db.close()
        print ( 'died')



