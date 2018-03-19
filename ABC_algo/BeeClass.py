from random import *
from .fitnessFunc import *


#TODO : more neighborhood Operators functions

class BeeClass:
    """
    a bee with work method to find better solution to improve the given foodscource 
    the neighborhood Operators are implemente here  
    """
    # total instances of the class 
    beeCount = 0

    # bee constructor get init  parameters
    # some of them are reserved for future implementations
    # ffclass is reference to Fitness Function class
    def __init__(self, name,ffclass, limit ,index,value):
        self.name = name
        self.limit = limit
        self.index = index
        self.value = value
        self.ffclass = ffclass
        BeeClass.beeCount += 1
      
    # main method of the bee class 
    # choose which neighborhood Operator will try to improve the given solution 
    def work(self,arr,alpha):
        tmp = list(arr)
        choose_op = randint(0,2)

        if(choose_op == 0):
            self.random_swap(tmp)
        elif(choose_op == 1):
            tmp = self.swaps_of_subsequences(tmp)
        else:
            tmp = self.swaps_of_subsequences_revers(tmp)
        
        (newValue,violation) = self.ffclass.fitnessFunction(tmp,alpha)
        return (tmp,newValue,violation)

    """here will come the neighborhood Operators method"""

    # random_swap - choose 2 random elements in the vector and swap
    def random_swap(self,arr):
        rand1 = randint(0,len(arr)-1)
        rand2 = randint(0,len(arr)-1)
        while (arr[rand2] == arr[rand1]):
            rand2 = randint(0,len(arr)-1)
        tmp = arr[rand1]
        arr[rand1] = arr[rand2]
        arr[rand2] = tmp

    # swaps_of_subsequences - choose 2 subsequences and swap them
    def swaps_of_subsequences(self,arr):
            
        #generate rnandom index and lenths
        start_index1 = randint(0,(len(arr)-1)//2)
        len_of_sub1 = randint(1,len(arr) - 2 - start_index1)
        start_index2 = randint( start_index1 + len_of_sub1,len(arr)-1)
        len_of_sub2 = randint(1,len(arr) - start_index2)

        #for readablity
        sub1 = arr[start_index1:len_of_sub1+start_index1]
        sub2 = arr[start_index2:len_of_sub2 + start_index2]

        #swap them and make new arr
        mylist = (arr[0:start_index1] + sub2 + arr[start_index1 + len_of_sub1 :start_index2] + sub1 + arr[start_index2 + len_of_sub2 :] )
        return mylist



    # swaps_of_subsequences_revers - choose 2 subsequences, revers them and swap
    def swaps_of_subsequences_revers(self,arr):
            
        #generate rnandom index and lenths
        start_index1 = randint(0,(len(arr)-1)//2)
        len_of_sub1 = randint(1,len(arr) - 2 - start_index1)
        start_index2 = randint( start_index1 + len_of_sub1,len(arr)-1)
        len_of_sub2 = randint(1,len(arr) - start_index2)

        #revrse the 2 subsq
        sub1 = arr[start_index1:len_of_sub1+start_index1]
        sub1.reverse()
        sub2 = arr[start_index2:len_of_sub2 + start_index2]
        sub2.reverse()

        #swap them and make new arr
        mylist = (arr[0:start_index1] + sub2 + arr[start_index1 + len_of_sub1 :start_index2] + sub1 + arr[start_index2 + len_of_sub2 :] )
        return mylist 

        
    #function for debug should not be used
    def displayEmployee(self):
        print ("Name : ", self.name,  ", limit: ", self.limit)






