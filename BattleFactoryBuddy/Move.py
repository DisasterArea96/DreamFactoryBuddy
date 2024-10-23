class Move:
    def __init__(self, attrlist):
        self.name = attrlist[0].replace("_", " ").replace(" ", "").lower()
        self.type = attrlist[3]
        self.status = attrlist[2] == "0"
        self.power = attrlist[2]
        self.pp = attrlist[5]
        self.standarddamagemove = None

    # Several moves are handled differently during switch-in logic calculation.
    # The docs refer to these as not "Normal Damaging moves" which this covers.
    def isNormalDamaging(self):
        if self.standarddamagemove != None:
            pass
        elif self.name in [
            "fissure",
            "horndrill",
            "guillotine",
            "sheercold",
            "flail",
            "frustration",
            "return",
            "lowkick",
            "magnitude",
            "present",
            "reversal",
            "counter",
            "mirrorcoat",
            "nightshade",
            "seismictoss",
        ]:
            self.standarddamagemove = False
        else:
            self.standarddamagemove = True
        return self.standarddamagemove

    def getName(self):
        return self.name

    def getType(self):
        return self.type
