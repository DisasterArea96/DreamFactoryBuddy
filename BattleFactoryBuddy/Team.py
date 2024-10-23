from collections import Counter
import math

# A class representing a team of 3 sets. This is used to work out what phrase / style / round a team could be in. As 
# such it's not used at calculation time as that's all precomputed to try and speed up the queries. During calculation
# we just use a flat list of uids of sets to save on memory usage rather than wrapping in an object.
class Team:
    def __init__(self, set1, set2, set3):
        self.sets = [set1, set2, set3]
        self.style = "99"
        self.type = ""

        self.initCalculateStyle()
        self.initCalculateType()
        self.initCalculateRound()

    # Work out which style this team has. Called during init.
    # ALTSETS - Edits required if your calculation of scientist hint for styles is different.
    def initCalculateStyle(self):
        stylepoints = ""
        for set in self.sets:
            stylepoints += set.moves
        
        counter = Counter(stylepoints)
        t1 = 1 if (counter["1"] > 1) else 0
        t2 = 1 if (counter["2"] > 2) else 0
        t3 = 1 if (counter["3"] > 2) else 0
        t4 = 1 if (counter["4"] > 2) else 0
        t5 = 1 if (counter["5"] > 1) else 0
        t6 = 1 if (counter["6"] > 1) else 0
        t7 = 1 if (counter["7"] > 2) else 0

        if (t1 + t2 + t3 + t4 + t5 + t6 + t7) > 2:
            self.style = 8
        elif t7 == 1:
            self.style = 7
        elif t6 == 1:
            self.style = 6
        elif t5 == 1:
            self.style = 5
        elif t4 == 1:
            self.style = 4
        elif t3 == 1:
            self.style = 3
        elif t2 == 1:
            self.style = 2
        elif t1 == 1:
            self.style = 1
        else:
            self.style = 0

    # Calculate the type covered by the team.
    # ALTSETS - Edits required if your calculation of scientist hint for types is different.
    def initCalculateType(self):
        
        types = []
        for set in self.sets:
            types += set.types
        maxcount = 0

        for a in types:            
            if a == "":
                continue
            number = types.count(a)
            if number > maxcount:
                maxcount = number
                self.type = a
            elif number == maxcount:
                if a != self.type:
                    self.type = "None"

    # Work out which "round" this team can appear in. This isn't 1-1 with rounds in the game but more like buckets.

    # 1 = l50 round 4 / OL round 1
    # 2 = l50 round 5 / OL round 2
    # 3 = l50 round 6 / OL round 3
    # 4 = l50 round 7 / OL round 4
    # 5 = l50 round 8+
    # 6 = OL round 5+

    # A = l50 round 1-3
    # B = l50 round 4-6
    # C = l50 round 4+ / OL round 1-3
    # D = l50 round 7+ / OL (all)
    # E = OL round 4+
    # F = OL round 7+

    # ALTSETS - Edits required if your sets maps to rounds in different ways.
    def initCalculateRound(self):
        roundmarkers = []
        for monset in self.sets:
            roundmarkers.append(monset.roundInfo)        
        
        # If we have an OL r5+ mon (e.g. Dragonite-1) then we know the whole team can only appear in bucket 6.
        if "6" in roundmarkers:
            self.round = "6"
        # Similarly, if there's another legendary then we're in bucket 5.
        elif "5" in roundmarkers:
            self.round = "5"
        # Otherwise, if all the round markers match (e.g. Zam-3, Lanturn-3, Gengar-3) then we put it in the bucket matching their round markers.
        elif len(set(roundmarkers)) == 1:
            self.round = roundmarkers[0]
        # Otherwise it's a mix of sets (e.g Whiscash-1, Armaldo-2, Manectric-3) and we're in bucket 5 again.
        else:
            self.round = "5"

    # Return a human readable list of the sets in the team.
    def readableStr(self):
        return (
            self.sets[0].id
            + ","
            + self.sets[1].id
            + ","
            + self.sets[2].id
            + ","
            + self.round
        )
    
    # Return the uids of the Sets in the team.
    def shortStr(self):
        return (
            str(self.sets[0].uid)
            + ","
            + str(self.sets[1].uid)
            + ","
            + str(self.sets[2].uid)
            + ","
            + self.round
        )

    # Used to return the type and phrase for a team. Used for team phrase analysis.
    def phraseoutput(self):
        typstr = ""
        phrasestr = "The favourite battle style "
        if self.type == "None":
            typstr = (
                "The Trainer appears to have no clear favourites when it comes to type."
            )
        else:
            typstr = (
                "The Trainer is apparently skilled in the handling of the %s type."
                % (self.type)
            )
        if self.style == 0:
            phrasestr += "appears to be free-spirited and unrestrained."
        elif self.style == 1:
            phrasestr += "appears to be one based on total preparation."
        elif self.style == 2:
            phrasestr += "appears to be slow and steady."
        elif self.style == 3:
            phrasestr += "appears to be one of endurance."
        elif self.style == 4:
            phrasestr += "appears to be high risk, high return."
        elif self.style == 5:
            phrasestr += "appears to be weakening the foe to start."
        elif self.style == 6:
            phrasestr += "appears to be impossible to predict."
        elif self.style == 7:
            phrasestr += "appears to depend on the battle's flow."
        elif self.style == 8:
            phrasestr += "appears to be flexibly adaptable to the situation."
        return (typstr, phrasestr)
