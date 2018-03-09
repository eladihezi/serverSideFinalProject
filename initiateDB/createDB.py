

import MySQLdb

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

sql ="""CREATE TABLE `projectdb`.`employees` (
  `empID` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `adress` VARCHAR(45) NOT NULL,
  `status` BOOLEAN DEFAULT false,
  PRIMARY KEY (`empID`)
)
ENGINE = InnoDB;"""

cursor.execute(sql)

#db.commit()
cursor.close()
db.close()
