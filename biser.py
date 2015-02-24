#! /usr/bin/python2

import numpy
import math
import gearcomparer

from bardinventory import * # change this to include the inventory you want to calculate against

def calc_effectivedex(gearset, wd):
    seedweights = [1.0, 0, 0.339, 0.320, 0.161, 0]
    wd = [9.429]
    return numpy.sum(numpy.array(gearset)*numpy.array(seedweights))+52*wd[0]

def pruneItems(itemset):
    wd = [9.429]
    i = j = 0
    for i in range(len(itemset)):
        myval = calc_effectivedex(itemset[i])
        print myval, i
        mycaps = caps*itemset[i]
        for j in range(len(itemset)):
            newval = calc_effectivedex(itemset[j], seedweights)
            newcaps = caps*itemset[j]
            comp = mycaps > newcaps
            if newval > myval and not True in comp:
                print "prune item", i, "beat by", j, "dif", newval-myval

def sumset(fullcombo, indexes, base):
    for i in range(0, 11):
        base = numpy.add(base, allitems[i][allindex[i]])
    accplus = min(math.floor(base[1]*.03), 16)
    critplus = min(math.floor(base[2]*.05), 33)
    vitplus = min(math.floor(base[5]*.05), 28)
    base = numpy.add(base, [0, accplus, critplus, 0, 0, vitplus])
    base[4] = 341
    return base

def increment(fullcombo, indexes):
    i = 0
    while i < len(fullcombo):
        if indexes[i]+1 == len(fullcombo[i]):
            indexes[i] = 0
            i = i + 1
        else:
            indexes[i] = indexes[i]+1
            return False
    return True

def isValid(itemset):
    comp = itemset > caps
    if itemset[4] > 385:
        return False
    return not False in comp

def calc_bis(allitems, allindex, basestats):
    bestset = sumset(allitems, allindex, basestats)
    bestsetval = gearcomparer.calc_dps(bestset[0], bestset[1], bestset[2], bestset[3], bestset[4], [52, 3.2])
    print bestsetval
    while(not increment(allitems, allindex)):
        newset = sumset(allitems, allindex, basestats)
        if(isValid(newset)):
            newval = gearcomparer.calc_dps(newset[0], newset[1], newset[2], newset[3], newset[4], [52, 3.2])
            if(newval > bestsetval):
                bestset = newset
                bestsetval = newval
                print bestsetval, bestset, allindex

calc_bis(allitems, allindex, basestats)
