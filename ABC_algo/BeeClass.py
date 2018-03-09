from random import *
from .fitnessFunc import *

class BeeClass:
   'Common base class for all bees'
   beeCount = 0

   def __init__(self, name, limit ,index,value):
      self.name = name
      self.limit = limit
      self.index = index
      self.value = value
      BeeClass.beeCount += 1


##worker bee here
   def work(self,arr):
       tmp = list(arr)
       self.neighborhoodOperators(tmp)
       newValue = fitnessFunction(tmp)
       #print ("my org arr is ",arr,"and value is ",value," and my change is " , tmp,"and value is ",newValue)
       tmp.append(newValue)
       return tmp


#TODO : more neighborhood Operators functions
   def neighborhoodOperators(self,arr):
      rand1 = randint(1,len(arr)-1)
      rand2 = randint(1,len(arr)-1)
      #print (rand1," = rand1",rand2," = rand2")
      tmp = arr[rand1]
      arr[rand1] = arr[rand2]
      arr[rand2] = tmp



   def displayEmployee(self):
      print ("Name : ", self.name,  ", limit: ", self.limit)






