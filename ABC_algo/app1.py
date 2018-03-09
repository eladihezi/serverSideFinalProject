from .BeeClass import *
from .FoodSource import *
from random import *
from .fitnessFunc import *
import timeit
from .config import *
import sys
import time








def daemon():

    time.sleep(7)
    saveout = sys.stdout
    sys.stdout = open("file.xt", "w+")

    start_time = timeit.default_timer()
    print("start time is ", start_time)
    
    def initiateFoodScource(points  , numOfCars,new_or_not):
        tmparr = [0]    
        myList = [i+1 for i in range(points)]
        for x in range(0, numOfCars-1):
            myList.append(0) 
        for x in range(0, numOfCars+points-1):
            rand1 = randint(0,len(myList)-1)
            tmparr.append(myList[rand1])
            del myList[rand1]
        return FoodSource(tmparr,fitnessFunction(tmparr),new_or_not)

    def initiatePopulation(collectionPoint,cars,populationSize):
        allPopulation = []
        for x in range(0, populationSize):
            foodSource = initiateFoodScource(collectionPoint,cars,0)
            allPopulation.append(foodSource)
        return allPopulation



    #get default config setup from modul
    FFPopulationFoodSource = []
    workBees = []



    ##init martix/food sources/bees
    #initTravelCostMatrix(collectionPoint+1)
    allPopulation = initiatePopulation(collectionPoint,cars,populationSize)
    bee = BeeClass("Employed" ,limit,0,0)
    for f in allPopulation:
        workBees.append(BeeClass("Employed" ,limit,f.ID,f.value))

    print("we initiate bees Population")
    print("we initiate foodSource Population")
    print("we initiate foodSource Population FF values")



    ## BIG LOOP
    LOOPCOUNTER = numOfIterations
    while(LOOPCOUNTER > 0 ):
        LOOPCOUNTER -= 1
        
        ##BEE WORKER
        # for each food source
        #we do 1 bee for all but next will do it better maybe for GPU   
        for f in allPopulation:
            betterFoodSource =  bee.work(f.solution)
            newValue = betterFoodSource.pop()
            if (newValue < f.value): #if we found better solution
                f.setBetterFood(betterFoodSource , newValue)
            else :
                f.limit += 1
            
        #allPopulation.sort()  
        FFPopulationFoodSource = [f.value for f in allPopulation]
        
        
        ##ONLOOKER BEE
        probVector = setProbability(FFPopulationFoodSource)
        group = [[] for i in range(0,populationSize)]
        valueGroup = [[] for i in range(0,populationSize)]
        for loopCounter in range(0, populationSize):
            #this index is chosen by probability of the FF
            index = rouletteWeelGetIndex(probVector,probVector[-1])
            localFoodScource = allPopulation[index]
            altenativeSolution = bee.work(localFoodScource.solution)
            newValue = altenativeSolution.pop()
            group[index].append(altenativeSolution)
            valueGroup[index].append(newValue)
        
        for i, gi in enumerate(group):
            localValueGroup = valueGroup[i]
            orgValue = allPopulation[i].value
            if gi: #that list no empty
                minValue = min(localValueGroup)
                minIndex = localValueGroup.index(minValue)            
                bestOfGroup = gi[minIndex]

                if(minValue < orgValue):
                    index = len(allPopulation) - 1
                    chosen =  allPopulation[index]
                    while(index >= 0 ):
                        if(allPopulation[index].value > orgValue and chosen.limit < allPopulation[index].limit):
                            chosen = allPopulation[index]
                        index -= 1
                    chosen.setBetterFood(bestOfGroup,minValue)
                else:
                    allPopulation[i].limit += 1
                    
        ##SCOUT BEE
        #check if any foodsource reach the limit (BETA: we not going to change our 10% of out best solutions  )
        for i, f in enumerate(allPopulation):
            if(f.limit >= LIMIT and i > populationSize / 10):
                localSolution = bee.work(f.solution)
                f.setBetterFood( localSolution,localSolution.pop() )









    allPopulation.sort()
    FFPopulationFoodSource = [f.value for f in allPopulation]
    #print("we use neighborhoodOperators on each food source ",numOfIterations , "times !!!" )
    print()
    print("our foodSource Population FF values")
    print (FFPopulationFoodSource)


    print()
    print()
    allPopulation[0].print_me()
    print()
    print()
    fitnessFunction(allPopulation[0].solution)
    elapsed = timeit.default_timer() - start_time
    print ("total time elapsed is  ",elapsed," sec")
    sys.stdout=saveout 

    return allPopulation[0].solutionToJson()



if __name__ == "__main__":
    daemon()