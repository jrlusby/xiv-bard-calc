#! /usr/bin/python2

# I have yet to pinpoint the reason why but for some reason my ability dps
# equation is yielding a higher number than the spreadsheet (approx +40), I
# straight copied this equation from easymodex's dps formula post and didnt
# even change the names of the variables so I'd rather prefer to trust my
# version than the excel version, also my potency numbers are slightly
# lower than the excel version, which makes it even more confusing that i'd
# get a higher abilitydps number
bardweights = [1.0, 0, 0.339, 0.320, 0.161, 9.429]
drgweights = [1.0, 0, .233, .327, .198, 9.349]
def abilitydamage(WD, STR, DTR, potency):
    return (WD*.2714745 + STR*.1006032 + (DTR-202)*.0241327 + WD*STR*.0036167 + WD*(DTR-202)*.0010800 - 1) * (potency/100)

def autoattackdamage(WD, STR, DTR, weapon_delay):
    return (WD*.2714745 + STR*.1006032 + (DTR-202)*.0241327 + WD*STR*.0036167 + WD*(DTR-202)*.0022597 - 1) * (weapon_delay/3)

def sumdps(STR, CRIT, DTR, SS, WD, weapon_delay):
    potency = bardrotation(CRIT, SS)
    critrate = (CRIT*0.0697-18.437)/100 + 0.1*15/60 + .1
    critmodifier = 1 + 0.5*critrate
    cdmodifier = 1.25 # this was from the original spreadsheet, for barrage and other cds
    auto = autoattackdamage(WD, STR, DTR, weapon_delay)/weapon_delay*cdmodifier*critmodifier
    ability = abilitydamage(WD, STR, DTR, potency)
    return auto+ability

# expects weapon as a 2 element list of format [WeaponDamage, Delay]
def calc_weights(STR, ACC, CRIT, DTR, SKS, WEP):
    SKS = SKS - 341
    base = sumdps(STR, CRIT, DTR, SKS, WEP[0], WEP[1])
    strinc = sumdps(STR+1, CRIT, DTR, SKS, WEP[0], WEP[1])-base
    critinc = sumdps(STR, CRIT+1, DTR, SKS, WEP[0], WEP[1])-base
    detinc = sumdps(STR, CRIT, DTR+1, SKS, WEP[0], WEP[1])-base
    ssinc = sumdps(STR, CRIT, DTR, SKS+1, WEP[0], WEP[1])-base
    wdinc = sumdps(STR, CRIT, DTR, SKS, WEP[0]+1, WEP[1])-base
    return [strinc/strinc, 0, critinc/strinc, detinc/strinc, ssinc/strinc, wdinc/strinc]

def calc_value(STR, ACC, CRIT, DTR, SKS, WEP):
    weights = calc_weights(STR, ACC, CRIT, DTR, SKS, WEP)
    value = STR*weights[0] + ACC*weights[1] + CRIT*weights[2] + DTR*weights[3] + SKS*weights[4] + WEP[0]*weights[5]
    return value

def calc_staticvalue(STR, ACC, CRIT, DTR, SKS, WEP, weights):
    value = STR*weights[0] + ACC*weights[1] + CRIT*weights[2] + DTR*weights[3] + SKS*weights[4] + WEP[0]*weights[5]
    return value

def calc_dps(STR, ACC, CRIT, DTR, SKS, WEP):
    SKS = SKS - 341
    base = sumdps(STR, CRIT, DTR, SKS, WEP[0], WEP[1])
    return base

