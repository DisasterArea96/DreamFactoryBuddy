import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler

# This class handles queries about speed tiers via a static method. It's not at all nice but as this is some
# side functionality on the Buddy, and relatively straightforward, I'm not attempting to tidy it up for
# first release. There's much more and better to be done here by someone at some point.

class SpeedQueryHandler:
    
    def calcSpeedOutputs(inputdict):
        level = int(inputdict["Level"])
        round = int(inputdict["Round"])    
        input_ivs = int(inputdict["IVs"])
        ivs = min(input_ivs + ((round - 1) * 4),31)
        
        if inputdict["yourspeed"] == '':
            inputdict["outputcol1"] = "<font size=\"20\"><b>Please input a speed</b></font><br>"
            return(inputdict)     

        # Work out which sets are allowable in this round.
        allowedRoundSets = []
        if level == 50 and round < 4:
            allowedRoundSets=["A"]
        elif level == 50 and round in [4,5,6]:
            allowedRoundSets=["B","C"]
        elif (level == 50 and round > 6) or (level == 100 and round < 4):
            allowedRoundSets=["C","D"]
        elif level == 100 and round in [4,5,6]:
            allowedRoundSets=["D","E"]
        elif level == 100 and round > 6:
            allowedRoundSets=["D","E","F"]


        # Calculate the speeds for all other allowable sets and sort them into the relevant buckets.
        refspeed = int(inputdict["yourspeed"])
        fasterList = []
        tiedList = []
        slowerQCList = []
        slowerList = []

        for set in StaticDataHandler.StaticDataHandler.getSetList():
            if set.roundInfo not in allowedRoundSets:
                continue
            setSpeed = set.calcspeedraw(level,ivs)
            if setSpeed > refspeed:
                fasterList.append((set.id, int(set.getuid()), setSpeed))
            elif setSpeed == refspeed:
                tiedList.append((set.id, int(set.getuid()), setSpeed))
            else:
                slowerList.append((set.id, int(set.getuid()), setSpeed))
        
        # Sort lists so that the faster mons are higher and then the higher ID
        # mons within a tie are higher. As smaller number = higherid we have to take the 
        # ID off the speedscore.
        fasterList.sort(key=lambda tuple: tuple[2]*10000-tuple[1],reverse=True)        
        fasterHtml = ""
        for (id, unused, speed) in fasterList:
            fasterHtml += "<br>" + id + ": " + str(speed)

        tiedList.sort(key=lambda tuple: tuple[2]*10000-tuple[1],reverse=True)
        tiedHtml = ""
        for (id, unused, speed) in tiedList:
            tiedHtml += "<br>" + id + ": " + str(speed)

        slowerQCList.sort(key=lambda tuple: tuple[2]*10000-tuple[1],reverse=True)
        slowerQcHtml = ""
        for (id, unused, speed) in slowerQCList:
            slowerQcHtml += "<br>" + id + ": " + str(speed)

        slowerList.sort(key=lambda tuple: tuple[2]*10000-tuple[1],reverse=True)
        slowerHtml = ""
        for (id, unused, speed) in slowerList:
            slowerHtml += "<br>" + id + ": " + str(speed)

        # Output as HTML
        total = len(fasterList) + len(tiedList) + len(slowerQCList) + len(slowerList)

        inputdict["outputcol1"] = "<h3>Faster: {:.2f}%</h3></br>".format(float(100*len(fasterList))/total) + fasterHtml
        inputdict["outputcol2"] = "<h3>Tied: {:.2f}%</h3></br>".format(float(100*len(tiedList))/total) + tiedHtml
        inputdict["outputcol3"] = "<h3>Slower: {:.2f}%</h3></br>".format(float(100*len(slowerList))/total) + slowerHtml
        return inputdict
