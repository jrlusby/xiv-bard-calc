class JobClass:
    def __init__(self, weights, food, jobclassval, attributeval):
        self.weights = weights
        self.food = food
        self.jobclassval = jobclassval
        self.attributeval = attributeval

    def damageType(self):
        if self.attributeval <= 3:
            return "damage"
        else:
            return "magic_damage"

    def SSName(self):
        if self.attributeval <= 3:
            return "Skill Speed"
        else:
            return "Spell Speed"

    def AttributeName(self):
        if self.attributeval == 1:
            return "Strength"
        if self.attributeval == 2:
            return "Dexterity"
        if self.attributeval == 3:
            return "Strength"
        if self.attributeval == 4:
            return "Intelligence"
        if self.attributeval == 5:
            return "Mind"
        if self.attributeval == 6:
            return "Piety"

    def gearQuery(self, minlevel):
        return "https://api.xivdb.com/search?classjobs={}&one=items&level_item%7Cgt={}&attributes={}%7Cgt%7C1%7C0&language=en".format(self.jobclassval, minlevel, self.attributeval)
