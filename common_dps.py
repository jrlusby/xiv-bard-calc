#! /usr/bin/python2
import random
import math

def abilitydamage(WD, STR, DTR, potency, BUFFS):
    return ((potency/100.0)*(WD/25.0+1)*(STR/9.0)*(DTR/7290.0+1)*BUFFS)-1


def autoattackdamage(WD, STR, DTR, weapon_delay):
    BUFFS = 1.0
    return ((WD/3.0*weapon_delay/34.0+1)*(STR/6.8)*(DTR/6795.0+1)*BUFFS)-1

def crit_rate(CRIT):
    return ((CRIT-354.0)/(858.0*5.0))+0.05

def crit_damage(CRIT):
    return ((CRIT-354.0)/(858.0*5.0))+1.45

def gcd_timer(SS):
    # print 2.50256-(0.01*(SS-354)/26.5)
    # print 2.50245-((SS-354)*0.0003776)
    # print 2.51-((SS-334)/2641.0)
    # return 2.50256-(0.01*(SS-354)/26.5)
    # return 2.50245-((SS-354)*0.0003776)
    return 2.51-((SS-334)/2641)

def dot_modifier(SS):
    # return (1+(SS-354)*0.000138)
    return ((SS-354)/7722.0+1)

def main():
    print "hi"
    print gcd_timer(354)
    print dot_modifier(354)
    print gcd_timer(654)
    print dot_modifier(654)
    print abilitydamage(68, 1.18*1078, 293, 100)/abilitydamage(68, 1.03*1078, 293, 100)
    # print autoattackdamage(68, 1078, 293, 3.2)
    # CRIT = 934
    # critrate = (((CRIT-354)*0.0232558)+4.9511233)/100
    # critrate = critrate+.1 # straight shot
    # # critrate = critrate+(.1*1.0/4)
    # critrate = critrate+.1
    # critdamage = ((CRIT-354)*0.000232558)+1.4484746
    # critmodifier = 1 + (critdamage-1)*critrate
    # print critrate, critdamage, critmodifier
    # print (15*blpersec(critrate)*150 + 80*5 + 100 + 5*150)*critmodifier
    # print abilitydamage(68, 1.18*1078, 293, 100)/abilitydamage(68, 1.03*1078, 293, 100)



    # newbardweights = [1.0, 0, 0.311, 0.310, 0.110, 9.807]

    # dreadbow = [52, 3.2]
    # augmentedironworksbow = [51, 3.04]
    # yoichibow = [50, 3.04]
    # highallaganbow = [48, 3.36]
    # diamondbow = [48, 2.88]
    # zetabow = [52, 3.04]
    # hivebow = [65, 3.04]
    # nobow = [0, 0]

    # # 1078.     595.     764.     457.     736.
    # weights = calc_weights(1078, 595, 764, 457, 736, hivebow)
    # print weights

if __name__ == "__main__":
    main()
