import numpy
import sys
sys.path.append("./inventories")
from food import *
from JobClass import *
### SETTINGS ###

minacc = 703
maxacc = 703

# [DEX, ACC, CRIT, DET, SKS, VIT, WD, DELAY] you can set any of the minimum or maximum values, its fun
mincaps = numpy.array([0, minacc, 0, 0, 0, 0, 0, 0])
maxcaps = numpy.array([10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000]) # 420 is double ogcd cap according to krietor highwind

# bardweights = [1.0, 0, 0.125, 0.124, 0.070, 0, 9.806859476776257, 0]
mchweights = [1.0, 0, .300, .166, .168, 0, 13.459, 0]
blmweights = [1.0, 0, .206, .172, .413, 0, 9.971, 0]
ninweights = [1.0, 0, .215, .168, .106, 0, 12.799, 0]

miqotebasestats = [299, 354, 354, 218, 354, 218, 0, 0]


minlevel = 240
mchfood = [pipirapira, gsweetfish, sstaff]
blmfood = [applestrudle]

# statweights = blmweights

mch = JobClass(mchweights, mchfood, 31, 2)
blm = JobClass(blmweights, blmfood, 25, 4)
nin = JobClass(ninweights, mchfood, 30, 2)

basestats = miqotebasestats
cJob = nin
food = cJob.food

from nin240plus import * # change this to include the inventory you want to calculate against
# from mryaahinventory import * # change this to include the inventory you want to calculate against

unpruneablerings = 2
allitems = [ Arm, Head, Body, Hands, Waist, Legs, Feet, Necklace, Earrings, Bracelets, Ring, Ring, food, ]

################
