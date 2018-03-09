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
        if(type(status) == type(True)):
            self.request.send(bytes(status))
            return status
        #time.sleep(5)
        # just send back the same data, but upper-cased
        self.request.send(status.encode('ASCII'))

if __name__ == "__main__":
    (HOST, PORT) = get_ip(), 1234

    print('starting up on {} port {}'.format(*(HOST, PORT)))
    # Create the server, binding to localhost on port 1234
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    settings.myDBhandler = DBhandler.MyConnectionDBClass()
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()