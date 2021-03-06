

import MySQLdb
import numpy
import sys

db = MySQLdb.connect("127.0.0.1","root","root")
cursor = db.cursor()

sql = 'CREATE SCHEMA mydata' 
sql = 'CREATE SCHEMA   IF NOT EXISTS projectDB'
cursor.execute(sql)

sql = """CREATE TABLE `projectdb`.`AdminUsers` (
  `adminID` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`adminID`)
)
ENGINE = InnoDB;"""
cursor.execute(sql)


username = 'root' 
password = 'root'
query = ("""INSERT INTO `projectdb`.`AdminUsers` ( username, password)
	  VALUES (\'{}\',  \'{}\');""".format(*(username, password)))  

result = cursor.execute(query)
db.commit()

sql ="""CREATE TABLE `projectdb`.`employees` (
  `empID` INTEGER UNSIGNED NOT NULL,
  `firstname` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  `status` BOOLEAN DEFAULT false,
  PRIMARY KEY (`empID`)
)
ENGINE = InnoDB;"""

cursor.execute(sql)

sql = """CREATE TABLE `projectdb`.`distances` (
  `sourceID` INTEGER UNSIGNED NOT NULL,
  `destinationID` INTEGER UNSIGNED NOT NULL,
  `distance` INTEGER NOT NULL DEFAULT '-1',
  PRIMARY KEY (`sourceID`, `destinationID`),
  CONSTRAINT `FK_distances_1` FOREIGN KEY `FK_distances_1` (`sourceID`)
    REFERENCES `employees` (`empID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `FK_distances_2` FOREIGN KEY `FK_distances_2` (`destinationID`)
    REFERENCES `employees` (`empID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
    )
    ENGINE = InnoDB;
    """

cursor.execute(sql)


emp_array = [
  {
  'empID' : 1230,
  'firstname' : 'moshe',
  'lastname' : 'cohen',
  'address' : 'Snunit St 51 Karmiel',
  },
  {
  'empID' : 1231,
  'firstname' : 'igor',
  'lastname' : 'mamorski',
  'address' : 'Sarig St 5 Karmiel',
  },
  {
  'empID' : 1233,
  'firstname' : 'elad',
  'lastname' : 'hezi',
  'address' : 'Ha-Dekel St 56 Karmiel',
  },
  {
  'empID' : 1234,
  'firstname' : 'vered',
  'lastname' : 'hezi',
  'address' : 'Ramim St 37 Karmiel',
  },
  {
  'empID' : 1235,
  'firstname' : 'ronaldo',
  'lastname' : 'bloom',
  'address' : 'Arava St 10 Karmiel',
  },
  {
  'empID' : 1236,
  'firstname' : 'johni',
  'lastname' : 'depp',
  'address' : 'HaShoshanim Street 4 Karmiel',
  },
  {
  'empID' : 1237,
  'firstname' : 'bibi',
  'lastname' : 'nati',
  'address' : 'Sderot Jabotinsky 10 Kiryat Yam',
  },
  {
  'empID' : 1238,
  'firstname' : 'test1',
  'lastname' : 'test1',
  'address' : 'Sarig St 30 Karmiel',
  },



]




for emp in emp_array:
  empID = emp['empID']
  firstname = emp['firstname']
  lastname = emp['lastname']
  address = emp['address']
  query = ("""INSERT INTO `projectdb`.`employees` (empID, firstname, lastname,address)
      VALUES ({}, \'{}\',  \'{}\',\'{}\');""".format(*(empID,firstname, lastname,address)))  
  result = cursor.execute(query)
db.commit()


cursor.close()
db.close()
