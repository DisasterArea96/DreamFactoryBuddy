import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler
import BattleFactoryBuddy.Team as Team

# Script to generate all static data (teams and speed tiers) and save them off in CSV files. This allows us to precompute all available teams
# once and not have to do it per query (which would be prohibitively slow). These files are also large so aren't checked in
# and need to be generated per-checkout or if the underlying mon data changes.

# Spin through all combinations of 3 mons. For each combination see if they're a valid team. If they are, work out which phrase they go with.
# Once we've done that then write them into csvs using their uids for brevity.
def generateTeamList():
    print("Starting generating team lists")
    setList = StaticDataHandler.StaticDataHandler.getSetList()
    maxpkmn = len(setList)
    validcombocount=0
    # Initialise looking at sets 1, 2 and 3 and work from there.
    a = 0
    b = 1
    c = 2
    combodictcount= {}
    while a < maxpkmn:
        setA = setList[a]
        while (b < maxpkmn):
            setB = setList[b]
            if (setA.compatibilitycheck(setB)):
                while (c < maxpkmn):
                    setC = setList[c]                
                    if((setA.compatibilitycheck(setC))):
                        if((setB.compatibilitycheck(setC))):                                
                            validcombocount +=1
                            team = Team.Team(setA,setB,setC)                            
                            type = team.type                                
                            style = team.style                            
                            if type in combodictcount:
                                if style in combodictcount[type]:
                                    combodictcount[type][style].append(team.shortStr())
                                else:
                                    combodictcount[type][style] = [team.shortStr()]
                            else:
                                combodictcount[type] = {}
                                combodictcount[type][style] = [team.shortStr()]                                                    
                    setC=None
                    c+=1
            setB=None
            setC=None
            b+=1
            c=b+1
        print("Done with all " + setA.id + " teams!")
        setA = None
        setB = None
        setC = None
        # Reinitialise with the next 3 sets.
        a+=1
        b=a+1
        c=a+2

    # Write out the CSVs.
    print("Created " + str(validcombocount) + " teams! Start writing them in sets")
    for a in combodictcount:
        for b in combodictcount[a]:
            with open ("./BattleFactoryBuddy/Data/"+str(a) + "-" + str(b) + ".csv","w") as o:
                for teamStr in combodictcount[a][b]:
                    o.write(teamStr + "\n")
                print("Written to ../Data/"+str(a) + "-" + str(b) + ".csv")

# Calculate the speed for all possible opposing mons. This is all sets in both and l50 and OL and 3IV, 6IV, 15IV, 31IV.
# How pokemon stats works means that some sets swap their order depending on the level and IV tier. We don't attempt to
# address that here in the ordering and it is instead handled at query time.
def generateSpeedList():
    print("Creating Speed Tiers")
    setList = StaticDataHandler.StaticDataHandler.getSetList()
    # Use 31IV open level as the master. That's least likely to have ties.
    speeddict = {}
    for set in setList:
        speed = set.calcspeedinternal(50,3)
        if speed not in speeddict:
            speeddict[speed] = []
        speeddict[speed].append(set)
    sortedspeeds = list(speeddict.keys())
    sortedspeeds.sort(reverse=True)    

    with open("./BattleFactoryBuddy/Data/Pokemonspeedtiers.csv","w") as r:
        r.write("Pokemon,round,l50_3,l50_6,l50_15,l50_31,l100_3,l100_6,l100_15,l100_31,quickclaw\n")
        for speed in sortedspeeds:
            for set in speeddict[speed]:
                r.write(",".join([set.id,str(set.roundInfo),str(set.calcspeedinternal(50,3)),str(set.calcspeedinternal(50,6)),str(set.calcspeedinternal(50,15)),str(set.calcspeedinternal(50,31)),str(set.calcspeedinternal(100,3)),str(set.calcspeedinternal(100,6)),str(set.calcspeedinternal(100,15)),str(set.calcspeedinternal(100,31)),str(set.item=="Quick Claw")+ "\n"]))
    print("Done creating speed tiers!")

# A utility function for checking the data on set moves and their phrases is consistent.
# As an example, the base spreadsheet for factory had Registeel-3 as 0 0 4 4 whereas Amnesia
# meant it should have been 0 1 4 4, this catches those issues (especially useful if you've edited the sets for some reason).
def validateSetInfo():
    setList = StaticDataHandler.StaticDataHandler.getSetList()
    movedict = {}
    typesdict = {}
    for set in setList:
        i = 0
        while i < 4:
            move = set.moveList[i]
            cat = set.moves.split(" ")[i]
            if move not in movedict:
                movedict[move] = cat
            else:
                if movedict[move] != cat:
                    print("Mistmatch on %s, found %s saved as %s. \nFix allpkmn.csv and rerun."%(move,cat,movedict[move]))
                    exit()
            i += 1
        if set.speciesName not in typesdict:            
            typesdict[set.speciesName] = sorted(set.types)
        elif typesdict[set.speciesName] != sorted(set.types):
            print("Type mismatch on %s, saved off as %s and found as %s. \nFix allpkmn.csv and rerun."%(set.speciesName,typesdict[set.speciesName],set.types))
            exit()


# UNUSED
# ALTSETS - provide an updated battle_moves.h in this directory if you need to update the move data. This list is small enough
# and distinct enough from the source data that it's just included in the repo for standard factory usage. You'll need
# to uncomment the function call below if you want it to run.
def generateMoveList():
    try:
        with open("./BattleFactoryBuddy/InputData/battle_moves.h") as r:
            with open(".BattleFactoryBuddy/InputData/moves.csv","w") as w:
                currmove = []
                for line in r:
                    if "[MOVE_" in line:                
                        if currmove != []:
                            w.write(",".join(currmove) + "\n")                
                        currmove = [line.split("MOVE_")[1].split("]")[0]]
                    elif "=" in line and currmove != []:    
                        if ".type" in line:
                            currmove.append(line.split("TYPE_")[1].split(",")[0])

                        else:
                            currmove.append(line.split("=")[1].split(",")[0])
                    else:
                        continue
                w.write(",".join(currmove) + "\n")
    except:
        print("Using standard move data - not generating.")

# UNUSED
# A silly little utility function to count the instances of each move, not run by default.
def generateMoveCounts():
    movedict = {}
    setList = StaticDataHandler.StaticDataHandler.getSetList()
    for set in setList:
        for move in set.moveList:
            if move not in movedict:
                movedict[move] = 1
            else:
                movedict[move] += 1
    with open("./BattleFactoryBuddy/Data/movecounts.csv","w") as o:
        for move in movedict:
            outstr = move + "," + str(movedict[move]) + "\n"
            o.write(outstr)

# UNUSED
# ALTSETS - if you've changed the type chart then you can use this autogenerate a bunch of code used to work out type effectiveness.
def generateTypeEffectivenessCode():
    with open("./types.csv") as r:
        currenttype = None
        prefill = "\tif \"{}\" in targettypes:\n\t\tretval = int(retval*{})"
        for line in r:
            split = line.strip().split(" ")        
            if split[0] != currenttype:
                print("elif intype == \"{}\":".format(split[0]))
                currenttype = split[0]

            print(prefill.format(split[1],split[2]))

if __name__ == "__main__":
    print("This will take a while (maybe 5-10 mins?), it gets faster as it goes though!")
    validateSetInfo()
    generateSpeedList()    
    generateTeamList()
    # Various utility functions that aren't needed to be run in most cases.
    # generateMoveList()
    # generateMoveCounts()
    # generateTypeEffectivenessCode()