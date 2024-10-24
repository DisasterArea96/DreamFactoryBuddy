import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler

# This class handles queries about speed tiers via a static method. It's not at all nice but as this is some
# side functionality on the Buddy, and relatively straightforward, I'm not attempting to tidy it up for
# first release. There's much more and better to be done here by someone at some point.

class SpeedQueryHandler:
    
    def calcSpeedOutputs(inputdict):
        level = int(inputdict["Level"])
        round = int(inputdict["Round"])    
        ivs = int(inputdict["IVs"])    
        
        if inputdict["yourspeed"] == '':
            inputdict["outputcol1"] = "<font size=\"20\"><b>Please input a speed</b></font><br>"
            return(inputdict)     

<<<<<<< HEAD
        # Work out which sets are allowable in this round.
        allowedRoundSets = []
        if level == 50:
            if round < 4:
                inputdict["outputcol1"] = "<font size=\"20\"><b>Not supported for Level 50 rounds 1-3.</b></font><br>"
                return(inputdict)
            elif round < 8:
                allowedRoundSets.append(round - 3)
            else:
                allowedRoundSets=[1,2,3,4,5]
        elif round < 5:
            allowedRoundSets.append(round)
        else:
            allowedRoundSets = [1,2,3,4,5,6]        

        # Calculate the speeds for all other allowable sets and sort them into the relevant buckets.
        refspeed = int(inputdict["yourspeed"])
        fasterList = []
        tiedList = []
        slowerQCList = []
        slowerList = []

        for set in StaticDataHandler.StaticDataHandler.getSetList():
            if int(set.roundInfo) not in allowedRoundSets:
                continue
            setSpeed = set.calcspeedraw(level,ivs)
            if setSpeed > refspeed:
                fasterList.append((set.id, int(set.getuid()), setSpeed))
            elif setSpeed == refspeed:
                tiedList.append((set.id, int(set.getuid()), setSpeed))
            elif set.item == "Quick Claw":
                slowerQCList.append((set.id, int(set.getuid()), setSpeed))
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
        inputdict["outputcol3"] = "<h3>Slower with Quick Claw: {:.2f}%</h3></br>".format(float(100*len(slowerQCList))/total) + slowerQcHtml
        inputdict["outputcol4"] = "<h3>Slower: {:.2f}%</h3></br>".format(float(100*len(slowerList))/total) + slowerHtml
        return inputdict
        
            

=======
        refspeed = int(inputdict["yourspeed"])

        column = 2
        if level == 100:
            column += 4
        if IVs == 6:
            column +=1
        elif IVs == 15:
            column +=2
        elif IVs == 31:
            column +=3
        
        sets = []
        if level == "50" and int(round) < 4:
            sets=[1]
        elif level == "50" and round in [4,5,6]:
            sets=[2,3]
        elif (level == "50" and int(round) > 6) or (level == "100" and int(round) < 4):
            sets=[3,4,5]
        elif level == "100" and round in [4,5,6]:
            sets=[5,6]
        elif level == "100" and int(round) > 6:
            sets=[5,6,7]
        
        faster = ""
        fastercount = 0
        tied = ""
        tiedcount = 0
        slowerwithqc = ""
        slowerwithqccount = 0
        slower = ""    
        slowercount = 0    
        skip = True
        with open("./BattleFactoryBuddy/Data/Pokemonspeedtiers.csv") as r:
            for line in r:
                splits = line.split(",")
                if skip:
                    skip = False
                    continue
                if int(splits[1]) not in sets:
                    continue
                if int(splits[column]) > refspeed:
                    faster += splits[0] + ": " + splits[column] + "<br>"
                    fastercount += 1
                elif int(splits[column]) == refspeed:
                    tied += splits[0] + ": " + splits[column] + "<br>"
                    tiedcount += 1
                elif (int(splits[column]) < refspeed) and splits[-1].strip() == "True":
                    slowerwithqc += splits[0] + ": " + splits[column] + "<br>"
                    slowerwithqccount += 1
                else:                    
                    slower += splits[0] + ": " + splits[column] + "<br>"
                    slowercount += 1
        total = fastercount+tiedcount+slowerwithqccount+slowercount
        inputdict["outputcol1"] = "<h3>Faster: {:.2f}%</h3></br>".format(float(100*fastercount)/total) + faster
        inputdict["outputcol2"] = "<h3>Tied: {:.2f}%</h3></br>".format(float(100*tiedcount)/total) + tied
        inputdict["outputcol3"] = "<h3>Slower with Quick Claw: {:.2f}%</h3></br>".format(float(100*slowerwithqccount)/total) + slowerwithqc
        inputdict["outputcol4"] = "<h3>Slower: {:.2f}%</h3></br>".format(float(100*slowercount)/total) + slower

        return(inputdict)
>>>>>>> 040db62 (Updated speed query handler to handle the new set buckets)
