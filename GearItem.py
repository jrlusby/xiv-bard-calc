
class GearItem:
    categories = ["Arm", "Head", "Body", "Hands", "Waist", "Legs", "Feet", "Necklace", "Earrings", "Bracelets", "Ring"]
    def __init__(self, AP, ACC, CRIT, DET, SS, VIT, WD, WDelay, name, meldslots, geartype, itemlevel, isunique, itemid, attribute):
        self.stats = [AP, ACC, CRIT, DET, SS, VIT, WD, WDelay]
        self.name = name
        self.meldslots = meldslots
        self.geartype = geartype
        self.itemlevel = itemlevel
        self.isunique = isunique
        self.itemid = itemid
        self.attribute = attribute

    # def stats(self):
    #     return [self.AP, self.ACC, self.CRIT, self.DET, self.SS, self.VIT, self.WD, self.WDelay]

    def __str__(self):
        return self.name + str(self.stats)

    def isVitAccessory(self):
        print categories[-4:]
        return self.attribute == 3 and self.geartype in categories[-4:]


    # return [[stats["Dexterity"], stats["Accuracy"], stats["Critical Hit Rate"], stats["Determination"], stats["Skill Speed"], stats["Vitality"], WEAPONDAMAGE, WEAPONDELAY], detailedItem["name"]], [meldslots, geartype, itemlevel, isunique, itemid]
