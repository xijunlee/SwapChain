from __future__ import print_function

import sys
import math


# import numpy as np
# from pyspark import SparkContext
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
        self.geneLength = 0


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
                ws = min(ws,self.O[len(chain)-1].demand)
                
                for i in range(1,len(chain)-1):
                    if i%2 == 1:
                        tmpo = chain[i]
                        tmpp = chain[i+1] - len(self.O)
                        for tmp in self.Assignment:
                            if tmp.o == tmpo and tmp.p == tmpp:
                                ws = min(min,tmp.w)
                                break
                for i in range(1,len(chain)-1):
                    if i%2 == 1:
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
                for i in range(0,len(chain)):
                    if i%2 == 0:
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
        for i in range(0,10*(len(self.O)+len(self.P))):
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
        
        if flag == True:
            return chain
        else:
            return flag

    def find_d_satisfiable(self):
        hash = []
        myQueue = []
        haveFound = False
        for i in range(0,len(self.O)+len(self.P)):
            hash.append(0)
        for i in range(0,10*(len(self.O)+len(self.P))):
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
        
        """"self.Assignment = sorted(self.Assignment,key = self.returnDis)
        # print for debug
        for i in range(0,len(self.Assignment)):
            print(self.Assignment[i].o, self.Assignment[i].p, self.Assignment[i].w, self.Assignment[i].dis)"""
        


def CalcFitness(chromosomeNo, geneSerial, data):
    """
        usage ChromosomeNumber,geneSerial,data
        return fitness for this Chromosome
    """
    customers = data.CUSTOMERS
    providers = []
    for i in range(0,len(geneSerial)):
        tmpProvider = Provider()
        tmpProvider.x = data.PROVIDERS[i].x
        tmpProvider.y = data.PROVIDERS[i].y
        tmpProvider.capacity = data.PROVIDERS[i].capacity[geneSerial[i]]
        tmpProvider.cost = data.PROVIDERS[i].cost[geneSerial[i]]
        providers.append(tmpProvider)
    swapchainsolver = SwapChainSolver(providers, customers)
    return swapchainsolver.Solver()
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
    po.PROVIDERS, po.CUSTOMERS = LoadDataFromText(r"alldata.txt")
    gs = [0, 0, 0, 0, 0, 0]
    mmd = CalcFitness(0, gs, po)
    print(mmd)
