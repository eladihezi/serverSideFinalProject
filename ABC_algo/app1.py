from .BeeClass import *
from .FoodSource import *
from random import *
from .fitnessFunc import fitnessFunctionClass
import timeit
from .config import *
import sys
import time
import math


global LOOPCOUNTER




def daemon(dict_of_param):

     
    saveout = sys.stdout
    #sys.stdout = open("file.xt", "w+")

    delta = 0.001
    alpha = 0.1
    capacity = 10

    collectionPoint = dict_of_param['collectionPoint']
    cars = dict_of_param['numofvehicles']
    route_quality = dict_of_param['routequality']
    capacity = dict_of_param['vehiclecapacity']
    
    LIMIT = 50 * collectionPoint
    numOfIterations = {
        'low' : math.pow(collectionPoint,2)*cars,
        'medium' : math.pow(collectionPoint,3)*cars,
        'high' : math.pow(collectionPoint,4)*cars,
    }

    ffclass = fitnessFunctionClass(capacity)
    #time.sleep(10)


    start_time = timeit.default_timer()
    print("start time is ", start_time)
    print ("collection Points is {}, num of cars is {}, route quality is {} and itration is {}, capacity is {}".format(
        *(collectionPoint,cars,route_quality,numOfIterations[route_quality],capacity)))

    def initiateFoodScource(points  , cars):
        solutionRepresentation = []    
        myList = [i+1 for i in range(points)]
        #print("number of real cars is ",cars)
        for x in range(0, cars-1):
            myList.append(0) 
        for x in range(1, cars + points):
            rand1 = randint(0,len(myList)-1)
            solutionRepresentation.append(myList[rand1])
            del myList[rand1]
        (value,my_violation) = ffclass.fitnessFunction(solutionRepresentation,alpha) 
        return FoodSource(solutionRepresentation,value,my_violation)

    def initiatePopulation(collectionPoint,cars,populationSize):
        allPopulation = []
        for x in range(0, populationSize):
            foodSource = initiateFoodScource(collectionPoint,cars)
            allPopulation.append(foodSource)
        return allPopulation

    def set_alpha(alpha):
        if(FoodSource.num_of_violation > populationSize/2 ):
            alpha = alpha * (1 + delta)
        else:
            alpha = alpha / (1 + delta)
        return alpha


    #get default config setup from modul
    FFPopulationFoodSource = []
    workBees = []



    ##init martix/food sources/bees
    allPopulation = initiatePopulation(collectionPoint,cars,populationSize)
    bee = BeeClass("Employed" ,ffclass,0,0,0)
    # for f in allPopulation:
    #     workBees.append(BeeClass("Employed" ,limit,f.ID,f.value))

    print("we initiate bees Population")
    print("we initiate foodSource Population")
    print("we initiate foodSource Population FF values")





    ## BIG LOOP
    LOOPCOUNTER = numOfIterations[route_quality]
    #LOOPCOUNTER = 1000
    while(LOOPCOUNTER > 0 ):
        LOOPCOUNTER -= 1
        alpha = set_alpha(alpha)
        ##BEE WORKER
        # for each food source
        #we do 1 bee for all but next will do it better maybe for GPU   
        for f in allPopulation:
            (betterFoodSource,newValue,my_violation) =  bee.work(f.solution,alpha)
            if (newValue < f.value): #if we found better solution
                f.setBetterFood( betterFoodSource, newValue, my_violation)
            else :
                f.limit += 1
            
        #allPopulation.sort()  
        FFPopulationFoodSource = [f.value for f in allPopulation]
        
        alpha = set_alpha(alpha)
        ##ONLOOKER BEE
        probVector = fitnessFunctionClass.setProbability(FFPopulationFoodSource)
        
        group = [[] for i in range(0,populationSize)]
        valueGroup = [[] for i in range(0,populationSize)]
        violationGroup = [[] for i in range(0,populationSize)]

        for loopCounter in range(0, populationSize):
            #this index is chosen by probability of the FF
            index = fitnessFunctionClass.rouletteWeelGetIndex(probVector,probVector[-1])
            localFoodScource = allPopulation[index]
            (altenativeSolution,newValue,my_violation)= bee.work(localFoodScource.solution,alpha)           
            group[index].append(altenativeSolution)
            valueGroup[index].append(newValue)
            violationGroup[index].append(my_violation)

        for i, gi in enumerate(group):
            localValueGroup = valueGroup[i]
            orgValue = allPopulation[i].value
            localviolationGroup = violationGroup[i]

            if gi: #that list no empty
                minValue = min(localValueGroup)
                minIndex = localValueGroup.index(minValue)            
                bestOfGroup = gi[minIndex]
                my_violation = localviolationGroup[minIndex]

                if(minValue < orgValue):
                    index = len(allPopulation) - 1
                    chosen =  allPopulation[index]
                    while(index >= 0 ):
                        if(allPopulation[index].value > orgValue and chosen.limit < allPopulation[index].limit):
                            chosen = allPopulation[index]
                        index -= 1
                    chosen.setBetterFood(bestOfGroup,minValue,my_violation)
                else:
                    allPopulation[i].limit += 1
        
        alpha = set_alpha(alpha)          
        ##SCOUT BEE
        #check if any foodsource reach the limit (BETA: we not going to change our 10% of out best solutions  )
        for i, f in enumerate(allPopulation):
            #if(f.limit >= LIMIT and i > populationSize / 10): #dont touch the 10% of best 
            if(f.limit >= LIMIT ): 
                (new_solution, new_value,new_violation) = bee.work(f.solution,alpha)
                #print (new_solution, new_value,new_violation)
                f.setBetterFood(new_solution, new_value,new_violation)









    allPopulation.sort()
    FFPopulationFoodSource = [f.value for f in allPopulation]
    #print("we use neighborhoodOperators on each food source ",numOfIterations , "times !!!" )
    print()
    print("our foodSource Population FF values")
    print (FFPopulationFoodSource)


    print()
    allPopulation[0].print_me()
    print()
    allPopulation[1].print_me()
    print()
    allPopulation[2].print_me()
    print()
    #ffclass.fitnessFunction(allPopulation[0].solution,0.1)
    elapsed = timeit.default_timer() - start_time
    print ("total time elapsed is  ",elapsed," sec")
    sys.stdout=saveout 

    return allPopulation[0].solutionToJson()



if __name__ == "__main__":
    dict_of_param['collectionPoint'] = 26
    dict_of_param['numofvehicles'] = 7
    dict_of_param['routequality'] = 'low'
    dict_of_param['capacity'] = 5

    daemon(dict_of_param)