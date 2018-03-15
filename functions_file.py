

import time
from ABC_algo import app1
import threading
import json
import numpy


#from ABC_algo import LOOPCOUNTER
import math
import googlemaps 

import settings
#from socket_server import myDBhandler

class MyThread():
    def __init__(self):
        ''' Constructor. '''
        self.d = ''

    def run(self,data):
        
        self.d = threading.Thread(name='daemon', target=app1.daemon,args=(data,))
        self.d.start()

    def isAlive(self):
        try:
            status = self.d.isAlive()
        except:
            status = False

        return status
        
    
d = MyThread()



### functions  by id        
def func1(data):
    username = data['username']
    password = data['password']
    query = ("SELECT * FROM AdminUsers WHERE  username = \'{}\' AND password = \'{}\';".format(*(username,password)))
    result = settings.myDBhandler.SelectQuery(query)
    if(result):
        return True
    return False

#add emp 
#TODO set -1 values in distance matrix in DB
def func2(data):
    empID = data['empID']
    firstname = data['firstname']
    lastname = data['lastname']
    address = data['address']
    status = data['status']
    query = ("""INSERT INTO employees (empID, firstname, lastname,address,status)
        VALUES ({}, \'{}\', \'{}\', \'{}\',{});""".format(*(empID,firstname, lastname,address,status)))
    result = settings.myDBhandler.InsertQuery(query)
    return result

#get emp list
#TODO check if its not empty
def func3(data):
    query = ("SELECT * FROM employees WHERE not (empID = 0 );")
    result = settings.myDBhandler.SelectQuery(query)
    users = []
    for (empID,firstname,lastname,address,status) in result:
        #print("empID is {}, firstname is {}, lastname is  {}, address is {}, status is {} ".format(*(empID,firstname,lastname,address,status)))
        user = {
            'empID' : empID,
            'firstname' : firstname,
            'lastname' :lastname,
            'status' : status,
            'address' : address
        }
        users.append(user)
    return (json.dumps(users))


#remove emp
def func4(data):
    empID =  data[0]['empID']
    result = ''
    for emp in data:
        empID =  emp['empID']
        query = ("DELETE FROM employees WHERE empID = {} ;".format(*(empID,)))
        result += settings.myDBhandler.InsertQuery(query)
    result = settings.myDBhandler.InsertQuery(query)
    return result
    


#run algo
#TODO check that DB is updated
def func5(data):
    if (func7("")):
        return False
    #check if DATABASE is updated for employees that should work
    query = ("""SELECT  t1.empID,t1.address,t2.empID,t2.address   FROM employees as t1 ,employees as t2
                WHERE t1.status = 1 AND t2.status = 1 AND NOT (t1.empID = t2.empID) AND
                (t1.empID,t2.empID) NOT IN(SELECT  sourceID,destinationID FROM distances  )""")
    result = settings.myDBhandler.SelectQuery(query)
    print ("result =",result)
    if( result):
        gmaps = googlemaps.Client(key='AIzaSyBN-UulFeXqjqECo628iWwY9pEZyGRUltA')
        
        for (empID1,address1,empID2,address2) in result:
        #update when needed
            distance_result = gmaps.distance_matrix(address1, address2)
            print ("sourceID, destinationID",address1,address2)
            print ("google results",distance_result )
            query = ("""INSERT INTO distances (sourceID, destinationID, distance)
            VALUES ({}, \'{}\',  \'{}\');""".format(*(empID1, empID2,distance_result['rows'][0]['elements'][0]['distance']['value'] )))
            status = settings.myDBhandler.InsertQuery(query)
            

    #get the needed matrix and write it for the algo
    query = ("""SELECT  sourceID,destinationID,distance,t1.firstname,t1.lastname,t1.address
        FROM projectdb.employees as t1 ,projectdb.employees as t2,projectdb.distances
        where t1.status = 1 AND t2.status = 1 AND sourceID = t1.empID AND destinationID = t2.empID ;""")
 
    result = settings.myDBhandler.SelectQuery(query)
    print ("result is",result,result.rowcount)
    n = math.sqrt(result.rowcount)
    n = math.ceil(n)
    distanceMatrix = [[0 for col in range(n)] for row in range(n)]
    i = 0
    dict_ID = {}
    source_dict = {}
    for sourceID,destinationID,distance,firstname,lastname,address in result:
        if(sourceID not in source_dict):
            source_dict[sourceID] = i
            
            dict_ID[i] = {
                 'empID' : sourceID,
                 'address' : address,
                 'firstname' : firstname,
                 'lastname' : lastname
                } 
            i += 1
            
    print("new dict is ",source_dict) 
    
    
    for sourceID,destinationID,distance,firstname,lastname,address in result:
        print ( "sourceID,destinationID,distance,firstname,lastname,address",sourceID,destinationID,distance,firstname,lastname,address)
        # if(math.floor(i/n) == i%n):
        #     distanceMatrix[math.floor(i/n)][i%n] = 0
        #     i += 1

                       
        distanceMatrix[source_dict[destinationID]][source_dict[sourceID]] = distance
        #i += 1
    print ("dict is ",dict_ID)

    json.dump(dict_ID, open("dict_ID.txt",'w'))
    arr = numpy.asarray(distanceMatrix)
    numpy.savetxt("ABC_algo/distanceMatrix.csv", arr, delimiter = ",",fmt = '%d')
    data['collectionPoint'] = n-1
    print ("data is ",data)
    #try the algo 
    try:
        d.run(data)
        return "Success"
    except:
        return False

