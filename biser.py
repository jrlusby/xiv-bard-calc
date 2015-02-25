#! /usr/bin/python2

import numpy
import math
import gearcomparer

from bardinventory import * # change this to include the inventory you want to calculate against

statweights = bardweights

def itemValue(item, weights):
    return numpy.sum(numpy.array(item)*numpy.array(weights[:-1]))

def setValue(armorset, weapon, weights):
    return itemValue(armorset, weights)+weapon[0]*weights[-1]

def pruneMaxItems(item, itemSet, weights, mincap, maxcap, basestats):
    for i in range(len(maxcap)):
        if item[i] > maxcap[i]-basestats[i]:
            return True
    return False

def pruneItem(item, itemSet, weights, mincap, maxcap, basestats):
    val = itemValue(item, weights)
    caps = mincap*item
    for otherItem in itemSet:
        newval = itemValue(otherItem, weights)
        newcaps = mincap*otherItem
        comp = caps > newcaps # does item have higher stat for any mincap required item?
        if newval*.98 > val and not True in comp:
            return True
    return False

def pruneSet(itemSet, weights, mincap, maxcap, basestats):
    newset = []
    for itemSubset in itemSet[:-2]:
        newitemsubset = []
        for item in itemSubset:
            if not pruneMaxItems(item, itemSubset, weights, mincap, maxcap, basestats):
                newitemsubset.append(item)
        for item in newitemsubset:
            if pruneItem(item, itemSubset, weights, mincap, maxcap, basestats):
                newitemsubset.remove(item)
        newset.append(newitemsubset)
    for itemSubset in itemSet[-2:]:
        newset.append(itemSubset)
    return newset

def sumset(armorset, indexes, base):
    for i in range(len(indexes)):
        base = numpy.add(base, armorset[i][indexes[i]])
    accplus = min(math.floor(base[1]*.03), 16)
    critplus = min(math.floor(base[2]*.05), 33)
    vitplus = min(math.floor(base[5]*.05), 28)
    base = numpy.add(base, [0, accplus, critplus, 0, 0, vitplus])
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

def isValid(itemset, allgears, indexes):
    mincomp = itemset >= mincaps
    maxcomp = itemset <= maxcaps
    if indexes[-1] == indexes[-2] and indexes[-1] >= len(allgears[-1]) - numuniquerings:
        return False
    return not False in mincomp and not False in maxcomp

def gensetval(itemset): # use this if you're a bard and want precise comparisons (MrYaah Approved)
    weapon = [52, 3.04] # zetabow
    return gearcomparer.calc_dps(itemset[0], itemset[1], itemset[2], itemset[3], itemset[4], weapon)

# def gensetval(itemset): # Use this for statweight calculations
#     weapon = [52, 3.04] # zetabow
#     return setValue(itemset, weapon, statweights)

def calc_bis(allitems, allindex, basestats):
    bestset = sumset(allitems, allindex, basestats)
    bestsetval = gensetval(bestset)
    print bestsetval
    while(not increment(allitems, allindex)):
        newset = sumset(allitems, allindex, basestats)
        if(isValid(newset, allitems, allindex)):
            newval = gensetval(newset)
            if(newval > bestsetval):
                bestset = newset
                bestsetval = newval
                print bestsetval, bestset, allindex
    print allindex

def printSet(itemSet, indexes):
    for i in range(len(indexes)):
        print itemSet[i][indexes[i]]


prunedItems = pruneSet(allitems, statweights, mincaps, maxcaps, elzenbasestats)
print numpy.array(prunedItems)
calc_bis(prunedItems, allindex, elzenbasestats)
print allindex
# print pruneItem(item, bracelets, statweights, mincaps, maxcaps, elzenbasestats)
