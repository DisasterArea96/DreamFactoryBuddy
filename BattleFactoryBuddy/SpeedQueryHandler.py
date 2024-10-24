# This class handles queries about speed tiers via a static method. It's not at all nice but as this is some
# side functionality on the Buddy, and relatively straightforward, I'm not attempting to tidy it up for
# first release. There's much more and better to be done here by someone at some point.

class SpeedQueryHandler:
    
    @staticmethod
    def getspeedoutputs(inputdict):
        level = int(inputdict["Level"])
        round = int(inputdict["Round"])
        IVs = int(inputdict["IVs"])
        
        if inputdict["yourspeed"] == '':
            inputdict["outputcol1"] = "<font size=\"20\"><b>Please input a speed</b></font><br>"
            return(inputdict)

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
