class GearItem:
    def __init__(self, AP, ACC, CRIT, DET, SS, VIT, WD, WDelay, name, meldslots, geartype, itemlevel, isunique, itemid):
        self.stats = [AP, ACC, CRIT, DET, SS, VIT, WD, WDelay]
        self.name = name
        self.meldslots = meldslots
        self.geartype = geartype
        self.itemlevel = itemlevel
        self.isunique = isunique
        self.itemid = itemid

    # def stats(self):
    #     return [self.AP, self.ACC, self.CRIT, self.DET, self.SS, self.VIT, self.WD, self.WDelay]

    def __str__(self):
        return self.name + str(self.stats)

    # return [[stats["Dexterity"], stats["Accuracy"], stats["Critical Hit Rate"], stats["Determination"], stats["Skill Speed"], stats["Vitality"], WEAPONDAMAGE, WEAPONDELAY], detailedItem["name"]], [meldslots, geartype, itemlevel, isunique, itemid]
