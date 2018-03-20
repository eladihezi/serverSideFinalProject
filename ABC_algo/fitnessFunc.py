from random import *
from itertools import *
import timeit
from .config import * 



import numpy



class fitnessFunctionClass:
    'global fitness function class with methods'
   
    # class constructor get the distance matrix from the file after the server write the values to the file
    # and set capacity as given
    def __init__(self,capacity):
        self.mat = numpy.loadtxt(open("distanceMatrix.csv", "rb"),  dtype='int',delimiter=",")
        self.capacity = capacity



    # fitnessFunction - the main method of the class return the value of a given solution
    # split the vector by value 0  and calculate the value of the road
    def fitnessFunction(self, route, alpha):
        totalValue = 0
        number_of_cars = 0
        tmp_vector = list(route)
        tmp_vector.append(0)
        violation = False
        # print("arrlocal",tmp_vector)
        last_index = 0
        for i, val in enumerate(tmp_vector):
            if val == 0:
                new_a = tmp_vector[last_index:i]
                vector_len = len(new_a)
                if(vector_len > 0):
                    new_a = [0] + new_a + [0]
                    totalValue += 3000 # 5km penelty for each car
                    totalValue += self.calTravelCost(new_a)
                    
                    #violation cost
                    if(vector_len > self.capacity):
                        violation = True                        
                        qx = (vector_len - self.capacity) * 10000 # 5km 
                        totalValue += alpha * qx
                        #print ("we have cars that over the capacity, capacity is : {} and number of pickup points is {}, qx is {},alpha is {}"
                        #    .format(*(self.capacity,vector_len,qx,alpha)) )
                       
                last_index = i+1
        return (totalValue,violation)

    # calTravelCost func get road (vecor of point) and calculate the total cost for this road
    # each vector should start with 0 that represent thet start point (factory)
    # exmple : 
    #       input <[0, 4, 5, 1, 0]> 
    #  then the road is <0 -> 4 -> 5 -> 1 -> 0 > and we calculate the sum of A[0][4] + A[4][5] + A[5][1] + A[1][0]
    def calTravelCost(self,myVector):
        totalValue = 0
        for i in range(1,len(myVector)-1):
            row = myVector[i]
            col = myVector[i+1]
            totalValue += self.mat[col][row]
        return (totalValue)


    # setProbability - this methos for the onlooker bees 
    # we set for each Food source his probability to selected from population
    def setProbability(foodSourceFF):
        totals = []
        running_total = 0
        for elem in foodSourceFF:
            try:
                running_total += int(elem)
            except:
                print("ERROR : the give vector is ",foodSourceFF)
            totals.append(running_total)
        return(totals)

    # rouletteWeelGetIndex - return index according to his Probability
    def rouletteWeelGetIndex(totals,running_total):    
        rnd = random() * running_total
        for i, total in enumerate(totals):
            if rnd < total:
                return i

