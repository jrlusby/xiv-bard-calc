#! /usr/bin/python2

from __future__ import division
import numpy
import math
import BardModel
from xivsettings import *
import copy
import Queue
from multiprocessing import Pool, Lock
printlock = Lock()

### SETTINGS ###

from mch import * # change this to include the inventory you want to calculate against
# from mrconductivitywarinv import * # change this to include the inventory you want to calculate against
# from mryaahwarinv import * # change this to include the inventory you want to calculate against

unpruneablerings = 2
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
            printlock.acquire()
            print "exceded max, pruning ", item
            printlock.release()
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
            if printintermediate:
                printlock.acquire()
                print item, " pruned by ", otherItem
                print mincaps, newval, val, comp
                printlock.release()
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
        if printintermediate:
            printlock.acquire()
            print len(itemSubset) - len(neweritemsubset)
            printlock.release()
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
        if printintermediate:
            printlock.acquire()
            print len(itemSubset) - len(neweritemsubset)
            printlock.release()
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
        if printintermediate:
            printlock.acquire()
            print indexes
            printlock.release()
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
        if printintermediate:
            print "invalid because of unique rings"
        return False
    mincomp = itemset >= mincaps
    maxcomp = itemset <= maxcaps
    return not False in mincomp and not False in maxcomp

# def gensetval(itemset): # use this if you're a bard and want precise comparisons (MrYaah Approved)
#     return gearcomparer.calc_dps(itemset[0], itemset[1], itemset[2], itemset[3], itemset[4], [itemset[6], itemset[7]])

def gensetval(itemset): # Use this for statweight calculations
    return itemValue(itemset)

def calc_bis_subset(args):
    allitems, startpoint, divisor = args
    total = countTotalSets(allitems)
    index = int(math.floor(total/divisor*startpoint)) # start
    stop = int(math.floor(total/divisor*(startpoint+1)))
    allindex = num_to_indexes(index, allitems)
    if printintermediate:
        printlock.acquire()
        print stop - index, "sets being compared from", index, stop
        print allindex
        printlock.release()
    bestindex = allindex
    bestsetval = 0
    while( index < stop ):
        newset = sumset(allitems, allindex)
        # print newset, newval
        if(isValid(newset, allitems, allindex)):
            newval = gensetval(newset)
            if(newval >= bestsetval):
                bestset = newset
                bestsetval = newval
                bestindex = list(allindex)
                if printintermediate:
                    printlock.acquire()
                    print newval, newset
                    printSet(allitems, bestindex)
                    printlock.release()
        increment(allitems, allindex)
        index += 1
    return bestindex

def calc_bis(allitems):
    divisor = 7
    inputset = []
    for i in range(divisor):
        inputset.append((allitems, i, divisor))
    p = Pool(divisor)
    bestsubsets = p.map(calc_bis_subset, inputset)
    if printintermediate:
        print bestsubsets
    maxval = 0
    bestsubset = 0
    for subset in bestsubsets:
        newset = sumset(allitems, subset)
        newval = gensetval(newset)
        if newval > maxval:
            bestsubset = subset
            maxval = newval
    return bestsubset





def countTotalSets(inventory):
    total = 1
    for slot in inventory:
        total *= len(slot)
    # print total, "possible set combinations"
    return total

def num_to_indexes(number, lengthlist):
    indexes = [0] * len(lengthlist)
    for i in range(len(lengthlist)):
        length = len(lengthlist[i])
        indexes[i] = number % length
        number = int(number / length)
    return indexes



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

def verifyMinCaps(inventory):
    for stat in range(len(mincaps)):
        if mincaps[stat] > 0:
            total = basestats[stat]
            for slot in inventory[:-1]:
                slotmaxstat = 0
                for item in slot:
                    if item[0][stat] > slotmaxstat:
                        slotmaxstat = item[0][stat]
                # print type(slotmaxstat)
                total += slotmaxstat
            print total


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
    # prunedItems = pruneSet(allitems)
    prunedItems = allitems
    verifyMinCaps(prunedItems)
    countTotalSets(prunedItems)
    acc = minacc
    sks = minsks
    while acc <= maxacc or sks <= maxsks:
        sks = minsks
        thisset = [0,0]
        while sks <= maxsks:
            print "--------------------------------------------------------------------------------"
            mincaps[1] = acc
            mincaps[4] = sks
            # bestset = calc_bis_subset((prunedItems, 0, 1))
            bestset = calc_bis(prunedItems)
            thisset = sumset(prunedItems, bestset)
            if thisset[4] < sks:
                break
            print gensetval(thisset), thisset
            printSet(prunedItems, bestset)
            sks = thisset[4]+1
        print acc, thisset[1]
        if thisset[1] < acc:
            break
        acc = thisset[1]+1

# print allindex
# # print pruneItem(item, bracelets, cJob.weights, mincaps, maxcaps, elzenbasestats)