#get routes
def func6(data):
    print ("call func6 ...",data)
    local = json.load(open("data.txt"))
    return json.dumps(local)

#check algo status
def func7(data):
    return d.isAlive()

#update emp status
def func8(data):
    print ("call func8 ...",data)
    query = """UPDATE employees 
        SET status = {}
        WHERE empID = {}""".format(*(data[0]['status'],data[0]['empID']))
    local_string =''
    for emp in data:
        local_string += " OR empID = {}".format(*(emp['empID'],))
    query += local_string
    print ("query is ",query)
    result = settings.myDBhandler.InsertQuery(query)
    print ("result is ",result)
    
    return result

#search emp by empID/name/address
def func9(data):
    print ("call func9 ...",data)
    searchby = data['searchby']
    if(data['searchby'] == 'firstname'):
        query = ("SELECT * FROM employees WHERE firstname LIKE \'{}%\' OR lastname LIKE \'{}%\';".format(*(data[searchby],data[searchby])))
    elif(data['searchby'] == 'address'):
        query = ("SELECT * FROM employees WHERE {} LIKE \'%{}%\';".format(*(searchby,data[searchby])))
    else:
        query = ("SELECT * FROM employees WHERE {} LIKE \'{}%\';".format(*(searchby,data[searchby])))
    result = settings.myDBhandler.SelectQuery(query)
    users = []
    print (query)
    for (empID,firstname,lastname,address,status) in result:
        print("empID is {}, firstname is {}, lastname is  {}, address is ,{} status is {} ".format(*(empID,firstname,lastname,address,status)))
        user = {
            'empID' : empID,
            'firstname' : firstname,
            'lastname' :lastname,
            'address' : address,
            'status' : status
        }
        users.append(user)

    print (json.dumps(users))#it str now
    return (json.dumps(users))

#update emp data
def func10(data):
    print ("call func10 ...",data)
    user = {}
    setStr = "set "
    condStr = "WHERE empID = " + str(data['empID'])
    address_flag = False
    i = 0 
    for key in data.keys():
        if(key == 'empID'):
            continue
        if(i > 0):
            setStr += "," 
        setStr += " {} = \'{}\' ".format(*(key, data[key]))
        i += 1
        if(key == 'address'):
            address_flag = True
    
    query = ("UPDATE employees " + setStr  + condStr)
    print ("query is", query)
    #query = ("UPDATE employees FROM employees WHERE {} = {};".format(*(searchby,data[searchby])))
    result = settings.myDBhandler.InsertQuery(query)
    result1 = True
    if(address_flag):
        query = ("DELETE FROM distances WHERE sourceID = {} OR destinationID = {}".format(*(data['empID'],data['empID'])))
        result1 = settings.myDBhandler.InsertQuery(query)   
    return (result and result1)
