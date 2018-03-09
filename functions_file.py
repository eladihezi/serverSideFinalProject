

import time
from ABC_algo import app1
import threading
import json

import settings
#from socket_server import myDBhandler

d = threading.Thread(name='daemon', target=app1.daemon)
# class MyThread(Thread):
#     def __init__(self,val):
#         ''' Constructor. '''
 
#         Thread.__init__(self)
#         self.val = val

#     def run(self):
#         time.sleep(1)
#         return app1.daemon()


### functions  by id        
def func1(data):
    username = data['username']
    password = data['password']
    query = ("SELECT * FROM admin_users WHERE  username = \'{}\' AND password = \'{}\';".format(*(username,password)))
    print(query)
    result = settings.myDBhandler.SelectQuery(query)
    print (result)
    if(result == "error"):
        return False
    else:
        return True

def func2(data):
    print ("data = ", data)


def func3(data):
    print ("call func3 ...",data)
    query = ("SELECT * FROM employees ;")
    result = settings.myDBhandler.SelectQuery(query)
    users =[]
    for (userID,firstname,lastname,address) in result:
        print("userID is {}, username is {}, password is  {}".format(*(userID,firstname,lastname)))
        user = {
            'userID' : userID,
            'firstname' : firstname,
            'lastname' :lastname,
            'address' : address
        }
        users.append(user)

    print (json.dumps(users))

def func4(data):
    print ("call func4 ...")


#run algo
def func5(data):
    try:
        d.start()
        return "Success"
    except:
        return "Failed"

#get routes
def func6(data):
    print ("call func6 ...")

#check status
def func7(data):
    return str(d.isAlive())
    