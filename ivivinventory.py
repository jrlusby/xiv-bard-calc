from barditems import *
from food import *

weapon = [zetabow]

kirimuhatacccap = [[24, 25, 25, 18, 6, 28, 0, 0], "Kirimu Tricorne"]
kirimuhatnocap = [[24, 24, 25, 18, 9, 28, 0, 0], "Kirimu Tricorne"]
kirimuhatlesscrit = [[24, 25, 24, 18, 9, 28, 0, 0], "Kirimu Tricorne"]
head = [kirimuhatacccap, kirimuhatnocap, kirimuhatlesscrit, demonhat, aironhat, dreadhat]

kirimuweirdcheap = [[39, 41, 33, 26, 0, 46, 0, 0], "Kirimu Coat"]
body = [kirimuchest1, kirimuweirdcheap, demonchest, aironworkschest, dreadchest]

kirimuglovesacccap = [[24, 25, 25, 18, 6, 28, 0, 0], "Kirimu Bracers"]
kirimuglovesnocap = [[24, 24, 25, 18, 9, 28, 0, 0], "Kirimu Bracers"]
kirimugloveslesscrit = [[24, 25, 24, 18, 9, 28, 0, 0], "Kirimu Bracers"]
hands = [kirimuglovesacccap, kirimuglovesnocap, kirimugloveslesscrit, airongloves, dreadgloves, demongloves]


waist = [arachnesash1, arachnesash3, aironbelt, dreadbelt, demonbelt]

legs = [kirimupants1, kirimupants2, aironpants, dreadpants, demonpants]

ivivfeet1 = [[24, 25, 25, 18, 6, 28, 0, 0], "Kirimu Boots of Aiming"]
ivivfeet2 = [[24, 25, 24, 18, 9, 28, 0, 0], "Kirimu Boots of Aiming"]
feet = [ivivfeet1, ivivfeet2, aironfeet, dreadfeet, demonfeet]

necklace = [scarfdetcap, scarfcritcap, aironchoak, dreadchoak]

earrings = [plateardetcap, platearacccap, aironearings, dreadear]

bracelets = [aironwrists, dreadwrists]

rings = [platring1, platring2, aironring, dreadring, ironring]
numuniquerings = 3 # unique rings go on end of list
unpruneablerings = 1 # just put the ironworks ring at the end and leave this as 1

food = [flintcaviar, steamedcatfish, btrisotto]

allitems = [weapon, head, body, hands, waist, legs, feet, necklace, earrings, bracelets, rings, rings, food] # weapon
