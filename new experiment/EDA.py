
import math
import random
from random import randint
import copy
from sklearn.metrics import mean_squared_error
from Surrogate import Surrogate
from SwapChainSolver import SwapChainSolver
from PO import PO
from Customer import Customer
from Provider import Provider
from ProviderPlus import ProviderPlus
import numpy as np

class Chromosome:
    def __init__(self):
        self.geneSerial = []
        self.fitness = 0
        self.sigmaCost = 0
        self.sigmaDemand = 0
        self.sigmaCapacity = 0
        self.mmd = 0

class EDA:
    def __init__(self, populationSize, iterationMax, blockMax, po, alpha, beta, D, surrogateFlag, sizeRatio=0.3):

        self.m_PO = po
        self.m_D = D
        self.m_PopSize = populationSize
        self.m_iterMax = iterationMax
        self.m_Alpha = alpha
        self.m_Beta = beta
        self.m_Population = []
        self.m_BestSolution = []
        self.m_BestFitness = -65536
        self.m_BestCost = 0
        self.m_BlockMax = blockMax
        self.m_Block = 0
        self.m_Surrogate = 0
        self.m_SurrogateFlag = surrogateFlag
        # init the EDA matrix
        self.m_Matrix = [[1 for _ in range(self.m_PO.PROVIDERS[0].cnt)] for _ in range(len(self.m_PO.PROVIDERS))]
        if surrogateFlag:
            n_AllSol = len(po.PROVIDERS) ** po.PROVIDERS[0].cnt
            self.m_Surrogate = Surrogate(int(n_AllSol * sizeRatio), po)
            self.m_Surrogate.trainModel()

    def calcFitnessWithSurrogate(self, geneSerial, data, D):
        """
            usage ChromosomeNumber,geneSerial,data,D
            return fitness for this1  Chromosome
        """
        alpha = self.m_Alpha
        beta = self.m_Beta
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
        for i in range(0, len(geneSerial)):
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
            x = np.array(geneSerial).reshape(1, -1)
            mmd = self.m_Surrogate.predict(x)[0]
            if mmd > D:
                fitness = -1000
            elif mmd > 0:
                if sigmaCost != 0:
                    fitness = float(1000.0 / sigmaCost)
                else:
                    fitness = 1e8
            else:
                fitness = -1e8
        #print"fitness,mmd,sigmaCapacity,sigmaCost,sigmaDemand:",fitness,mmd,sigmaCapacity,sigmaCost,sigmaDemand
        return fitness,mmd,sigmaCapacity,sigmaCost,sigmaDemand



    def calcFitness(self, geneSerial, data, D):
        """
            usage ChromosomeNumber,geneSerial,data,D
            return fitness for this1  Chromosome
        """
        alpha = self.m_Alpha
        beta = self.m_Beta
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
        for i in range(0, len(geneSerial)):
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
                    fitness = float(1000.0 / sigmaCost)
                else:
                    fitness = 1e8
        # print("fitness,mmd,sigmaCapacity,sigmaCost,sigmaDemand:",fitness,mmd,sigmaCapacity,sigmaCost,sigmaDemand)
        return fitness, mmd, sigmaCapacity, sigmaCost, sigmaDemand

    def initializePopulation(self):
        self.m_Population = []
        for i in xrange(self.m_PopSize):
            chromosome = Chromosome()
            chromosome.geneSerial = self.sample()
            if self.m_SurrogateFlag:
                chromosome.fitness, chromosome.mmd, chromosome.sigmaCapacity, chromosome.sigmaCost, chromosome.sigmaDemand = self.calcFitnessWithSurrogate(chromosome.geneSerial,self.m_PO, self.m_D)
            else:
                chromosome.fitness, chromosome.mmd, chromosome.sigmaCapacity, chromosome.sigmaCost, chromosome.sigmaDemand = self.calcFitness(chromosome.geneSerial,self.m_PO, self.m_D)
            self.m_Population.append(chromosome)

    def update(self):
        sortedPopulation = sorted(self.m_Population, key = lambda x:x.fitness, reverse=True)

        if sortedPopulation[0].fitness > self.m_BestFitness:
            self.m_BestFitness = sortedPopulation[0].fitness
            self.m_BestSolution = copy.deepcopy(sortedPopulation[0].geneSerial)
            self.m_Block = 0
            self.m_BestCost = sortedPopulation[0].sigmaCost
        else:
            self.m_Block += 1
        #sigmaCost = 0
        #for i in range(len(self.m_BestSolution)):
        #    sigmaCost = sigmaCost + po.PROVIDERS[i].cost[self.m_BestSolution[i]]
        #print "the best individual serial, fitness, mmd, sigmaCost, sigmaCapacity, sigmaDemand ",sortedPopulation[0].geneSerial, sortedPopulation[0].fitness,sortedPopulation[0].mmd, sortedPopulation[0].sigmaCost, sortedPopulation[0].sigmaCapacity, sortedPopulation[0].sigmaDemand
        for i in range(1):
            gene = sortedPopulation[i].geneSerial
            for p in range(len(self.m_Matrix)):
                row = self.m_Matrix[p]
                row[gene[p]] += 1


    def sample(self):
        geneSerial = []
        for p in range(len(self.m_Matrix)):
            # each row is for a provider, the length of row is equal to number of capacities of the provider
            row = self.m_Matrix[p]
            rowSum = float(sum(row))
            cumulateRow = [0 for _ in range(len(row))]
            cumulateRow[0] = row[0] / rowSum
            for i in range(1,len(row)):
                cumulateRow[i] = cumulateRow[i-1]+ row[i] / rowSum
            rnd = random.random()
            for i in range(len(row)):
                if cumulateRow[i] >= rnd:
                    geneSerial.append(i)
                    break
        return geneSerial

    def evaluate(self):
        iter = 0
        while iter < self.m_iterMax and self.m_Block < self.m_BlockMax:
            print "the " + str(iter) + " th iteration"
            self.initializePopulation()
            self.update()
            iter += 1

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

if __name__ == "__main__":
    # po is data contains informantion about PROVIDERS and CUSTOMERS
    po = PO()
    # read providers and customers data from text
    po.PROVIDERS, po.CUSTOMERS = LoadDataFromText(r"alldata.txt")

    popSize = 300
    iterMax = 300
    blockMax = 10
    alpha = 10000000.00
    beta = 0.01
    D = 6.0
    surrogateFlag = False
    surrogateSizeRatio = 0.6

    eda = EDA(popSize, iterMax, blockMax, po, alpha, beta, D, surrogateFlag, surrogateSizeRatio)
    eda.evaluate()
    print "best fitness, cost, serial", eda.m_BestFitness, eda.m_BestCost, eda.m_BestSolution

