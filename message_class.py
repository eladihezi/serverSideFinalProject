
import json
import functions_file 
import DBhandler
import defineCommands

class globalMessage():
    """
    The globalMessage class is for client/server connect the server to the logic in functions_file
    and return the client the Data as json or boolean
    """

    # constructor is reserved for future use
    def __init__( self,id_request,Data):
        print ("id : " ,id_request ,"Data : ",Data)
        self.id_request = id_request
        self.Data = json.loads(Data)

    # handle print good looking
    def __str__(self):
        return ("id = {} data = {}".format(*(self.id_request,self.Data)))

    # call the right function by id_request 
    def runbyid(id_r,data):
        my_str = getattr(functions_file, defineCommands.dict_commands[int(id_r)])(json.loads(data))
        return my_str



