from __future__ import print_function

import sys
import math
#from pyspark import SparkContext
from random import randint
from random import random
import copy

class ProviderPlus:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.cnt = 0
        self.capacity = []
        self.cost = []


class Provider:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.capacity = 0
        self.cost = 0


class Customer:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.demand = 0


class PO:
    def __init__(self):
        self.PROVIDERS = []
        self.CUSTOMERS = []


class Chromosome:
    def __init__(self):
        self.geneSerial = []
        self.fitness = 0

class Match:
    def __init__(self):
        self.o = 0
        self.p = 0
        self.w = 0
        self.dis = 0

class Queue:
    def __init__(self):
        self.num = 0
        self.parent = 0


class SwapChainSolver:

    def __init__(self, providers, customers):
        self.P = providers
        self.O = customers
        self.Assignment = []

    def Solver(self):

        self.initiallize_assignment()
        while True:
            extremeMatch = self.find_d_satisfiable()
            if not extremeMatch:
                break
            else:
                self.swap(extremeMatch)

        self.Assignment = sorted(self.Assignment,key = self.returnDis)
        return self.Assignment[len(self.Assignment)-1].dis

    def swap(self,m):
        self.sub_match(m)
        chain = []
        while True:
            chain = self.find_chain(m)
            if not chain:
                break
            else:
                #chain breaking
                ws = float('inf')
                ws = min(ws,self.P[chain[0]-len(self.O)].capacity)
                ws = min(ws,self.O[chain[len(chain)-1]].demand)

                for i in range(1,len(chain)-1,2):
                    #if i%2 == 1:
                        tmpo = chain[i]
                        tmpp = chain[i+1] - len(self.O)
                        for tmp in self.Assignment:
                            if tmp.o == tmpo and tmp.p == tmpp:
                                ws = min(min,tmp.w)
                                break
                for i in range(1,len(chain)-1,2):
                    #if i%2 == 1:
                        tmpo = chain[i]
                        tmpp = chain[i+1] - len(self.O)
                        for tmp in self.Assignment:
                            if tmp.o == tmpo and tmp.p == tmpp:
                                tmpm = tmp
                                self.sub_match(tmp)
                                if tmpm.w != ws:
                                    tmpm.w = tmpm.w - ws
                                    self.add_match(tmpm)
                                break
                #chain matching
                for i in range(0,len(chain),2):
                        tmpo = chain[i+1]
                        tmpp = chain[i] - len(self.O)
                        tmpm = Match()
                        tmpm.o = tmpo
                        tmpm.p = tmpp
                        tmpm.w = ws
                        tmpm.dis = math.sqrt((self.O[tmpo].x-self.P[tmpp].x) ** 2 +(self.O[tmpo].y-self.P[tmpp].y) ** 2)
                        self.add_match(tmpm)

                if self.O[m.o].demand == 0:
                    break

        #post matching
        if self.O[m.o].demand > 0:
            tmpm = Match()
            tmpm.o = m.o
            tmpm.p = m.p
            tmpm.w = self.O[m.o].demand
            tmpm.dis = math.sqrt((self.O[m.o].x-self.P[m.p].x) ** 2 +(self.O[m.o].y-self.P[m.p].y) ** 2)
            self.add_match(tmpm)

    def find_chain(self,m):
        chain = []
        flag = False
        maxDis = m.dis
        Q = []
        hash = []
        for i in range(0,2*(len(self.O)+len(self.P))):
            Q.append(Queue())
            hash.append(0)
        head = 0
        tail = 0
        hash[m.o] = 1
        Q[head].num = m.o
        Q[head].parent = -1
        tail = tail + 1

        while not flag and head != tail:
            CurrentNode = Q[head].num
            if CurrentNode < len(self.O):
                for i in range(0,len(self.P)):
                    tmpDis = math.sqrt((self.O[CurrentNode].x - self.P[i].x) ** 2 + (self.O[CurrentNode].y - self.P[i].y) ** 2)
                    if tmpDis < maxDis and hash[i+len(self.O)] == 0:
                        Q[tail].num = i+len(self.O)
                        Q[tail].parent = head
                        hash[i+len(self.O)] = 1
                        tail = (tail+1)%len(Q)
            else:
                pNode = CurrentNode - len(self.O)
                if self.P[pNode].capacity == 0:
                    for tmp in self.Assignment:
                        if tmp.p == pNode and hash[tmp.o] == 0:
                            hash[tmp.o] = 1
                            Q[tail].num = tmp.o
                            Q[tail].parent = head
                            tail = (tail+1)%len(Q)
                else:
                    flag = True
                    tmp = head
                    while tmp >= 0:
                        chain.append(Q[tmp].num)
                        tmp = Q[tmp].parent
            head = (head+1)%len(Q)

        if flag:
            return chain
        else:
            return flag

    def find_d_satisfiable(self):
        hash = []
        myQueue = []
        haveFound = False
        for i in range(0,len(self.O)+len(self.P)):
            hash.append(0)
        for i in range(0,2*(len(self.O)+len(self.P))):
            myQueue.append(Queue())

        self.Assignment = sorted(self.Assignment,key = self.returnDis)
        maxDis = self.Assignment[len(self.Assignment)-1].dis

        k = len(self.Assignment) - 1
        extremeMatch = False
        while not haveFound and self.Assignment[k].dis == maxDis and k >= 0:
            for tmp in hash:
                tmp = 0
            for tmp in myQueue:
                tmp.num = 0
                tmp.parent = 0

            head = 0
            tail = 0

            hash[self.Assignment[k].o] = 1
            myQueue[head].num = self.Assignment[k].o
            myQueue[head].parent = -1
            tail += 1

            extremeMatch = self.Assignment[k]
            self.sub_match(extremeMatch)

            while head != tail and not haveFound:
                CurrentNode = myQueue[head].num

                if CurrentNode < len(self.O):
                    for i in range(0,len(self.P)):
                        tmpDis = math.sqrt((self.O[CurrentNode].x - self.P[i].x) ** 2 + (self.O[CurrentNode].y - self.P[i].y) ** 2)
                        if tmpDis < maxDis and hash[i+len(self.O)] == 0:
                            myQueue[tail].num = i+len(self.O)
                            myQueue[tail].parent = head
                            hash[i+len(self.O)] = 1
                            tail = (tail+1)%len(myQueue)
                else:
                    pNode = CurrentNode - len(self.O)
                    if self.P[pNode].capacity == 0:
                        for tmp in self.Assignment:
                            if tmp.p == pNode and hash[tmp.o] == 0:
                                hash[tmp.o] = 1
                                myQueue[tail].num = tmp.o
                                myQueue[tail].parent = head
                                tail = (tail+1)%len(myQueue)
                    else:
                        haveFound = True
                head = (head+1)%len(myQueue)

            self.add_match(extremeMatch)
            k = k-1

        if haveFound:
            return extremeMatch
        else:
            return False

    def distance(self, s):
        return s['distance']

    def returnDis(self,s):
        return s.dis

    def add_match(self,m):

        flag = False

        for tmp in self.Assignment:
            if (m.o == tmp.o and m.p == tmp.p):
                tmp.w += m.w
                flag = True
                break

        if flag == False:
            self.Assignment.append(m)

        self.P[m.p].capacity -= m.w
        self.O[m.o].demand -= m.w

    def sub_match(self,m):
        self.P[m.p].capacity += m.w
        self.O[m.o].demand += m.w

        for tmp in self.Assignment:
            if m.o == tmp.o and m.p == tmp.p:
                tmp.w -= m.w
                if tmp.w == 0:
                    self.Assignment.remove(tmp)
                break

    def initiallize_assignment(self):

        distanceList = []
        for i in range(0,len(self.O)):
            distanceList = []
            for j in range(0,len(self.P)):
                dis = math.sqrt((self.O[i].x - self.P[j].x) ** 2 + (self.O[i].y - self.P[j].y) ** 2)
                tmp = {'p': j, 'distance': dis}
                distanceList.append(tmp)

            distanceList = sorted(distanceList, key=self.distance)

            for j in range(0,len(self.P)):
                tmp = min(self.O[i].demand, self.P[distanceList[j]['p']].capacity)
                if (tmp > 0):
                    m = Match()
                    m.o = i
                    m.p = distanceList[j]['p']
                    m.w = tmp
                    m.dis = distanceList[j]['distance']
                    self.add_match(m)
                if self.O[i].demand == 0:
                    break

        self.Assignment = sorted(self.Assignment,key = self.returnDis)
        # print for debug
        '''for i in range(0,len(self.Assignment)):
            print(self.Assignment[i].o, self.Assignment[i].p, self.Assignment[i].w, self.Assignment[i].dis)
        '''
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

    Iteration = 50 #need input
    GeneLength = len(po.PROVIDERS)
    ChromosomesSize = 1000#need input
    Chromosomes = []
    ProbabilityMutation = 0.00001
    ProbabilityCross = 0.01
    ProbabilityS = 0 # unknow
    D = 40.00

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

        print("the iteration:",i)
        # need distributed computation spark to finish the task of calculating fitness
        for x in range(len(Chromosomes)):
            Chromosomes[x].fitness = CalcFitness(x,Chromosomes[x].geneSerial,po,D)
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

