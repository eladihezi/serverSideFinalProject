
import json
import functions_file 
import DBhandler

class globalMessage():
    """
    The globalMessage class is for client/server .
    """


    def __init__( self,id_request,Data):
        print ("id : " ,id_request ,"Data : ",Data)
        self.id_request = id_request
        self.Data = json.loads(Data)
    
    def __str__(self):
        return ("id = {} data = {}".format(*(self.id_request,self.Data)))


    #call the right function by its id
    def runbyid(self):
        my_str = getattr(functions_file, 'func' + str(self.id_request))(self.Data)
        print ("my_str = ",my_str)
        return my_str

    def runbyidtry(id_r,data):
        my_str = getattr(functions_file, 'func' + str(id_r))(json.loads(data))
        return my_str



