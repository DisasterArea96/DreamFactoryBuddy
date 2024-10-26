import math
import BattleFactoryBuddy.StaticMoveDataHandler as StaticMoveDataHandler


# A class representing a single Pokemon set i.e. a line in the spreadsheet.
class Set:
    evlist = ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]

    def __init__(self, attrList):
        self.types = attrList[0].replace("\xef\xbb\xbf", "").strip().split(" ")
        self.moves = attrList[1]
        self.speciesName = attrList[2]
        # The human readable ID of the set e.g. "Skarmory-4"
        self.id = self.speciesName + "-" + attrList[3]
        # The set number within the species e.g. "4" for "Skarmory-4"
        self.idno = int(attrList[3]) if attrList[3] != "X" else 10
        # The unique set number across all factory sets e.g. 392 for "Skarmory-4"
        self.uid = attrList[14]
        self.nature = attrList[4]

        # Rather than escaping "King's Rock" we just drop the apostrophe for ease.
        self.item = attrList[5].replace("'", "")
        self.moveList = attrList[6:10]
        self.roundInfo = attrList[10]
        self.abilities = attrList[11]

        # Handle EVs
        tempevs = attrList[12].split("/")

        # Store off a friendly representation. Spin through and add the names for the stats that have EVs.
        i = 0
        self.evs = ""
        while i < len(Set.evlist):
            if int(tempevs[i]) > 0:
                self.evs += Set.evlist[i] + ": " + tempevs[i] + ", "
            i += 1
        self.evs = self.evs[:-2]

        # Store off the raw info for speed calculations. You can't simply scale between OL and L50 or IVs so
        # need this intel.
        self.basespeed = int(attrList[13])
        self.speednaturemulti = 1
        if self.nature in ("Timid", "Hasty", "Jolly", "Naive"):
            self.speednaturemulti = float(1.1)
        elif self.nature in ("Relaxed", "Sassy", "Quiet", "Brave"):
            self.speednaturemulti = float(0.9)
        self.speedevs = float(attrList[12].split("/")[-1])

    # Returns the speed of the mon given the round and battle the mon is in.
    def calcspeed(self, inputdict):
        level = int(inputdict["Level"])
        calced_ivs = int(inputdict["Battle"]) + ((int(inputdict["Round"]) - 1) * 4)
        ivs = min(calced_ivs, 31)
        return self.calcspeedraw(level, ivs)

    # Returns the speed value given the exact level and IVs.
    def calcspeedraw(self, level, ivs):
        return math.floor(
            (
                math.floor(
                    ((2 * self.basespeed + ivs + self.speedevs / 4) * level) / 100
                )
                + 5
            )
            * self.speednaturemulti
        )

    # Returns a boolean based on whether these two Sets could be in the same opposing team, checking item clause and
    # species clause. Used when generating teams.
    def compatibilitycheck(self, otherpkmn):
        if self.item == otherpkmn.item and self.item != "(no item)":
            return False
        if self.speciesName == otherpkmn.speciesName:
            return False
        if self.roundInfo == "A":
            if otherpkmn.roundInfo not in ["A"]:
                return False
        elif self.roundInfo == "B":
            if otherpkmn.roundInfo not in ["B","C"]:
                return False
        elif self.roundInfo == "C":
            if otherpkmn.roundInfo not in ["B","C","D"]:
                return False
        elif self.roundInfo == "D":
            if otherpkmn.roundInfo not in ["C","D","E","F"]:
                return False
        elif self.roundInfo in ("E","F"):
            if otherpkmn.roundInfo not in ["D","E","F"]:
                return False
        return True

    def getSpeciesName(self):
        return self.speciesName

    def getTypes(self):
        return self.types

    def getAbilities(self):
        return self.abilities

    def getuid(self):
        return self.uid

    # Returns a tuple used to display this set in the "found sets" table.
    def getTableRow(self, level, ivs, providePhrase, probability=0):
        if providePhrase:
            col2entry = self.moves
        else:
            col2entry = "{:.2f}%".format(probability)
        return (self.abilities,
            self.id,
            col2entry,
            self.item,
            self.moveList[0],
            self.moveList[1],
            self.moveList[2],
            self.moveList[3],
            self.nature,
            self.evs,
            self.calcspeedraw(level, ivs),
        )

    # Returns a string representation of this set to use in tooltips.
    def getTooltipInfo(self, probability):
        probabilitystr = "{:.2f}%".format(probability)
        return (
            self.id
            + " - "
            + probabilitystr
            + " | "
            + self.item
            + " | "
            + ", ".join(self.moveList)
        )

    # get speed for switching calculation
    def getSwitchSpeed(self, inputdict):
            return (self.calcspeed(inputdict),0,0)
