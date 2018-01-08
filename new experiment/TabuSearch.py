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


class TabuSearch:

    def __init__(self, tabuMaxLength, maxIter, maxNumCandidate, surrogateFlag, po, D, alpha, beta, blockMax):
        self.m_TabuList = []
        self.m_CandidateList = []
        self.m_TabuMaxLength = tabuMaxLength
        self.m_MaxIter = maxIter
        self.m_MaxNumCandidate = maxNumCandidate
        self.m_SurrogateFlag = surrogateFlag
        self.m_PO = po
        self.m_D = D
        self.m_Alpha = alpha
        self.m_Beta = beta
        self.m_CurrentSolution = self.generateRandomChromosome()
        self.m_BestSolution = self.m_CurrentSolution
        self.m_BlockMax = blockMax
        self.m_Block = 0


    def evaluate(self):
        iter = 0
        while iter < self.m_MaxIter:# and self.m_Block < self.m_BlockMax:
            # randomly decide the transformation method, 0 for swap, 1 for add(reduce) 1
            self.m_CandidateList = []
            for _ in range(self.m_MaxNumCandidate):
                flag = randint(0, 1)
                chromosome = Chromosome()
                chromosome.geneSerial = self.m_CurrentSolution.geneSerial
                if flag == 0:
                    pointA = randint(0, len(self.m_CurrentSolution.geneSerial) - 1)
                    pointB = randint(0, len(self.m_CurrentSolution.geneSerial) - 1)
                    tmp = chromosome.geneSerial[pointA]
                    chromosome.geneSerial[pointA] = chromosome.geneSerial[pointB]
                    chromosome.geneSerial[pointB] = tmp
                else:
                    pointA = -1
                    pointB = randint(0, len(self.m_CurrentSolution.geneSerial) - 1)
                    chromosome.geneSerial[pointB] = (chromosome.geneSerial[pointB] + 1) % self.m_PO.PROVIDERS[
                        pointB].cnt
                if (flag, pointA, pointB) not in set(self.m_TabuList):
                    if self.m_SurrogateFlag:
                        chromosome.fitness, chromosome.mmd, chromosome.sigmaCapacity, chromosome.sigmaCost, chromosome.sigmaDemand = self.calcFitnessWithSurrogate(
                            chromosome.geneSerial, self.m_PO, self.m_D)
                    else:
                        chromosome.fitness, chromosome.mmd, chromosome.sigmaCapacity, chromosome.sigmaCost, chromosome.sigmaDemand = self.calcFitness(
                            chromosome.geneSerial, self.m_PO, self.m_D)
                    self.m_CandidateList.append((chromosome, chromosome.fitness, (flag, pointA, pointB)))

            nextBestChromosome, nextBestFitness, tabu = sorted(self.m_CandidateList, key=lambda x: x[1], reverse=True)[
                0]

            if self.m_BestSolution.fitness <= nextBestFitness:
                self.m_BestSolution = copy.deepcopy(nextBestChromosome)
                self.m_Block = 0
            elif math.fabs(self.m_BestSolution.fitness - nextBestFitness) <= 0.00001:
                self.m_Block += 1

            if len(self.m_TabuList) >= self.m_TabuMaxLength:
                self.m_TabuList.pop(0)
            self.m_TabuList.append(tabu)
            self.m_CurrentSolution = nextBestChromosome
            #print iter, "th iteration"
            #print "the current individual serial, fitness, mmd, sigmaCost, sigmaCapacity, sigmaDemand ", \
            #    self.m_CurrentSolution.geneSerial, self.m_CurrentSolution.fitness, self.m_CurrentSolution.mmd, self.m_CurrentSolution.sigmaCost, self.m_CurrentSolution.sigmaCapacity, self.m_CurrentSolution.sigmaDemand
            print self.m_CurrentSolution.sigmaCost
            iter += 1

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


if __name__ == "__main__":
    # po is data contains informantion about PROVIDERS and CUSTOMERS
    po = PO()
    # read providers and customers data from text
    po.PROVIDERS, po.CUSTOMERS = LoadDataFromText(r"data6.txt")

    tabuMaxLength = 20
    maxIter = 100
    maxNumCandidate = 300
    surrogateFlag = False
    D = 40.0
    alpha = 10000000.00
    beta = 0.01
    blockMax = 5

    tabuSearch = TabuSearch(tabuMaxLength, maxIter, maxNumCandidate, surrogateFlag, po, D, alpha, beta, blockMax)
    tabuSearch.evaluate()
    print "the best solution"
    print "serial, fitness, mmd, sigmaCost, sigmaCapacity, sigmaDemand ", \
        tabuSearch.m_BestSolution.geneSerial, tabuSearch.m_BestSolution.fitness, tabuSearch.m_BestSolution.mmd, tabuSearch.m_BestSolution.sigmaCost, tabuSearch.m_BestSolution.sigmaCapacity, tabuSearch.m_BestSolution.sigmaDemand