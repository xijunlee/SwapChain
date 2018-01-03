from __future__ import print_function

import sys
import math
from pyspark import SparkContext
from random import randint
from random import random
import copy

def ChromosomesInitiallize(chromosomesSize,geneLength,data,D):
    chromosomes = []
    for i in range(chromosomesSize):
        chromosome = Chromosome()
        for j in range(geneLength):
            chromosome.geneSerial.append(randint(0,data.PROVIDERS[j].cnt-1))
        #for test,will be deleted in real environment
        chromosome.fitness = CalcFitness(i,chromosome.geneSerial,data,D)
        chromosomes.append(chromosome)
    return chromosomes

def returnFitness(x):
    return x.fitness

def CalcFitness(chromosomeNo, geneSerial, data, D):
    """
        usage ChromosomeNumber,geneSerial,data,D
        return fitness for this1  Chromosome
    """
    alpha = 10000000.00
    beta = 0.01
    # alpha and beta are weight factor
    data = data.value
    D = D.value
    customers = []
    fitness = 0
    for item in data.CUSTOMERS:
        tmp = Customer()
        tmp.x = copy.deepcopy(item.x)
        tmp.y = copy.deepcopy(item.y)
        tmp.demand = copy.deepcopy(item.demand)
        customers.append(tmp)
    providers = []
    sigmaCost = 0
    sigmaCapacity = 0
    sigmaDemand = 0
    mmd = -1000.00
    for i in range(0,len(geneSerial)):
        tmpProvider = Provider()
        tmpProvider.x = copy.deepcopy(data.PROVIDERS[i].x)
        tmpProvider.y = copy.deepcopy(data.PROVIDERS[i].y)
        tmpProvider.capacity = copy.deepcopy(data.PROVIDERS[i].capacity[geneSerial[i]])
        tmpProvider.cost = copy.deepcopy(data.PROVIDERS[i].cost[geneSerial[i]])
        sigmaCost = sigmaCost + tmpProvider.cost
        sigmaCapacity = sigmaCapacity + tmpProvider.capacity
        providers.append(tmpProvider)
    for item in customers:
        sigmaDemand = sigmaDemand + item.demand

    if sigmaCapacity >= sigmaDemand:
        swapchainsolver = SwapChainSolver(providers, customers)
        mmd = swapchainsolver.Solver()
        if mmd > D:
            fitness = -1000.00
        else:
            if sigmaCost != 0:
                fitness = float(1000.0/sigmaCost)
            else:
                fitness = 1e8
    #print("fitness,mmd,sigmaCapacity,sigmaCost,sigmaDemand:",fitness,mmd,sigmaCapacity,sigmaCost,sigmaDemand)
    return fitness

    #swapchainsolver.initiallize_assignment()
    # print for debug
    """for i in range(len(customers)):
        print(customers[i].x,customers[i].y,customers[i].demand)
        for i in range(len(providers)):
            print(providers[i].x,providers[i].y,providers[i].capacity,providers[i].cost)"""

'''
def CalcFitnessForSpark(chromosomeNo, geneSerial, data, D):
    """
        usage ChromosomeNumber,geneSerial,data,D
        return fitness for this1  Chromosome
    """
    alpha = 10000000.00
    beta = 0.01
    # alpha and beta are weight factor
    customers = []
    fitness = 0
    for item in data.value.CUSTOMERS:
        tmp = Customer()
        tmp.x = copy.deepcopy(item.x)
        tmp.y = copy.deepcopy(item.y)
        tmp.demand = copy.deepcopy(item.demand)
        customers.append(tmp)
    providers = []
    sigmaCost = 0
    sigmaCapacity = 0
    sigmaDemand = 0
    mmd = -1000.00
    for i in range(0,len(geneSerial)):
        tmpProvider = Provider()
        tmpProvider.x = copy.deepcopy(data.value.PROVIDERS[i].x)
        tmpProvider.y = copy.deepcopy(data.value.PROVIDERS[i].y)
        tmpProvider.capacity = copy.deepcopy(data.value.PROVIDERS[i].capacity[geneSerial[i]])
        tmpProvider.cost = copy.deepcopy(data.value.PROVIDERS[i].cost[geneSerial[i]])
        sigmaCost = sigmaCost + tmpProvider.cost
        sigmaCapacity = sigmaCapacity + tmpProvider.capacity
        providers.append(tmpProvider)
    for item in customers:
        sigmaDemand = sigmaDemand + item.demand

    if sigmaCapacity >= sigmaDemand:
        swapchainsolver = SwapChainSolver(providers, customers)
        mmd = swapchainsolver.Solver()
        if mmd > D:
            fitness = -1000.00
        else:
            if sigmaCost != 0:
                fitness = float(1000.0/sigmaCost)
            else:
                fitness = 1e8
    #print("fitness,mmd,sigmaCapacity,sigmaCost,sigmaDemand:",fitness,mmd,sigmaCapacity,sigmaCost,sigmaDemand)
    return fitness

    #swapchainsolver.initiallize_assignment()
    # print for debug
    """for i in range(len(customers)):
        print(customers[i].x,customers[i].y,customers[i].demand)
        for i in range(len(providers)):
            print(providers[i].x,providers[i].y,providers[i].capacity,providers[i].cost)"""
'''

