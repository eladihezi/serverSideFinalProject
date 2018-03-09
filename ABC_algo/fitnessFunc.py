from random import *
from itertools import *
import timeit
from .config import * 

def myFunc(str):
    print ("the string is " ,str)


#_A #= []#[[0,4,3,5,6],[0,0,12,3,4],[0,0,0,2,1],[0,0,0,0,7],[0,0,0,0,0]]
_size = collectionPoint + 1 # collectionPoint + 1 for factory
_A = [[0 for col in range(_size)] for row in range(_size)]

# _A = [  [    0,  1581,  1888,  2513,  1930,  2593, 30085],
#         [ 2163,     0,  1887,  2512,  1533,  2196, 31557],
#         [ 1896,  1447,     0,  1510,  1777,  1613, 31573],
#         [ 2474,  2025,  1482,     0,  2355,  2418, 32790],
#         [ 1980,  1515,  1705,  2330,     0,  1082, 31657],
#         [ 2582,  2117,  2018,  2802,  1545,     0, 33308],
#         [30289, 31556, 31862, 32907, 31905, 33174,     0]]



def initTravelCostMatrix(size):
    print ("matrix size*size is " , size)
    for row in range(0,size):
        for col in range(row+1,size):
            _A[row][col] = randint(3,30)
            #print ("my row is ",row,"my col is ",col)

    #for row in range(0,size):
    #    print (_A[row])




#TODO NEED TO shape it alot
def fitnessFunction(myVector):
    totalValue = 0
    start = 0 
    tmp_vector = list(myVector)
    tmp_vector.append(0)

    #distance cost
    for i in range(1,len(tmp_vector)):  
        # slice solution to cars and calculate 
        if(tmp_vector[i] == 0):
            if(i - start > 1  ):
                totalValue += calTravelCost(tmp_vector[start : i+1])
            start = i

    return (totalValue)


    #print (myVector)

# calTravelCost func get road (vecor of point) and calculate the total cost for this road
# each vector should start with 0 that represent thet start point (factory)
# exmple : 
#       input <[0, 4, 5, 1, 0]> 
#   then the road is <0 -> 4 -> 5 -> 1 -> 0 > and we calculate the sum of A[0][4] + A[4][5] + A[5][1] + A[1][0]
def calTravelCost(myVector): 
    totalValue = 0  
    for i in range(0,len(myVector)-1):
        row = myVector[i]
        col = myVector[i+1]
        totalValue += _A[row][col]
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

