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
from Chromosome import Chromosome
from FileProcess import *

class GA:
    def __init__(self, maxIter, maxBlock, populationSize, probMutate, probCross, probSelect, D, po, alpha, beta, surrogateFlag):
        self.m_MaxIter = maxIter
        self.m_MaxBlock = maxBlock
        self.m_PopulationSize = populationSize
        self.m_Population = []
        self.m_SurrogateFlag = surrogateFlag

        self.m_ProbMutate = probMutate
        self.m_ProbCross = probCross
        self.m_ProbSelect = probSelect
        self.m_PO = po
        self.m_D = D
        self.m_Alpha = alpha
        self.m_Beta = beta
        self.m_Block = 0

        for _ in range(self.m_PopulationSize):
            self.m_Population.append(self.generateRandomChromosome())
        tmp = sorted(self.m_Population, key=lambda x:x.fitness, reverse=True)
        self.m_BestSolution = tmp[0]
        self.m_BestFitness = self.m_BestSolution.fitness

    def select(self):
        nextPopulation = []
        pi = []
        fitnessSum = 0
        self.m_Population = sorted(self.m_Population, key=lambda x:x.fitness)
        nextPopulation.append(copy.deepcopy(self.m_Population[-1]))

        for ind in self.m_Population:
            fitnessSum = fitnessSum + ind.fitness
        pi.append(self.m_Population[0].fitness / fitnessSum)
        for ri in range(1, len(self.m_Population)):
            pi.append(self.m_Population[ri].fitness / fitnessSum + pi[ri - 1])
        copyNum = len(self.m_Population) - 1
        for ri in range(1, len(self.m_Population)):
            randnum = random.random()
            for j in range(len(pi)):
                if randnum <= pi[j]:
                    copyNum = j
                    break
            nextPopulation.append(copy.deepcopy(self.m_Population[copyNum]))
        self.m_Population = nextPopulation

    def crossover(self):
        # chromosomes cross
        hash = []
        for ci in range(len(self.m_Population)):
            hash.append(0)
        hash[0] = 1
        for ci in range(1, len(self.m_Population) / 2):
            hash[ci] = 1
            j = 0
            while hash[j] == 1:
                j = len(self.m_Population) / 2 + randint(0, len(self.m_Population) / 2 - 1)
            hash[j] = 1
            if random.random() > self.m_ProbCross:
                # cross gene between pointA and pointB
                pointA = randint(0, len(self.m_Population[0].geneSerial) - 1)
                pointB = randint(0, len(self.m_Population[0].geneSerial) - 1)
                if pointA >= pointB:
                    tmp = pointA
                    pointA = pointB
                    pointB = tmp
                if ci != 0 and j != 0:
                    for k in range(pointA, pointB + 1):
                        tmp = self.m_Population[ci].geneSerial[k]
                        self.m_Population[ci].geneSerial[k] = self.m_Population[j].geneSerial[k]
                        self.m_Population[j].geneSerial[k] = tmp

    def mutate(self):
        # chromosomes mutation
        for k in range(0, int(len(self.m_Population) * len(self.m_Population[0].geneSerial) * self.m_ProbMutate) + 1):
            mi = randint(0, len(self.m_Population) - 1)
            ik = randint(0, len(self.m_Population[0].geneSerial) - 1)
            vk = randint(0, self.m_PO.PROVIDERS[ik].cnt - 1)
            self.m_Population[mi].geneSerial[ik] = vk

    def calcPopulationFitness(self):
        for chromosome in self.m_Population:
            if self.m_SurrogateFlag:
                chromosome.fitness, chromosome.mmd, chromosome.sigmaCapacity, chromosome.sigmaCost, chromosome.sigmaDemand = self.calcFitnessWithSurrogate(
                    chromosome.geneSerial, self.m_PO, self.m_D)
            else:
                chromosome.fitness, chromosome.mmd, chromosome.sigmaCapacity, chromosome.sigmaCost, chromosome.sigmaDemand = self.calcFitness(
                    chromosome.geneSerial, self.m_PO, self.m_D)


    def evaluate(self):
        iter = 0
        while iter < self.m_MaxIter: #and self.m_Block < self.m_MaxBlock:
            #print "the " + str(iter) + " th iteration"
            self.select()
            self.crossover()
            self.mutate()
            self.calcPopulationFitness()
            sortedPopulation = sorted(self.m_Population, key=lambda x: x.fitness, reverse=True)
            if sortedPopulation[0].fitness > self.m_BestFitness:
                self.m_BestFitness = sortedPopulation[0].fitness
                self.m_BestSolution = copy.deepcopy(sortedPopulation[0])
                self.m_Block = 0
            elif math.fabs(sortedPopulation[0].fitness - self.m_BestFitness) <= 0.00001:
                self.m_Block += 1

            #print "the best individual serial, fitness, mmd, sigmaCost, sigmaCapacity, sigmaDemand ",\
            #    sortedPopulation[0].geneSerial, sortedPopulation[0].fitness,sortedPopulation[0].mmd, sortedPopulation[0].sigmaCost, sortedPopulation[0].sigmaCapacity, sortedPopulation[0].sigmaDemand
            print sortedPopulation[0].sigmaCost

            iter += 1


    def generateRandomChromosome(self):
        chromosome = Chromosome()
        for i in range(len(self.m_PO.PROVIDERS)):
            chromosome.geneSerial.append(randint(0, self.m_PO.PROVIDERS[i].cnt - 1))
        if self.m_SurrogateFlag:
            chromosome.fitness, chromosome.mmd, chromosome.sigmaCapacity, chromosome.sigmaCost, chromosome.sigmaDemand = self.calcFitnessWithSurrogate(
                chromosome.geneSerial, self.m_PO, self.m_D)
        else:
            chromosome.fitness, chromosome.mmd, chromosome.sigmaCapacity, chromosome.sigmaCost, chromosome.sigmaDemand = self.calcFitness(
                chromosome.geneSerial, self.m_PO, self.m_D)
        return chromosome

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
        mmd = self.m_D * 1000.0
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
                fitness = -4.0
            else:
                if sigmaCost != 0:
                    fitness = float(4.0 / sigmaCost)
                else:
                    fitness = 8.0
        else:
            fitness = -8.0
        # print("fitness,mmd,sigmaCapacity,sigmaCost,sigmaDemand:",fitness,mmd,sigmaCapacity,sigmaCost,sigmaDemand)
        return math.exp(fitness), mmd, sigmaCapacity, sigmaCost, sigmaDemand

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
        mmd = self.m_D * 1000.0
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
                    fitness = float(4.0 / sigmaCost)
                else:
                    fitness = 8.0
            else:
                fitness = -6.0
        else:
            fitness = -8.0
        # print"fitness,mmd,sigmaCapacity,sigmaCost,sigmaDemand:",fitness,mmd,sigmaCapacity,sigmaCost,sigmaDemand
        return math.exp(fitness), mmd, sigmaCapacity, sigmaCost, sigmaDemand

if __name__ == "__main__":
    # po is data contains informantion about PROVIDERS and CUSTOMERS
    po = PO()
    # read providers and customers data from text
    po.PROVIDERS, po.CUSTOMERS = LoadDataFromText(r"data6.txt")

    maxIter = 100
    maxBlock = 5
    populationSize = 300
    probMutate = 0.00001
    probCross = 0.7
    probSelect = 0.1
    D = 40.0
    alpha = 10000000.00
    beta = 0.01
    surrogateFlag = False

    ga = GA(maxIter,maxBlock,populationSize,probMutate,probCross,probSelect,D,po,alpha,beta,surrogateFlag)
    ga.evaluate()
    print "the best solution serial, fitness, mmd, sigmaCost, sigmaCapacity, sigmaDemand ", \
        ga.m_BestSolution.geneSerial, ga.m_BestSolution.fitness, ga.m_BestSolution.mmd, ga.m_BestSolution.sigmaCost, ga.m_BestSolution.sigmaCapacity, ga.m_BestSolution.sigmaDemand


