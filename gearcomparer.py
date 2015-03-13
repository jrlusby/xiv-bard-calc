#! /usr/bin/python2
import random
import math

def abilitydamage(WD, STR, DTR, potency):
    return (WD*.2714745 + STR*.1006032 + (DTR-202)*.0241327 + WD*STR*.0036167 + WD*(DTR-202)*.0010800 - 1) * (potency/100)

def autoattackdamage(WD, STR, DTR, weapon_delay):
    return (WD*.2714745 + STR*.1006032 + (DTR-202)*.0241327 + WD*STR*.0036167 + WD*(DTR-202)*.0022597 - 1) * (weapon_delay/3)

def sumdps(STR, CRIT, DTR, SS, WD, weapon_delay):
    cdmodifier = 1.25 # this was from the original spreadsheet, for barrage and other cds TODO remove

    critrate = (CRIT*0.0697-18.437)/100
    critrate = critrate+.1 # straight shot
    critrate = critrate+(.1*1.0/4)
    critmodifier = 1 + 0.5*critrate
    potency = bardrotation(critrate, SS)
    auto = autoattackdamage(WD, STR, DTR, weapon_delay)/weapon_delay*cdmodifier*critmodifier
    ability = abilitydamage(WD, STR, DTR, potency)
    noir = (auto+ability)*(1+.1*1.0/4.0)
    print "DEX, pot, auto, ability", STR, potency, auto, ability, noir

    # ircritrate = critrate+.1
    # ircritmodifier = 1 + 0.5*ircritrate
    # irpotency = bardrotation(ircritrate, SS)
    # irauto = autoattackdamage(WD, STR, DTR, weapon_delay)/weapon_delay*cdmodifier*ircritmodifier
    # irability = abilitydamage(WD, STR, DTR, irpotency)
    # ir = (irauto+irability)

    # return ir*15/60 + noir*45/60
    return noir

# expects weapon as a 2 element list of format [WeaponDamage, Delay]
def calc_weights(STR, ACC, CRIT, DTR, SKS, WEP):
    SKS = SKS - 341
    # partybuff = 1.03
    partybuff = 1.0
    hawkeseye = 1 + (.15*20/90)
    buffs = hawkeseye
    # STR = math.floor(STR*partybuff*hawkeseye)
    base = sumdps(STR*buffs, CRIT, DTR, SKS, WEP[0], WEP[1])
    strinc = sumdps((STR+5)*buffs, CRIT, DTR, SKS, WEP[0], WEP[1])-base
    detinc = sumdps(STR*buffs, CRIT, DTR+5, SKS, WEP[0], WEP[1])-base
    critinc = sumdps(STR*buffs, CRIT+5, DTR, SKS, WEP[0], WEP[1])-base
    wdinc = sumdps(STR*buffs, CRIT, DTR, SKS, WEP[0]+5, WEP[1])-base
    ssinc = sumdps(STR*buffs, CRIT, DTR, SKS+5, WEP[0], WEP[1])-base
    print strinc, detinc, critinc, wdinc, ssinc
    return [strinc/strinc, 0, critinc/strinc, detinc/strinc, ssinc/strinc, wdinc/strinc]

# calculates weights from current set, gives fairly useless numbers should be ignored
def calc_value(STR, ACC, CRIT, DTR, SKS, WEP):
    weights = calc_weights(STR, ACC, CRIT, DTR, SKS, WEP)
    value = STR*weights[0] + ACC*weights[1] + CRIT*weights[2] + DTR*weights[3] + SKS*weights[4] + WEP[0]*weights[5]
    return value

def calc_staticvalue(STR, ACC, CRIT, DTR, SKS, WEP, weights):
    value = STR*weights[0] + ACC*weights[1] + CRIT*weights[2] + DTR*weights[3] + SKS*weights[4] + WEP[0]*weights[5]
    return value

def calc_dps(STR, ACC, CRIT, DTR, SKS, WEP):
    SKS = SKS - 341
    partybuff = 1.03
    hawkeseye = 1 + (.15*20/90)
    STR = math.floor(STR*partybuff*hawkeseye)
    base = sumdps(STR, CRIT, DTR, SKS, WEP[0], WEP[1])
    return base

def bardrotation(critrate, SS):
    delay = 2.5-0.01*SS/10.5
    stupid = 1.2
    critmodifier = 1 + 0.5*critrate
    blprocrate = .5
    blonhit = 150

    constantdotrotationpps = bardpotcalc(4, critmodifier, delay)*stupid
    dropdotrotationpps = bardpotcalc(5, critmodifier, delay)*stupid

    ogcdpps = (350.0/60 + 50.0/30 + 80.0/30)*critmodifier*stupid
    rotationpps = max(dropdotrotationpps, constantdotrotationpps)
    BLFactor = blpersec(critrate)*150*critmodifier*stupid

    return BLFactor + rotationpps + ogcdpps

def bardpotcalc(heavyshots, critmodifier, delay): #assumes singletarget, 2 dots
    hsonhit = 150
    wbonhit = 60
    wbdot = 45
    vbonhit = 100
    vbdot = 35
    ssonhit = 140

    gcdcount = 3+heavyshots
    duration = delay*gcdcount
    dotticktime = min(duration, 18)
    numticks = dotticktime/3
    totalpotency = ssonhit*1.5 + (vbonhit+wbonhit+heavyshots*hsonhit + (vbdot+wbdot)*numticks)*critmodifier

    return totalpotency/duration

def simulatedblpersec(critrate):
    dotticks = 80000000 #+1) *3 = seconds
    numBL = 1
    numFails = 0
    prochance = blchance(critrate, 2)
    for i in range(dotticks):
        if random.random() < prochance:
            numFails = 0
            numBL = numBL + 1
        else:
            numFails = numFails + 1
            if numFails == 5:
                numFails = 0
                numBL = numBL + 1
    return numBL/((dotticks+1)*3.0)


def blchance(critrate, numDots):
    blprocrate = .5
    return 1 - (1-critrate*blprocrate)**numDots

def andrewblchance(critrate, numDots):
    blprocrate = .5
    total = 0
    p = critrate*blprocrate
    for i in range(1, numDots+1):
        total = total + p*(1-p)**(i-1)
    return total

def blpersec(critrate):
    A = blchance(critrate, 2)
    timeperbl = 3*A + 6*A*(1-A) + 9*A*(1-A)**2 + 12*A*(1-A)**3 + 15*(1-A)**4
    blps = 1/timeperbl
    return blps

def main():
    newbardweights = [1.0, 0, 0.267, 0.332, 0.116, 9.909]

    dreadbow = [52, 3.2]
    augmentedironworksbow = [51, 3.04]
    yoichibow = [50, 3.04]
    highallaganbow = [48, 3.36]
    zetabow = [52, 3.04]

    weights = calc_weights(664, 536, 520, 338, 389, zetabow)
    # weights = calc_dps(664, 536, 520, 338, 394, zetabow)
    print weights
    # weights2 = calc_weights(664, 536, 710, 338, 389, zetabow)
    # print weights2

if __name__ == "__main__":
    main()
