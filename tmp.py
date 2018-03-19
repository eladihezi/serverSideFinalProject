

import sys

import json
import message_class
import time

import MySQLdb



import DBhandler


# db = MySQLdb.connect("127.0.0.1","root","root",'test1' )

# cursor = db.cursor()

# query = ("INSERT INTO employees( firstname, lastname) VALUES (\"IGOR1\",\"MAMORSKI1\");")


# cursor.execute(query)
# db.commit()
# cursor.close()
# db.close()


# songs_as_dict = []

#     for song in all_songs:
#         song_as_dict = {
#             'name' : song.name,
#             'artist' : song.artist,
#             'album' : song.album}
#         songs_as_dict.append(song_as_dict)

# db = MySQLdb.connect("127.0.0.1","root","root",'test1' )

# cursor = db.cursor()

# # query = ("SELECT userID,username,password FROM admin_users ;")
# # query = ("SELECT * FROM employees ;")
# query = ("SELECT * FROM employees ;")
# cursor.execute(query)
# users =[]
# for (userID,firstname,lastname,address) in cursor:
#     print("userID is {}, username is {}, password is  {}".format(*(userID,firstname,lastname)))
#     user = {
#         'userID' : userID,
#         'firstname' : firstname,
#         'lastname' :lastname,
#         'address' : address
#     }
#     users.append(user)

# print (json.dumps(users))
# cursor.close()
# db.close()




data = {
   'firstname' : 'root',
   'lastname' : 'root',
   'empID' : 1230
}
message_class.globalMessage.runbyidtry(1,data)

exit()

# dict_of_param['collectionPoint'] = 26
#     dict_of_param['numofvehicles'] = 7
#     dict_of_param['routequality'] = 'low'
#     dict_of_param['capacity'] = 5
json_str = json.dumps(data)
json_str = '{"numofvehicles":7,"routequality":"low","vehiclecapacity" : 5}'
localclass  = message_class.globalMessage('5',json_str)


print ("localclass = " ,localclass)
localclass.runbyid()

#message_class.globalMessage.runbyidtry('11','{}')

print ("check if algo running ")
status  = "Success"

while(status):
    #status = message_class.globalMessage.runbyidtry('2','{"empID": "1234", "firstname": "eroot","lastname" : "eroot","address":"carmiel", "status" : 0}')
    #status = message_class.globalMessage.runbyidtry('4','[{"empID": "326962784", "firstname": "igor","lastname" : "mamorski","address":"carmiel", "status" : 1}]')
    print ('status is ',status)
    time.sleep(1)
    status = message_class.globalMessage.runbyidtry('7','{"numofvehicles":6,"routequality":"low"}')

print ("hi i just wake up ")