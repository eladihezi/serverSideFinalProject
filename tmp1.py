import MySQLdb
import numpy
import googlemaps
import numpy

gmaps = googlemaps.Client(key='AIzaSyBN-UulFeXqjqECo628iWwY9pEZyGRUltA')

db = MySQLdb.connect("127.0.0.1","root","root")
cursor = db.cursor()

query = ("SELECT * FROM `projectdb`.`employees` ;")
cursor.execute(query)
print ("result is ",cursor)
employees = []
for (empID,firstname,lastname,address,status) in cursor:
    print("empID is {}, firstname is {}, lastname is  {},'address' is {} , status is {} ".format(*(empID,firstname,lastname,address,status)))
    user = {
        'empID' : empID,
        'firstname' : firstname,
        'lastname' :lastname,
        'address' : address,
        'status' : status
    }
    employees.append(user)


_A = [[0 for x in range(7)] for y in range(7)]
emp1 =   {
  'empID' : 1238,
  'firstname' : 'test1',
  'lastname' : 'test1',
  'address' : 'Sarig St 30 Karmiel',
  }
i=0
j=0
for emp in employees:
    if(emp1['empID'] == emp['empID']):
        continue
    distance_result = gmaps.distance_matrix(emp1['address'],emp['address'])
    query = ("""INSERT INTO `projectdb`.`distances` (sourceID, destinationID, distance)
      VALUES ({}, \'{}\',  \'{}\');""".format(*(emp1['empID'],emp['empID'],distance_result['rows'][0]['elements'][0]['distance']['value'] )))
    cursor.execute(query)
    distance_result = gmaps.distance_matrix(emp['address'],emp1['address'])
    query = ("""INSERT INTO `projectdb`.`distances` (sourceID, destinationID, distance)
      VALUES ({}, \'{}\',  \'{}\');""".format(*(emp['empID'],emp1['empID'],distance_result['rows'][0]['elements'][0]['distance']['value'] )))
    cursor.execute(query)
    print (distance_result)
    print (distance_result['rows'])
    
    print (distance_result['rows'][0]['elements'][0]['distance']['value'] )
    _A[i][j] = distance_result['rows'][0]['elements'][0]['distance']['value']
    i += 1
    #print (element['distance']['value'])
db.commit()
#data = json.loads(distance_result)



print  (numpy.matrix(_A))

