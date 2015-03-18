from barditems import *
from food import *

yaahkirimuhat = [[24, 21, 25, 18, 9, 28, 0, 0], "Kirimu Tricorne"]
yaahkirimuchest = [[39, 41, 36, 20, 0, 46, 0, 0], "Kirimu Coat"]
yaahkirimugloves = [[24, 25, 25, 18, 0, 28, 0, 0], "Kirimu Bracers"]
yaaharachnesash = [[18, 15, 19, 13, 13, 21, 0, 0], "Arachne Sash"]
yaahkirimupants = [[39, 41, 36, 20, 0, 46, 0, 0], "Kirimu Brais"]
yaahkirimufeet = [[24, 25, 25, 18, 0, 28, 0, 0], "Kirimu Boots of Aiming"]
yaahplatear = [[18, 15, 19, 13, 0, 0, 0, 0], "Platinum Earrings of Ranging"]
yaahplatring = [[18, 18, 19, 13, 0, 0, 0, 0], "Platinum Ring of Ranging", 1]


weapon = [augmentedironworksbow]
head = [yaahkirimuhat, demonhat, aironhat, dreadhat]
body = [yaahkirimuchest, demonchest, aironworkschest, dreadchest]
hands = [yaahkirimugloves, airongloves, demongloves]
waist = [yaaharachnesash, aironbelt, demonbelt, dreadbelt]
legs = [yaahkirimupants, demonpants, aironpants]
feet = [yaahkirimufeet, aironfeet, dreadfeet, demonfeet]
necklace = [aironchoak, dreadchoak]
earrings = [yaahplatear, aironearings]
bracelets = [aironwrists, dreadwrists]
rings = [yaahplatring, dreadring, aironring, ironring]
unpruneablerings = 1 # just put the ironworks ring at the end and leave this as 1
food = [flintcaviar, omlettes, steamedcatfish, btrisotto]
# food = [omlettes, toadlegs, btrisotto]
allitems = [weapon, head, body, hands, waist, legs, feet, necklace, earrings, bracelets, rings, rings, food] # weapon
