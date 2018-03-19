import json

from .fitnessFunc import *


class FoodSource:
    """
    Food Scource class each instance is a potential solution 
    foodCounter holds the number of occurrences 
    num_of_violation holds the number of solutions that have violation
    """
    foodCounter = 0
    num_of_violation = 0

    # class constructor init self parameter for later used in algo
    def __init__(self, solution,value,violation):
        
        self.solution = solution
        self.value = value
        self.violation = violation
        self.limit = 0
        FoodSource.foodCounter += 1
        self.ID = FoodSource.foodCounter       
        if(violation):
            FoodSource.num_of_violation += 1
    
    # cmp function for sorting arr 
    # for array of this class just use function sort
    def __lt__(self, other):
        return self.value < other.value

    # setBetterFood - get new solution and replace it with the one that have 
    def setBetterFood(self, solution, value,violation):
        self.solution = solution
        self.value = value
        self.limit = 0
        if(self.violation and not violation):
            FoodSource.num_of_violation -= 1
        elif(violation):
            FoodSource.num_of_violation += 1
        self.violation = violation

    # print_me - debug function to follw up how the foodsource changing
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
        print("ID = ",self.ID, "and the total cost is ", self.value," violation = ",self.violation)
        print(self.solution)
    

    # solutionToJson - convert the solution in class to json so the client could get the routes
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
                #print(point,str(point))
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



