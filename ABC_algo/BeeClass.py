from random import *
from .fitnessFunc import *

class BeeClass:
    'Common base class for all bees'
    beeCount = 0
    #alpha = 0.1

    def __init__(self, name,ffclass, limit ,index,value):
        self.name = name
        self.limit = limit
        self.index = index
        self.value = value
        self.ffclass = ffclass
        BeeClass.beeCount += 1
      
    ##worker bee here
    def work(self,arr,alpha):
        tmp = list(arr)
        
        if( randint(0,1) ):
            self.swaps_of_subsequences(tmp)
        else:
            self.neighborhoodOperators(tmp)
        (newValue,violation) = self.ffclass.fitnessFunction(tmp,alpha)

        #print ("my org arr is ",arr,"and value is ",value," and my change is " , tmp,"and value is ",newValue)
        #tmp.append(newValue)
        return (tmp,newValue,violation)


    #TODO : more neighborhood Operators functions
    def neighborhoodOperators(self,arr):
        rand1 = randint(1,len(arr)-1)
        rand2 = randint(1,len(arr)-1)
        #print (rand1," = rand1",rand2," = rand2")
        tmp = arr[rand1]
        arr[rand1] = arr[rand2]
        arr[rand2] = tmp


    #TODO : what happend if start_index1 = start_index2
    def swaps_of_subsequences(self,arr):
        start_index1 = randint(0,len(arr)-1)
        start_index2 = randint(0,len(arr)-1)
        len_of_swap = randint(1,len(arr)-1)
        while (len_of_swap):
            len_of_swap -= 1
            tmp = arr[start_index1]
            arr[start_index1] = arr[start_index2]
            arr[start_index2] = tmp    
            start_index1 += 1
            start_index2 += 1
            if(start_index1 == len(arr)):
                start_index1 = start_index1 - len(arr)
            if(start_index2 == len(arr)):
                start_index2 = start_index2 - len(arr)


    def displayEmployee(self):
        print ("Name : ", self.name,  ", limit: ", self.limit)