def LoadDataFromHere():
    p=[]
    for i in range(6):
        p.append([])
    p[0]=[2,7,5,0,3,4,5,6,0,0,10,20,30]
    p[1]=[4,7,5,0,3,7,8,9,0,0,10,20,30]
    p[2]=[5,7,5,0,6,7,8,9,0,0,10,20,30]
    p[3]=[10,7,5,0,3,4,5,6,0,0,10,20,30]
    p[4]=[2.7,6.8,5,0,3,4,5,6,0,110,120,130,140]
    p[5]=[4,5,5,0,1,3,5,6,0,210,211,222,223]

    c=[]
    for i in range(10):
        c.append([])
    c[0]=[4,5,1]
    c[1]=[0,1,1]
    c[2]=[3,0,2]
    c[3]=[5,2,2]
    c[4]=[1,3,1]
    c[5]=[3,4,1]
    c[6]=[1,5,1]
    c[7]=[2,1,1]
    c[8]=[1,1,1]
    c[9]=[7,9,2]

    PROVIDERS = []
    for item in p:
        tmpProvider = ProviderPlus()
        tmpProvider.x = float(item[0])
        tmpProvider.y = float(item[1])
        tmpProvider.cnt = int(item[2])
        for j in range(0, tmpProvider.cnt):
            tmpProvider.capacity.append(float(item[j+3]))
            tmpProvider.cost.append(float(item[j + 3 + tmpProvider.cnt]))
        PROVIDERS.append(tmpProvider)

    CUSTOMERS = []
    for item in c:
        tmpCustomer = Customer()
        tmpCustomer.x = float(item[0])
        tmpCustomer.y = float(item[1])
        tmpCustomer.demand = float(item[2])
        CUSTOMERS.append(tmpCustomer)

    return PROVIDERS, CUSTOMERS

