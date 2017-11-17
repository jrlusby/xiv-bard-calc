import numpy
import sys
sys.path.append("./inventories")
from food import *
from JobClass import *
### SETTINGS ###

minacc = 699
maxacc = minacc
minsks = 0
maxsks = minsks

# [DEX, ACC, CRIT, DET, SKS, VIT, WD, DELAY] you can set any of the minimum or maximum values, its fun
mincaps = numpy.array([0, minacc, 0, 0, minsks, 0, 0, 0, 0, 0])
maxcaps = numpy.array([10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000]) # 420 is double ogcd cap according to krietor highwind

# bardweights = [1.0, 0, 0.125, 0.124, 0.070, 0, 9.806859476776257, 0]
brdweights = [1.0, 0, .366, .215, .233, 0, 16.824, 0, 0, 0]
mchweights = [1.0, 0, .366, .233, .050, 0, 16.824, 0, 0, 0]
rinchanweights = [1.0, 0, .21, .18, .1, 0, 13.459, 0]
blmweights = [1.0, 0, .206, .172, .413, 0, 9.971, 0]
ninweights = [1.0, 0, .215, .168, .086, 0, 12.799, 0, 0, 0]
warweights = [1.0, 0, .378, .303, .277, 1.0, 22.030, 0]
drgweights = [1.0, 0, .279, .207, .170, 0, 14.956, 0, 0, 0]
schweights = [1.0, 0, .181, .159, .138, 0, 9.128, 0, 0, .05]
smnweights = [1.0, 0, .181, .159, .138, 0, 9.128, 0, 0, 0]
whmweights = [1.0, 0, .2, .28, .18, 0, 9, 0, 0, .3]
astweights = [1.0, 0, .2, .28, .18, 0, 9, 0, 0, 0]

miqotebasestats = [299, 354, 354, 218, 354, 218, 0, 0, 354, 261]
smnmiquotebasestats = [295, 354, 354, 218, 354, 218, 0, 0, 354, 261]

doDamageMelds = True
overmeld = 4
overmeldVcount = 0
minVmeldlevel = 250
minlevel = 270
maxdefaultobtainedlvl = 275
mchfood = [sstaff, pipirapira, gsweetfish]
drgfood = [pomelette, cordonbleu]
cheapwarfood = [morelsalad, flintcaviar, gsweetfish]
cheapmchfood = [flintcaviar, gsweetfish]
blmfood = [applestrudle]
schfood = [pipirapira, gsweetfish]
smnfood = [pipirapira, sohmaltart, cremebrule]
whmfood = [pipirapira]
astfood = [spaghettip, pomelette]

# statweights = blmweights

mch = JobClass(mchweights, drgfood, 31, 2)
blm = JobClass(blmweights, blmfood, 25, 4)
nin = JobClass(ninweights, mchfood, 30, 2)
war = JobClass(warweights, cheapwarfood, 3, 3)
drg = JobClass(drgweights, drgfood, 4, 1)
sch = JobClass(schweights, schfood, 28, 5)
smn = JobClass(smnweights, smnfood, 27, 4)
whm = JobClass(whmweights, whmfood, 24, 5)
ast = JobClass(astweights, astfood, 33, 5)

basestats = miqotebasestats
cJob = mch
food = cJob.food

################
