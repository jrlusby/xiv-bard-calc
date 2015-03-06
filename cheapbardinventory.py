import numpy

zetabow = [57, 23, 39, 28, 0, 67]

weapon = [zetabow]

kirimuhat1 = [24, 25, 25, 18, 6, 28]
kirimuhat2 = [24, 24, 25, 18, 9, 28]
kirimuhat3 = [24, 25, 24, 18, 9, 28]
demonhat = [27, 19, 27, 0, 0, 32] # cannot be bis
aironhat = [31, 29, 0, 14, 0, 36]
dreadhat = [31, 0, 20, 0, 29, 36]

head = [kirimuhat1, kirimuhat2, kirimuhat3, demonhat, aironhat, dreadhat]

kirimuchest = [39, 41, 41, 20, 0, 46]
kirimuchest2 = [39, 41, 33, 26, 0, 46]
demonchest = [45, 0, 44, 22, 0, 52] # almost pruned
aironworkschest = [50, 33, 0, 0, 47, 59] # destroyed by kirimu chest
dreadchest = [50, 0, 0, 34, 33, 59]

body = [kirimuchest, kirimuchest2, demonchest, aironworkschest, dreadchest]

kirimugloves1 = [24, 25, 25, 18, 6, 28]
kirimugloves2 = [24, 24, 25, 18, 9, 28]
kirimugloves3 = [24, 25, 24, 18, 9, 28]
demongloves = [24, 0, 19, 0, 27, 32] #noo no no
airongloves = [31, 0, 20, 21, 0, 36]
dreadgloves = [31, 29, 0, 14, 0, 36]

hands = [kirimugloves1, kirimugloves2, kirimugloves3, airongloves, dreadgloves, demongloves]

arachnesash1 = [18, 18, 19, 13, 13, 21]
arachnesash2 = [18, 19, 18, 13, 13, 21]
arachnesash3 = [18, 18, 15, 13, 19, 21]
demonbelt = [21, 14, 0, 0, 20, 24] # yea no
aironbelt = [23, 0, 15, 15, 0, 27]
dreadbelt = [23, 22, 0, 11, 0, 27]

waist = [arachnesash1, arachnesash2, arachnesash3, aironbelt, dreadbelt, demonbelt]

kirimupants = [39, 41, 41, 20, 0, 46]
kirimupants2 = [39, 41, 33, 26, 0, 46]
demonpants = [45, 0, 0, 22, 44, 52] # loser
aironpants = [50, 47, 0, 0, 33, 59]
dreadpants = [50, 33, 47, 0, 0, 59]

legs = [kirimupants, kirimupants2, aironpants, dreadpants, demonpants]

kirimufeet = [24, 25, 25, 18, 6, 28]
kirimufeet2 = [24, 25, 24, 18, 9, 28]
demonfeet = [27, 0, 19, 19, 0, 32] # pruned again
aironfeet = [31, 20, 29, 0, 0, 36]
dreadfeet = [31, 29, 0, 0, 20, 36]

feet = [kirimufeet, kirimufeet2, aironfeet, dreadfeet, demonfeet]

scarfdetcap = [18, 19, 18, 13, 0, 0]
scarfcritcap = [18, 19, 19, 12, 0, 0]
aironchoak = [23, 15, 0, 15, 0, 0] # technically pooped on by scarf but who really has time for that?
dreadchoak = [23, 22, 0, 0, 15, 0]

necklace = [scarfcritcap, scarfdetcap, aironchoak, dreadchoak]

aironearings = [23, 22, 0, 0, 15, 0]
platear1 = [18, 18, 19, 13, 0, 0]
platear2 = [18, 19, 18, 12, 0, 0]
platear3 = [18, 9, 18, 13, 9, 0]
platear4 = [18, 0, 18, 13, 18, 0]
dreadear = [23, 15, 0, 15, 0, 0] # pruned


earrings = [platear1, platear2, platear3, platear4, aironearings, dreadear]

platwrists1 = [18, 18, 19, 0, 19, 0]
platwrists2 = [18, 19, 19, 0, 19, 0]
aironwrists = [23, 22, 0, 0, 15, 0]
dreadwrists = [23, 0, 22, 11, 0, 0]

bracelets = [platwrists1, platwrists2, aironwrists, dreadwrists]

platring1 = [18, 19, 18, 13, 0, 0]
platring2 = [18, 18, 19, 13, 0, 0]
platring3 = [18, 9, 19, 13, 9, 0]
platring4 = [18, 0, 19, 13, 18, 0]
dreadring = [23, 0, 0, 11, 22, 0] # pruned
aironring = [23, 22, 15, 0, 0, 0]
ironring = [21, 20, 14, 0, 0, 0] # wants to prune but thats only because it doesnt understand :(

rings = [platring1, platring2, platring3, platring4, dreadring, ironring, aironring] # accounting for unique rings is gonna be fun ._.
numuniquerings = 3 # keep this number accurate please, all unique rings go at the back.

allitems = [weapon, head, body, hands, waist, legs, feet, necklace, earrings, bracelets, rings, rings] # weapon
allindex = [0]*len(allitems)
elzenbasestats = [277, 341, 341, 202, 341, 200]
mincaps = numpy.array([0, 535, 0, 0, 0, 0])
maxcaps = numpy.array([10000, 10000, 10000, 10000, 10000, 10000]) #gotta set these, high, if you let 0 = no comp it has to check for 0 aka more comparisons less efficient

bardweights = [1.0, 0, 0.339, 0.320, 0.161, 0, 9.429]
