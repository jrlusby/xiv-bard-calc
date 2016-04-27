import numpy
import sys
sys.path.append("./inventories")
from food import *
from JobClass import *
### SETTINGS ###

minacc = 702
maxacc = minacc

# [DEX, ACC, CRIT, DET, SKS, VIT, WD, DELAY] you can set any of the minimum or maximum values, its fun
mincaps = numpy.array([0, minacc, 0, 0, 606, 0, 0, 0])
maxcaps = numpy.array([10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000]) # 420 is double ogcd cap according to krietor highwind

# bardweights = [1.0, 0, 0.125, 0.124, 0.070, 0, 9.806859476776257, 0]
mchweights = [1.0, 0, .300, .166, .168, 0, 13.459, 0]
rinchanweights = [1.0, 0, .21, .18, .1, 0, 13.459, 0]
blmweights = [1.0, 0, .206, .172, .413, 0, 9.971, 0]
ninweights = [1.0, 0, .215, .168, .086, 0, 12.799, 0]
warweights = [1.0, 0, .378, .303, .277, 1.0, 22.030, 0]
drgweights = [1.0, 0, .230, .168, .131, 0, 12.241, 0]

miqotebasestats = [299, 354, 354, 218, 354, 218, 0, 0]

overmeld = 0
overmeldVcount = 0
minVmeldlevel = 240
minlevel = 220
maxdefaultobtainedlvl = 220
mchfood = [sstaff, pipirapira, gsweetfish]
drgfood = [pipirapira, gsweetfish]
cheapwarfood = [morelsalad, flintcaviar, gsweetfish]
cheapmchfood = [flintcaviar, gsweetfish]
blmfood = [applestrudle]

# statweights = blmweights

mch = JobClass(rinchanweights, mchfood, 31, 2)
blm = JobClass(blmweights, blmfood, 25, 4)
nin = JobClass(ninweights, mchfood, 30, 2)
war = JobClass(warweights, cheapwarfood, 3, 3)
drg = JobClass(drgweights, drgfood, 4, 1)

basestats = miqotebasestats
cJob = drg
food = cJob.food

################