if __name__ == "__main__":

    sc = SparkContext(appName="PythonSwapChain")

    # po is data contains informantion about PROVIDERS and CUSTOMERS
    po = PO()
    # read providers and customers data from text
    po.PROVIDERS, po.CUSTOMERS = LoadDataFromHere()
    poBroadcast = sc.broadcast(po)

    Iteration = 50 #need input
    GeneLength = len(po.PROVIDERS)
    ChromosomesSize = 100#need input
    Chromosomes = []
    ProbabilityMutation = 0.00001
    ProbabilityCross = 0.01
    ProbabilityS = 0 # unknow
    D = 50.00

    theBestIndividual = []
    theBestFitness = -float('inf')
    #Chromosomes initiallizing
    Chromosomes = ChromosomesInitiallize(ChromosomesSize,GeneLength,po,D)
    '''Chromosomes = sorted(Chromosomes,key = returnFitness)
    theBestFitness = Chromosomes[len(Chromosomes)-1].fitness
    theBestIndividual.append(Chromosomes[len(Chromosomes)-1])'''
    for i in range(Iteration):
	    #chromosomes replicate
        nextGenerationChromosomes = []
        pi = []
        fitnessSum = 0
        Chromosomes = sorted(Chromosomes,key = returnFitness)
        #select the best individual in chromosomes into next generation chromosomes,directly
        tmp = Chromosome()
        tmp.fitness = copy.deepcopy(Chromosomes[len(Chromosomes)-1].fitness)
        tmp.geneSerial = copy.deepcopy(Chromosomes[len(Chromosomes)-1].geneSerial)
        nextGenerationChromosomes.append(tmp)

        for item in Chromosomes:
            fitnessSum = fitnessSum + item.fitness
        pi.append(Chromosomes[0].fitness/fitnessSum)
        for ri in range(1,len(Chromosomes)):
            pi.append(Chromosomes[ri].fitness/fitnessSum + pi[ri-1])
        copyNum = len(Chromosomes) - 1
        for ri in range(1,len(Chromosomes)):
            randnum = random()
            for j in range(len(pi)):
                if randnum <= pi[j]:
                    copyNum = j
                    break
            tmp = Chromosome()
            tmp.fitness = copy.deepcopy(Chromosomes[copyNum].fitness)
            tmp.geneSerial = copy.deepcopy(Chromosomes[copyNum].geneSerial)
            nextGenerationChromosomes.append(tmp)

        Chromosomes = nextGenerationChromosomes

        #chromosomes cross
        hash = []
        for ci in range(len(Chromosomes)):
            hash.append(0)
        hash[0] = 1
        for  ci in range(1,len(Chromosomes)/2):
            hash[ci] = 1
            j = 0
            while hash[j] == 1:
                j = len(Chromosomes)/2 + randint(0,len(Chromosomes)/2-1)#??????
            hash[j] = 1
            #cross gene between pointA and pointB
            pointA = randint(0,len(Chromosomes[0].geneSerial)-1)
            pointB = randint(0,len(Chromosomes[0].geneSerial)-1)
            if pointA >= pointB:
                tmp = pointA
                pointA = pointB
                pointB = tmp
            if ci != 0 and j != 0:
                for k in range(pointA,pointB+1):
                    tmp = Chromosomes[ci].geneSerial[k]
                    Chromosomes[ci].geneSerial[k] = Chromosomes[j].geneSerial[k]
                    Chromosomes[j].geneSerial[k] = tmp

		#chromosomes mutation
        for k in range(0,int(len(Chromosomes)*len(Chromosomes[0].geneSerial)*ProbabilityMutation)+1):
            mi = randint(0,len(Chromosomes)-1)
            ik = randint(0,len(Chromosomes[0].geneSerial)-1)
            vk = randint(0,po.PROVIDERS[ik].cnt-1)
            Chromosomes[mi].geneSerial[ik] = vk

        partitions = 2
        '''
        for x in range(len(Chromosomes)):
            Chromosomes[x].fitness = CalcFitness(x,Chromosomes[x].geneSerial,po,D)
        '''
        FITNESS = sc.parallelize(range(len(Chromosomes)),partitions) \
                    .map(lambda x:CalcFitness(x,Chromosomes[x].geneSerial,poBroadcast.value,D)) \
                    .collect()
        for x in range(len(Chromosomes)):
            Chromosomes[x].fitness = copy.deepcopy(FITNESS[x])

        Chromosomes = sorted(Chromosomes,key = returnFitness)
        for x in range(len(Chromosomes)):
            sigmaCost = 0
            for ii in range(len(Chromosomes[x].geneSerial)):
                sigmaCost = sigmaCost + po.PROVIDERS[ii].cost[Chromosomes[x].geneSerial[ii]]
            print("the individual fitness,sigmaCost,geneSerial ",Chromosomes[x].fitness,sigmaCost,Chromosomes[x].geneSerial)
        tmp = max(Chromosomes,key=returnFitness)
        theBest = Chromosome()
        theBest.fitness = copy.deepcopy(tmp.fitness)
        theBest.geneSerial = copy.deepcopy(tmp.geneSerial)
        theBestIndividual.append(theBest)

    sc.stop()

    print("the best:")
    for item in theBestIndividual:
        sigmaCost = 0
        for i in range(len(item.geneSerial)):
            sigmaCost = sigmaCost + po.PROVIDERS[i].cost[item.geneSerial[i]]
        print("the best individual fitness,sigmaCost,geneSerial ",item.fitness,sigmaCost,item.geneSerial)

    theBestInBest = max(theBestIndividual,key=returnFitness)
    sigmaCost = 0
    for i in range(len(theBestInBest.geneSerial)):
        sigmaCost = sigmaCost + po.PROVIDERS[i].cost[theBestInBest.geneSerial[i]]
    print("the best in best individual fitness,sigmaCost,geneSerial ",theBestInBest.fitness,sigmaCost,theBestInBest.geneSerial)

