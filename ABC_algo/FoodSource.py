import json

from .fitnessFunc import *


class FoodSource:
    foodCounter = 0
    num_of_violation = 0

    def __init__(self, solution,value,new_or_not):# violation
        
        self.solution = solution
        self.value = value
        #self.violation = 
        if(new_or_not):
            self.ID =  new_or_not 
        else:           
            FoodSource.foodCounter += 1 
            self.ID = FoodSource.foodCounter
        self.limit = 0
        #new_or_not ? FoodSource.foodCounter += 1 : 0
    
    def __lt__(self, other):
        return self.value < other.value


    def setBetterFood(self, solution, value):
        self.solution = solution
        self.value = value
        self.limit = 0

    def print_me(self):
        carNumber = 1
        myVector = list(self.solution)
        myVector.append(0)
        solution = list(splitz(myVector,0))
        
        for road in solution:
            myVector = [] 
            for point in road:
                myVector.append( str(point))

            road = " -> ".join(myVector)
            print("car ",carNumber ,"pick ",road)
            carNumber += 1
        #print("number of empty car is " ,cars - carNumber + 1)
        print("ID = ",self.ID, "and the total cost is ", self.value)
        print(self.solution)
    
    def solutionToJson(self):
        jsondict = {}
        carNumber = 1
        myVector = list(self.solution)
        myVector.append(0)
        solution = list(splitz(myVector,0))
        d2 = json.load(open("dict_ID.txt"))
        print ("d2 = ",d2)
        for road in solution:
            mydict = {}
            i = 0
            for point in road:
                i += 1
                print(point,str(point))
                mydict[i] = d2[str(point)]
                
            jsondict[carNumber] = mydict
            carNumber += 1

        json.dump(jsondict,open('data.txt', 'w'))

def splitz(seq, smallest):    
    group = []    
    for num in seq:
        if num != smallest:
            group.append(num)
        elif group:
            yield group
            group = []



