import socketserver
import socket


import time
import logging
import sys

#local files
import message_class
import settings

import DBhandler

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP




class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        arr = self.data.decode("utf-8").split(";")
        status = message_class.globalMessage.runbyidtry(arr[0],arr[1])
        
        #print ("sending back ",status)
        
        mymsg  = str(len(str(status))) + ';' + str(status)
        #print ("mymsg is ",mymsg ,str(status))
        # if(type(status) == type(True)):
        #     self.request.send(bytes(status))
        #     return status
        #time.sleep(5)
        #status = """[{"empID": 1231, "firstname": "igor", "lastname": "mamorski", "status": 1, "address": "Sarig St 5 Karmiel"}, {"empID": 1233, "firstname": "elad", "lastname": "hezi", "status": 1, "address": "Ha-Dekel St 56 Karmiel"}, {"empID": 1234, "firstname": "vered", "lastname": "hezi", "status": 1, "address": "Ramim St 37 Karmiel"}, {"empID": 1235, "firstname": "orlando", "lastname": "bloom", "status": 1, "address": "Arava St 10 Karmiel"}, {"empID": 1236, "firstname": "johni", "lastname": "depp", "status": 1, "address": "HaShoshanim Street 4 Karmiel"}, {"empID": 1237, "firstname": "bibi", "lastname": "netaniyahu", "status": 1, "address": "Sderot Jabotinsky 10 Kiryat Yam"}, {"empID": 2030405, "firstname": "oren", "lastname": "hazan", "status": 1, "address": "kiryat ata, hankin st 10"}, {"empID": 4583456, "firstname": "zehava", "lastname": "galon", "status": 1, "address": "David Noy st 39, acre"}, {"empID": 5678435, "firstname": "zipi", "lastname": "livni", "status": 1, "address": "Hativat Harel st 151, Karmiel"}, {"empID8"""
        #my_len = len(status) + len(str(len(status))) + 1
         

        #print("len msg is ",len(status))
        print(mymsg.encode('ASCII'))
        # just send back the same data, but upper-cased
        self.request.send(mymsg.encode('ASCII'))

if __name__ == "__main__":
    (HOST, PORT) = get_ip(), 1234

    print('starting up on {} port {}'.format(*(HOST, PORT)))
    # Create the server, binding to localhost on port 1234
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    settings.myDBhandler = DBhandler.MyConnectionDBClass()
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()