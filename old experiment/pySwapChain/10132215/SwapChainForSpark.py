from __future__ import print_function

import sys
import math
from pyspark import SparkContext
from random import randint
from random import random
import copy

class Data:
    def __init__(pp,cc):
        self.p = []
        self.c = []

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

def CalcFitness(chromosomeNo, geneSerial, initialData, D):
    """
        usage ChromosomeNumber,geneSerial,data,D
        return fitness for this1  Chromosome
    """
    pp = initialData.p
    cc = initialData.c
    PROVIDERS1 = []
    for item in pp:
        tmpProvider = ProviderPlus()
        tmpProvider.x = float(item[0])
        tmpProvider.y = float(item[1])
        tmpProvider.cnt = int(item[2])
        for j in range(0, tmpProvider.cnt):
            tmpProvider.capacity.append(float(item[j+3]))
            tmpProvider.cost.append(float(item[j + 3 + tmpProvider.cnt]))
        PROVIDERS1.append(tmpProvider)

    CUSTOMERS1 = []
    for item in cc:
        tmpCustomer = Customer()
        tmpCustomer.x = float(item[0])
        tmpCustomer.y = float(item[1])
        tmpCustomer.demand = float(item[2])
        CUSTOMERS1.append(tmpCustomer)
    data = PO()
    data.PROVIDERS = PROVIDERS1
    data.CUSTOMERS = CUSTOMERS1
    
    alpha = 10000000.00
    beta = 0.01
    # alpha and beta are weight factor
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
                fitness = float(100000000.0/sigmaCost)
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


def LoadDataFromText(txtpath):
    """
        load data from text,return PROVIDERS,CUSTOMERS
    """
    fp = open(txtpath, "r")
    arr = []
    for line in fp.readlines():
        arr.append(line.replace("\n", "").split(" "))
    fp.close()
    NumberOfProviders = int(arr[0][0])
    PROVIDERS = []
    for i in range(1, NumberOfProviders + 1):
        tmp = arr[i]
        tmpProvider = ProviderPlus()
        tmpProvider.x = float(tmp[0])
        tmpProvider.y = float(tmp[1])
        tmpProvider.cnt = int(tmp[2])
        for j in range(0, tmpProvider.cnt):
            tmpProvider.capacity.append(float(tmp[j + 3]))
            tmpProvider.cost.append(float(tmp[j + 3 + tmpProvider.cnt]))
        PROVIDERS.append(tmpProvider)
    NumberOfCustomers = int(arr[NumberOfProviders + 1][0])
    CUSTOMERS = []
    for i in range(0, NumberOfCustomers):
        tmp = arr[i + NumberOfProviders + 2]
        tmpCustomer = Customer()
        tmpCustomer.x = float(tmp[0])
        tmpCustomer.y = float(tmp[1])
        tmpCustomer.demand = float(tmp[2])
        CUSTOMERS.append(tmpCustomer)
    return PROVIDERS, CUSTOMERS

def LoadDataFromHere():
    numberOfProviders = 6
    numberOfCustomers = 10
    p = []
    c = []
    for i in range(numberOfProviders):
        provider = []
        provider.append(random()*180.0)
        provider.append(random()*180.0)
        p.append(provider)

    for i in range(numberOfCustomers):
        customer = []
        customer.append(random()*180.0)
        customer.append(random()*180.0)
        c.append(customer)

    demandSum = 0
    capacitySum = 0
    for item in c:
        item.append(random()*10000)
        demandSum = demandSum + item[2]

    for item in p:
        item.append(6)
        for increase in range(0,110,20):
            item.append(demandSum*0.7/len(p)*(randint(90,110)/100.0)*((100.0+increase)/100.0))
        capacitySum = capacitySum + item[-1]
        for increase in range(0,110,20):
            item.append(15*(increase+100.0)/100.0)

    print(capacitySum,demandSum,capacitySum/demandSum)

    '''
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
    '''

    return p, c

if __name__ == "__main__":
    '''
    # po is data contains informantion about PROVIDERS and CUSTOMERS
    po = PO()
    # read providers and customers data from text
    po.PROVIDERS, po.CUSTOMERS = LoadDataFromHere()
    '''
    data = Data()
    #po = PO()
    data.p,data.c = LoadDataFromHere()
    sc = SparkContext(appName="SwapChain")
    
    Iteration = 10 #need input
    GeneLength = len(data.p)
    ChromosomesSize = 100#need input
    Chromosomes = []
    ProbabilityMutation = 0.00001
    ProbabilityCross = 0.01
    ProbabilityS = 0 # unknow
    D = 200.00

    theBestIndividual = []
    theBestFitness = -float('inf')
    #Chromosomes initiallizing
    Chromosomes = ChromosomesInitiallize(ChromosomesSize,GeneLength,data,D)

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
        
        dataBroadcast = sc.broadcast(data)
        
        FITNESS = sc.parallelize(range(len(Chromosomes))) \
                    .map(lambda x:CalcFitness(x,Chromosomes[x].geneSerial,dataBroadcast.value,D)) \
                    .collect()
        for x in range(len(Chromosomes)):
            Chromosomes[x].fitness = copy.deepcopy(FITNESS[x])

        print("the iteration:",i)

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

