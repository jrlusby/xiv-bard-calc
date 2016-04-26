#! /usr/bin/python2

import numpy
import math
import BardModel
from xivsettings import *
import copy

### SETTINGS ###

# from blm230plus import * # change this to include the inventory you want to calculate against
from tmpinv import * # change this to include the inventory you want to calculate against
# from drg240inv import * # change this to include the inventory you want to calculate against
# from mrconductivitywarinv import * # change this to include the inventory you want to calculate against
# from mryaahwarinv import * # change this to include the inventory you want to calculate against

unpruneablerings = 0
allitems = [ Arm, Head, Body, Hands, Waist, Legs, Feet, Necklace, Earrings, Bracelets, Ring, Ring, food, ]
printintermediate = False

################

def itemValue(item):
    return numpy.sum(numpy.array(item)*numpy.array(cJob.weights))

def pruneMaxItems(item):
    stats = item[0]
    for i in range(len(maxcaps)):
        # print item
        if stats[i] > maxcaps[i]-basestats[i]:
            print "exceded max, pruning ", item
            return True
    return False

def pruneItem(item, itemSet):
    prunecount = 0
    val = itemValue(item[0])
    caps = mincaps*item[0]
    for otherItem in itemSet:
        newval = itemValue(otherItem[0])
        newcaps = mincaps*otherItem[0]
        comp = caps > newcaps # does item have higher stat for any mincap required item?
        if newval > val and not True in comp:
            print item, " pruned by ", otherItem
            prunecount = prunecount + 1
            if len(otherItem) == 3:
                prunecount = prunecount + otherItem[2]
    return prunecount

def pruneSet(itemSet):
    newset = []
    # prune all the non rings
    for itemSubset in itemSet[:-3]:
        newitemsubset = []
        for item in itemSubset:
            if not pruneMaxItems(item):
                newitemsubset.append(item)
        neweritemsubset = []
        for item in newitemsubset:
            if pruneItem(item, newitemsubset) < 1:
                neweritemsubset.append(item)
        newset.append(neweritemsubset)
        print len(itemSubset) - len(neweritemsubset)
    # prune the rings
    for itemSubset in itemSet[-3:-1]:
        newitemsubset = []
        for item in itemSubset:
            if not pruneMaxItems(item):
                newitemsubset.append(item)
        neweritemsubset = []
        for item in newitemsubset[:-unpruneablerings]:
            if pruneItem(item, newitemsubset) < 2:
                neweritemsubset.append(item)
        neweritemsubset = neweritemsubset + newitemsubset[-unpruneablerings:]
        newset.append(neweritemsubset)
        print len(itemSubset) - len(neweritemsubset)
    # just add the food
    newset.append(itemSet[-1])
    return newset

def sumset(armorset, indexes):
    base = basestats
    for i in range(len(indexes)-1):
        # print i
        # print base
        # print armorset
        # print indexes
        base = numpy.add(base, armorset[i][indexes[i]][0])
    foodstats = []
    for i in range(len(armorset[-1][indexes[-1]][0])):
        stat = armorset[-1][indexes[-1]][0][i]
        statplus = min(math.floor(base[i]*stat[0]), stat[1])
        foodstats.append(statplus)
    base = numpy.add(base, foodstats)
    return base

incrementRing = False

def increment(inventory, indexes):
    global incrementRing
    i = 0
    if incrementRing:
        print indexes
        i = len(indexes)-3
    while i < len(inventory):
        if indexes[i]+1 == len(inventory[i]):
            indexes[i] = 0
            i = i + 1
        else:
            indexes[i] = indexes[i]+1
            if incrementRing:
                # print indexes
                incrementRing = False
            return False
    return True

def isValid(itemset, allgears, indexes):
    global incrementRing
    if allgears[-2][indexes[-2]][3] == allgears[-3][indexes[-3]][3] and allgears[-2][indexes[-2]][2] == 1:
        incrementRing = True
        # print "invalid because of unique rings"
        return False
    mincomp = itemset >= mincaps
    maxcomp = itemset <= maxcaps
    return not False in mincomp and not False in maxcomp

# def gensetval(itemset): # use this if you're a bard and want precise comparisons (MrYaah Approved)
#     return gearcomparer.calc_dps(itemset[0], itemset[1], itemset[2], itemset[3], itemset[4], [itemset[6], itemset[7]])

def gensetval(itemset): # Use this for statweight calculations
    return itemValue(itemset)

def calc_bis(allitems):
    allindex = [0]*len(allitems)
    bestindex = allindex
    bestset = sumset(allitems, allindex)
    bestsetval = 0
    while(not increment(allitems, allindex)):
        newset = sumset(allitems, allindex)
        # print newset, newval
        if(isValid(newset, allitems, allindex)):
            newval = gensetval(newset)
            if(newval >= bestsetval):
                bestset = newset
                bestsetval = newval
                bestindex = list(allindex)
                if printintermediate:
                    print newval, newset
                    printSet(allitems, bestindex)
    return bestindex

def printInventory(inventory):
    i = 0
    for slot in inventory:
        for item in slot:
            print item
            i = i + 1
    print i, "Items in set"

def printSet(inventory, indexes):
    for i in range(len(inventory)):
        print(inventory[i][indexes[i]])

def countTotalSets(inventory):
    total = 1
    for slot in inventory:
        total *= len(slot)
    print total, "possible set combinations"


# def pickNextBest(inventory, options):


# printInventory(allitems)
# printInventory(prunedItems)
# print numpy.array(prunedItems)
# startset = sumset(prunedItems, [0]*len(prunedItems))
# print startset
# print gensetval(startset)

if 'tobuy' in globals():
    for itemgroup in tobuy:
        print "--------------------------------------------------------------------------------"
        print itemgroup
        allitemscopy = copy.deepcopy(allitems)
        allitemscopy[itemgroup[0]] += itemgroup[1]
        # printInventory(allitemscopy)
        prunedItems = pruneSet(allitemscopy)
        countTotalSets(allitemscopy)
        countTotalSets(prunedItems)

        acc = minacc
        while acc <= maxacc:
            print "--------------------------------------------------------------------------------"
            mincaps[1] = acc
            bestset = calc_bis(prunedItems)
            thisset = sumset(prunedItems, bestset)
            print gensetval(thisset), thisset
            printSet(prunedItems, bestset)
            acc = thisset[1]+1
else:
    prunedItems = pruneSet(allitems)
    countTotalSets(prunedItems)
    acc = minacc
    while acc <= maxacc:
        print "--------------------------------------------------------------------------------"
        mincaps[1] = acc
        bestset = calc_bis(prunedItems)
        thisset = sumset(prunedItems, bestset)
        print gensetval(thisset), thisset
        printSet(prunedItems, bestset)
        acc = thisset[1]+1

# print allindex
# # print pruneItem(item, bracelets, cJob.weights, mincaps, maxcaps, elzenbasestats)
