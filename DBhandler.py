
import MySQLdb

class MyConnectionDBClass():
    """
    handling with queries to DATABASE  
    """

    # default connection DB and local cursor 
    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1","root","root",'projectdb' )
        self.cursor = self.db.cursor()

    # insert/delete/update type of query cand be sent here
    # example : query = ("INSERT INTO employees( firstname, lastname) VALUES (\"IGOR1\",\"MAMORSKI1\");")
    def InsertQuery(self,query):       
        try:
            self.cursor.execute(query)
            self.db.commit()
            return "Success"
        except:
            pass
        return False

    # select type of query 
    # example : query = ("SELECT * FROM employees ;")
    def SelectQuery(self,query):       
        result = "error"
        try :
            self.cursor.execute(query)
            result = self.cursor
        except : 
            pass
        if(self.cursor.rowcount == 0):
            return False
        return result

    # when we want to close the connection
    def __del__(self):
        self.cursor.close()
        self.db.close()