def bardrotation(CRIT, SS):
    # assumes constant rotation of SS VB WB HS HS HS HS HS, assumes auto crit
    # on ss since you had 5 chances to proc it, iunno how i feel about this but
    # im just reusing the existing model used to calculate all stat weights for
    # bard to date
    stupid = 1.2
    critrate = (CRIT*0.0697-18.437)/100 + 0.1*15/60 + .1 #crit chance + ss + ir
    critmodifier = 1 + 0.5*critrate
    delay = 2.5-0.01*SS/10.5
    blprocrate = .5 # 50% chance that you get a proc on crit from dot

    dropdotrotationpotency = (140*1.5 + (310+330+150*5)*critmodifier)*stupid # this is the dot dropping rotation
    dropdotduration = 8*delay
    dotdroptime = (dropdotduration-18)*2 # each dot is off the target for duration - 18 seconds, theres two dots which is why its *2

    constantdotpotency = (140*1.5 + (60+100+150*4+delay*7/3*80)*critmodifier)*stupid
    constantdotduration = 7*delay

    ogcdpps = (350/60 + 50/30 + 80/30)*critmodifier*stupid
    dropdotrotationpps = dropdotrotationpotency/dropdotduration
    constantdotrotationpps = constantdotpotency/constantdotduration
    rotationpps = max(dropdotrotationpps, constantdotrotationpps)
    if dropdotrotationpps > constantdotrotationpps:
        print "omfg you're actually supposed to change ur rotation with this much SS"


    # que the complex bloodletter math, heres the old version
    # BLFactor = ((1-(1-(critrate+0.1))*(1-(critrate+0.1)))/2)/3*150 * (1 + 0.5*(critrate+0.1))*stupid*1.08
    # trying my own version of bloodletter value, where its the chance of a
    # proc on each dot tick / 3 plus the chance of getting zero procs for 15
    # seconds. tested and it gives slightly higher numbers than the existing
    # model, this is likely because it accounts for natural bloodletters and as
    # far as i can tell the other one only includes procs, the 1.08 modifier
    # might be a super lazy attempt to scale it up to account for natural
    # bloodletters, i dont know. turns out he does account for natural
    # bloodletters (he calls them hard wait) but his are static chance of
    # happening when in reality it scales with crit

    # chance of getting a double crit proc + 2*the chance of getting a single
    # critproc (can crit vb and not wb or wb and not vb)
    BLprocchance = (critrate*blprocrate)**2 + 2*(critrate*blprocrate*(1-(critrate*blprocrate))) # 2dot proc chance
    onedotBLPC = (critrate*blprocrate)
    BLPotency = 150

    # pps from procs + pps of natural bloodletters the stuff on natural
    # bloodletters could be working on improper assumptions and I'd love
    # someone whos better than me at statistics to double check it, its
    # currently assumed that the chance of going 15 seconds without a
    # bloodletter proc * the potency of 1 bloodletter / 15 seconds = the
    # potency per second you're going to get over the entire fight from natural
    # bloodletters
    BLFactor = (BLprocchance*BLPotency/3 + ((1-BLprocchance)**5)*BLPotency/15)*critmodifier*stupid #to lazy to modify this to account for slightly lower bl chance in dot dropping rotation, requires almost 500 skillspeed to make it worth using an extra heavy shot and even then you only drop each dot for ~.5 seconds
    return BLFactor + rotationpps + ogcdpps


def main():
    dreadbow = [52, 3.2]
    augmentedironworksbow = [51, 3.04]
    yoichibow = [50, 3.04]
    highallaganbow = [48, 3.36]

    bis24 = calc_dps(645, 547, 647, 349, 350, dreadbow) # no i110 accessory true bis
    fouraccbis = calc_dps(626, 539, 694, 369, 395, dreadbow) # true bis
    curgear = calc_dps(622, 550, 605, 373, 401, augmentedironworksbow)
    truebis = calc_dps(621, 536, 710, 360, 432, dreadbow)

    chestremeldbelt = calc_dps(624, 543, 610, 353, 434, augmentedironworksbow)
    beltbootsdemonchest = calc_dps(616, 535, 614, 374, 429, augmentedironworksbow)
    nossbis = calc_dps(630, 536, 705, 351, 341, dreadbow)

    ariyalabis = calc_staticvalue(663, 535, 558, 359, 370, [58, 2.88], drgweights)
    maskonly = calc_staticvalue(656, 537, 527, 406, 365, [58, 2.88], drgweights)
    maskbelt = calc_staticvalue(651, 537, 567, 379, 388, [58, 2.88], drgweights)

    wodcrafted = calc_staticvalue(616, 537, 638, 369, 401, augmentedironworksbow, bardweights)
    nonwod = calc_staticvalue(622, 535, 607, 368, 423, augmentedironworksbow, bardweights)
    dreadpantswod = calc_staticvalue(622, 544, 654, 347, 414, augmentedironworksbow, bardweights)

    print nossbis, truebis, curgear

if __name__ == "__main__":
    main()
