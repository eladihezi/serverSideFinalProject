#    Copyright 2015 Pietro Bertera <pietro@bertera.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import queue
import socketserver
import socket
import sys
import logging
import threading
import tkinter as tk

import message_class
import settings

import DBhandler

from tkinter.scrolledtext import ScrolledText

frame_bgr_run = 'Green'
frame_bgr_stop = 'Red'
btn_clr = 'OliveDrab1'
btn_font = ('Century Gotic', 12)

class QueueLogger(logging.Handler):
    def __init__(self, queue):
        logging.Handler.__init__(self)
        self.queue = queue

    # write in the queue
    def emit(self, record):
        self.queue.put(self.format(record).rstrip('\n') + '\n')

# class LoggedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
#     def __init__(self, server_address, RequestHandlerClass, logger):
#         socketserver.UDPServer.__init__(self, server_address, RequestHandlerClass)
#         # Add the queue logger
#         self.logger = logger

# class UDPHandler(socketserver.BaseRequestHandler):   
#     def handle(self):
#         # Queue logger is un under the self.server object
#         self.server.logger.debug(self.request[0])

class LoggedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, logger):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        # Add the queue logger
        self.logger = logger

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

class MainApplication:
    def __init__(self, root, log_level, ip, port ):
        self.root = root
        self.log_level = log_level
        self.ip = ip
        self.port = port
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.geometry('1024x680')

        # 2 rows: firts with settings, second with registrar data
        self.main_frame = tk.Frame(self.root)
        # Commands row doesn't expands
        self.main_frame.rowconfigure(0, weight=0)
        # Logs row will grow
        self.main_frame.rowconfigure(1, weight=1)
        # Main fram can enlarge
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.main_frame.configure(bg=frame_bgr_stop)
        
        # Run/Stop button
        self.control_button = tk.Button(self.main_frame, text="Run Server", font=btn_font, bg=btn_clr, command=self.run_server)
        self.control_button.grid(row=0, column=0, sticky=tk.EW, ipady=20)
        
        # Clear button
        self.clear_button = tk.Button(self.main_frame, text="Clear Log", font=btn_font, bg=btn_clr, command=self.clear_log)
        self.clear_button.grid(row=1, column=0, sticky=tk.EW, ipady=20)
        
        # Stop log button
        self.control_log_button = tk.Button(self.main_frame, text="Pause Log", font=btn_font, bg=btn_clr, command=self.stop_log)
        self.control_log_button.grid(row=2, column=0, sticky=tk.EW, ipady=20)

        # Logs Widget
        self.log_widget = ScrolledText(self.main_frame)
        self.log_widget.grid(row=0, column=1, rowspan=3, sticky=tk.NSEW)
        
        # Not editable
        self.log_widget.config(state='disabled') 
        
        # Queue where the logging handler will write
        self.log_queue = queue.Queue()

        # Stup the logger
        l = logging.getLogger('logger')
        l.setLevel(self.log_level)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        # Use the QueueLogger as Handler
        hl = QueueLogger(queue=self.log_queue) 
        hl.setFormatter(formatter)
        l.addHandler(hl)
        self.logger = logging.getLogger('logger')

        # Setup the update_widget callback reading logs from the queue
        self.start_log()

    def stop_log(self):
        self.logger.debug("Pausing the logger")
        if self.logger_alarm is not None:
            self.log_widget.after_cancel(self.logger_alarm)
            self.control_log_button.configure(text="Start Log", command=self.start_log)
            self.logger_alarm = None

    def start_log(self):
        self.logger.debug("Starting the logger")
        self.update_widget(self.log_widget, self.log_queue)
        self.control_log_button.configure(text="Pause Log", command=self.stop_log)

    def update_widget(self, widget, queue):
        widget.config(state='normal')
        # Read from the Queue and add to the log widger
        while not queue.empty():
            line = queue.get()
            widget.insert(tk.END, line)
            widget.see(tk.END)  # Scroll to the bottom
            widget.update_idletasks()
        widget.config(state='disabled')
        self.logger_alarm = widget.after(10, self.update_widget, widget, queue)

    def clear_log(self):
        self.log_widget.config(state='normal')
        self.log_widget.delete(0.0, tk.END)
        self.log_widget.config(state='disabled')

    def run_server(self):
        self.logger.debug("Starting thread")
        try:
            self.server = LoggedTCPServer((self.ip, self.port), MyTCPHandler, self.logger)
            self.server_thread = threading.Thread(name='server', target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            self.control_button.configure(text="Stop Server", command=self.stop_server)
            self.main_frame.configure(bg=frame_bgr_run)
        except Exception:
            self.logger.error("Cannot start the server: %s" % e)
            raise Exception
        
    def stop_server(self):
        self.logger.debug("Stopping server")
        self.server.shutdown()
        self.server.socket.close()
        self.logger.debug("Server stopped")
        self.control_button.configure(text="Run Server", command=self.run_server)
        self.main_frame.configure(bg=frame_bgr_stop)

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

if __name__ == "__main__": 
    root = tk.Tk()
    (address, port) = get_ip(), 1234
    # if len(sys.argv) == 3:
    #     port = int(sys.argv[2])
    #     address = sys.argv[1] 
        
    app = MainApplication(root, logging.DEBUG, address, port)
    root.title('GO2WORK')
    root.mainloop()
    # else:
    #     print ("Error: you must specify address and port..")
    #     sys.exit(-1)