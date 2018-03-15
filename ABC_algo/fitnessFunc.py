from random import *
from itertools import *
import timeit
from .config import * 


import numpy



class fitnessFunctionClass:
    'global fitness function class with methods'
   
    #mat = [[]]
    def __init__(self):
        self.mat = numpy.loadtxt(open("ABC_algo/distanceMatrix.csv", "rb"),  dtype='int',delimiter=",")
        self.delta = 0.001
    

    #TODO NEED TO shape it alot
    def fitnessFunction(self,route):
        totalValue = 0
        start = 0 
        tmp_vector = list(route)
        tmp_vector.append(0)

        #distance cost
        for i in range(1,len(tmp_vector)):  
            # slice solution to cars and calculate 
            if(tmp_vector[i] == 0):
                if(i - start > 1  ):
                    totalValue += self.calTravelCost(tmp_vector[start : i+1])
                start = i

        #violation cost

        return (totalValue)


        #print (myVector)

    # calTravelCost func get road (vecor of point) and calculate the total cost for this road
    # each vector should start with 0 that represent thet start point (factory)
    # exmple : 
    #       input <[0, 4, 5, 1, 0]> 
    #   then the road is <0 -> 4 -> 5 -> 1 -> 0 > and we calculate the sum of A[0][4] + A[4][5] + A[5][1] + A[1][0]
    def calTravelCost(self,myVector): 
        totalValue = 0
        #for i in range(0,len(myVector)-1):
        for i in range(1,len(myVector)-1):
            #print ("my vector is ",myVector,"matrix is ",self.mat)
            row = myVector[i]
            col = myVector[i+1]
            totalValue += self.mat[col][row]
        return (totalValue)


    def setProbability(foodSourceFF):
        totals = []
        running_total = 0
        for elem in foodSourceFF:
            running_total += elem
            totals.append(running_total)

        #debug loop
        lastelem = 0
        nice_view_prob = []
        for i,elem in enumerate(totals):
            tmp = (elem-lastelem) /running_total
            lastelem = elem
            nice_view_prob.append(tmp * 100)
            #print ("my probability is ",tmp, "and index is ",i)
        
        #print ("my probability is vector is ", nice_view_prob)
        return(totals)

    def rouletteWeelGetIndex(totals,running_total):    
        rnd = random() * running_total
        for i, total in enumerate(totals):
            if rnd < total:
                return i

