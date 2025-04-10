import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler
import BattleFactoryBuddy.StaticTeamUtils as StaticTeamUtils
from pathlib import Path

class SetCalcHandler:
    def __init__(self):
        return

    def calculate(self, inputdict, results):
        if "HiRes" in inputdict and inputdict["Species1"] != None:
            return self.calcProcedural(inputdict,results)
        if inputdict["Battle"] == "11":
            return self.calculateNolandBattle(inputdict, results)
        else:
            return self.calculateStandardBattle(inputdict, results)

    def generateListOfDictsOfRequiredSets(self, inputdict,overrideSetTo3 = False):
        requiredListList = []
        idx = 1
        while idx <= 3:
            if inputdict["Species" + str(idx)] != "":
                moves = [
                    inputdict["Move1" + str(idx)],
                    inputdict["Move2" + str(idx)],
                    inputdict["Move3" + str(idx)],
                    inputdict["Move4" + str(idx)],
                ]
                while "" in moves:
                    moves.remove("")
                items = [inputdict["Item" + str(idx)]]
                while "" in items:
                    items.remove("")
                ids = inputdict["Set" + str(idx)].split(",")
                while "" in ids:
                    ids.remove("")
                requiredDict = {}
                for id in StaticDataHandler.StaticDataHandler.getSpeciesFromName(
                        inputdict["Species" + str(idx)]
                    ).filter(moves, items, ids if not overrideSetTo3 else ['3']):
                    requiredDict[id] = 1
                requiredListList.append(requiredDict)
            idx += 1
        return requiredListList

    def calculateStandardBattle(self, inputdict, results):
        # Get list of lists of required sets to be present in teams that are possible.
        # These are set IDs.
        requiredDictsList = self.generateListOfDictsOfRequiredSets(inputdict)

        # Create a dict of setIDs that aren't allowed. This is all the sets of
        # all species that are on the team or the last team (or draft)
        unallowedDict = {}
        for speciesName in (inputdict["Team1"],inputdict["Team2"],inputdict["Team3"],inputdict["LastOpp1"],inputdict["LastOpp2"],inputdict["LastOpp3"]):
            if speciesName == "":
                continue
            for setID in StaticDataHandler.StaticDataHandler.getIDsFromSpeciesName(speciesName):
                unallowedDict[setID] = 1

        # Create the list of team sets that are allowed, based on round and level.
        teamSetList = []
        level = inputdict["Level"]
        round = inputdict["Round"]

        # ALTSETS - if you have different rules on which teams are in which rounds then change it here.

        # 1 - All As
        # 2 - Has B
        # 3 - All Cs
        # 4 - CD
        # 5 - All Ds
        # 6 - DE
        # 7 - Has F

        # Then l50:
        # r1-4 = [1]
        # r4-6 = [2,3]
        # r7+ = [3,4,5]
        # OL:
        # r1-3 =[3,4,5]
        # r4-6=[5,6]
        # r7+ = [5,6,7]

        if level == "50" and int(round) < 4:
            teamSetList = ["1"]
        elif level == "50" and round in ["4","5","6"]:
            teamSetList = ["2","3"]
        elif (level == "50" and int(round) > 6) or (level == "100" and int(round) < 4):
            teamSetList = ["3","4","5"]
        elif level == "100" and round in ["4","5","6"]:
            teamSetList = ["5","6"]
        elif level == "100" and int(round) > 6:
            teamSetList = ["5","6","7"]

        # Calculate any required info up front about which calcs we need to do, so
        # we've got a simple bool to check in the big loop.
        switchlogic = False
        if (
            "switchin" in inputdict
            and inputdict["Species2"] != ""
            and inputdict["Species1"] != ""
        ):
            switchlogic = True

        # Take a deep breath and pull each possible team one at a time from the
        # StaticDataHandler's iterable method.
        for teamData in StaticDataHandler.StaticDataHandler.iterGetTeamList(
            inputdict["Type"], inputdict["Phrase"]
        ):
            # Check whether the round indicator on the team is matches the round we're in.
            team = teamData[0:3]
            roundData = teamData[3]
            if roundData not in teamSetList:
                continue

            # Check we've got one of each of the required mons
            if len(requiredDictsList) > 0:
                foundrequired = False
                for requiredDict in requiredDictsList:
                    foundrequired = False
                    for setId in requiredDict:
                        if setId in team:
                            foundrequired = True
                            break                    
                    if not foundrequired:
                        break
                # We can only leave the previous loop "happily" if we ended by find a suitable set match. Otherwise loop onto
                # the next team
                if not foundrequired:
                    continue

            # Check we don't have any of the mons we shouldn't have.
            foundDisallowed = False
            for setId in team:
                if setId in unallowedDict:
                    foundDisallowed = True
                    break
            if foundDisallowed:
                continue

            # Run switch logic.
            if switchlogic:
                # Get the switch scores for Species2 and Species3 (which may or may not have been defined).
                for setId in team:
                    speciesName = StaticDataHandler.StaticDataHandler.getSpeciesFromId(
                        setId
                    ).speciesName
                    if speciesName == inputdict["Species2"]:
                        species2Speed = StaticDataHandler.StaticDataHandler.getSetFromId(setId).getSwitchSpeed(inputdict)
                    elif speciesName != inputdict["Species1"]:
                        species3Speed = StaticDataHandler.StaticDataHandler.getSetFromId(setId).getSwitchSpeed(inputdict)

                if species2Speed > species3Speed:
                    results.addTeam(team, 2)
                elif species2Speed == species3Speed:
                    results.addTeam(team)

            # We've got a valid team and how many we want it to count for. Save that off in our results object.
            else:
                results.addTeam(team)
        return results

    # What to work out and display for Noland battles is quite tricky. We don't want to have to trawl
    # through too much stuff but there is value we can add by eliminating through item clause and doing
    # switch logic if its applicable.
    # NOTE: We don't get here if we don't have at least one species defined, that's handled in validation.
    def calculateNolandBattle(self, inputdict, results):
        switchin = False
        if (
            "switchin" in inputdict
            and inputdict["Species2"] != ""
            and inputdict["Species1"] != ""
        ):
            switchin = True

        # Get all the possible sets we've seen from Noland.
        requiredListList = self.generateListOfListsOfRequiredSets(inputdict, False)

        # If we've not got anything species specified then the query handler will have returned an error.

        # If we've only got one species defined then just add them all equally so people can filter them.
        if inputdict["Species1"] != "" and inputdict["Species2"] == "":
            resultNote = "Noland battle - not attempting to calculate mons in the back"
            results.addNote(resultNote)
            for requiredList in requiredListList:
                for set in requiredList:
                    results.addTeam([set, set, set])
        # If we've got two or three species then we can some switch-in and item logic.
        else:
            species1Ids = requiredListList[0]
            species2Ids = requiredListList[1]
            if (
                inputdict["Species1"] != ""
                and inputdict["Species2"] != ""
                and inputdict["Species3"] == ""
            ):
                species3Sets = StaticDataHandler.StaticDataHandler.getSetList()
            else:
                # We need to get all these sets to make the loop below work.
                species3Sets = []
                species3Ids = requiredListList[2]
                for id in species3Ids:
                    species3Sets.append(
                        StaticDataHandler.StaticDataHandler.getSetFromId(id)
                    )
            for s1Id in species1Ids:
                s1set = StaticDataHandler.StaticDataHandler.getSetFromId(s1Id)
                for s2Id in species2Ids:
                    s2set = StaticDataHandler.StaticDataHandler.getSetFromId(s2Id)
                    if s1set.compatibilitycheck(s2set):
                        # We don't have an easy way to get all IDs so this one just goes straight from sets.
                        for s3set in species3Sets:
                            if s1set.compatibilitycheck(
                                s3set
                            ) and s2set.compatibilitycheck(s3set):
                                if switchin:
                                    species2Speed = s2set.getSwitchSpeed(s2Id)
                                    species3Speed = s3set.getSwitchSpeed(s3set)

                                    if species3Speed < species2Speed:
                                        results.addTeam((s1Id, s2Id, s3set.uid), 2)
                                    if species3Speed == species2Speed:
                                        results.addTeam((s1Id, s2Id, s3set.uid))
                                else:
                                    results.addTeam((s1Id, s2Id, s3set.uid))
        return results
    
    def calcProcedural(self,inputdict,results):        
        validOptionsFirst = len(StaticDataHandler.StaticDataHandler.getSetList())    
        # CREATE RESULTS ARRAY
        resultArray = {}    
        resultArray["total"] = 0
        noland = inputdict["Battle"] == "11"

        # Allowed round markers
        checkLevel = int(inputdict["Level"])
        checkRound = int(inputdict["Round"])

        if checkLevel == 50 and checkRound < 4:
            markers = ["A"]
        elif checkLevel == 50 and checkRound in [4,5,6]:
            markers = ["B","C"]
        elif (checkLevel == 50 and checkRound > 6) or (checkLevel == 100 and checkRound < 4):
            markers = ["C","D"]
        elif checkLevel == 100 and checkRound in [4,5,6]:
            markers = ["D","E"]
        elif checkLevel == 100 and checkRound > 6:
            markers = ["D","E","F"]

        # SET UP LIST OF MONS VALID FOR THESE TEAMS
        blockedSpecies = [inputdict["Team1"],inputdict["Team2"],inputdict["Team3"],inputdict["LastOpp1"],inputdict["LastOpp2"],inputdict["LastOpp3"],inputdict["Species1"],inputdict["Species2"],inputdict["Species3"]]
        while "" in blockedSpecies:
            blockedSpecies.remove("")
        setList = []
        firstSetList = []

        # Populate list with filtered sets for any Species defined.
        idx = 1
        while idx <= 3:
            if inputdict["Species" + str(idx)] != "":
                moves = [
                    inputdict["Move1" + str(idx)],
                    inputdict["Move2" + str(idx)],
                    inputdict["Move3" + str(idx)],
                    inputdict["Move4" + str(idx)],
                ]
                while "" in moves:
                    moves.remove("")
                items = [inputdict["Item" + str(idx)]]
                while "" in items:
                    items.remove("")
                ids = inputdict["Set" + str(idx)].split(",")
                while "" in ids:
                    ids.remove("")
                for consideredSet in StaticDataHandler.StaticDataHandler.getSpeciesFromName(
                        inputdict["Species" + str(idx)]
                    ).filter(moves, items, ids, True):
                    if consideredSet.roundInfo in markers:
                        resultArray[consideredSet.id] = 0
                        if idx == 1:
                            firstSetList.append(consideredSet)
                        else:
                            setList.append(consideredSet)
            idx += 1

        # Prep the setList for any mon not defined
        for consideredSet in StaticDataHandler.StaticDataHandler.getSetList():
            if consideredSet.roundInfo not in markers:
                continue
            if consideredSet.speciesName in blockedSpecies:
                continue
            resultArray[consideredSet.id] = 0        
            setList.append(consideredSet)
        if firstSetList == []:
            firstSetList = setList
        validOptionsFirst = len(firstSetList)    

        # Prep switch logic
        switchlogic = False
        if (
            "switchin" in inputdict
            and inputdict["Species2"] != ""
            and inputdict["Species1"] != ""
        ):
            switchlogic = True

        # DO THE THING
        for setA in firstSetList:        
            secondmonlist = []                
            validOptionsSecond = 0
            for setB in setList:            
                if setA.compatibilitycheck_noroundcheck(setB):
                    validOptionsSecond += 1
                    secondmonlist.append(setB)            
            for setB in secondmonlist:                           
                thirdmonlist = []
                validOptionsThird = 0
                for setC in setList:
                    if setA.compatibilitycheck_noroundcheck(setC) and setB.compatibilitycheck_noroundcheck(setC):
                        validOptionsThird += 1
                        thirdmonlist.append(setC)                
                for setC in thirdmonlist:
                    # TEAM VALIDATION - cover species 2 and species 3 if they're here.
                    if inputdict["Species2"] != "" and setB.speciesName != inputdict["Species2"] and setC.speciesName != inputdict["Species2"]:
                        continue
                    if inputdict["Species3"] != "" and setB.speciesName != inputdict["Species3"] and setC.speciesName != inputdict["Species3"]:
                        continue
                    if not noland:
                        (teamType, teamStyle) = StaticTeamUtils.StaticTeamUtils.getTeamInfo(setA,setB,setC)                 
                        if teamType != inputdict["Type"] or str(teamStyle) != inputdict["Phrase"]:
                            continue

                    # Do switch logic. Note that it's way easier here. We'll get to the other order
                    # later so just think about what's in front of us.                    
                    if switchlogic:
                        if inputdict["ballnum"] == "2":
                            if setB.speciesName != inputdict["Species2"]:
                                continue
                        elif inputdict["ballnum"] == "3":
                            if setB.speciesName != inputdict["Species3"]:
                                continue

                        if setB.speciesName == inputdict["Species2"]:
                            if setC.calcSpeed(inputdict) > setB.calcSpeed(inputdict):
                                continue
                        elif setC.speciesName == inputdict["Species2"]:
                            if setB.calcSpeed(inputdict) >= setC.calcSpeed(inputdict):
                                continue
                        compoundProbability = 1/validOptionsFirst/validOptionsSecond/validOptionsThird
                    else:
                        compoundProbability = 1/validOptionsFirst/validOptionsSecond/validOptionsThird

                    # TEAM RECORDING                    
                    resultArray["total"] += compoundProbability                  
                    resultArray[setA.id] += compoundProbability
                    resultArray[setB.id] += compoundProbability
                    resultArray[setC.id] += compoundProbability
        resultList = []        
        for setId in resultArray:
            if setId == "total" or resultArray["total"] == 0 or resultArray[setId] == 0:
                    continue
            totalodds = 100*resultArray[setId]/resultArray["total"]                
            resultList.append([StaticDataHandler.StaticDataHandler.getSetFromName(setId),totalodds])                    
        results.loadHiResResults(resultList)        
        return(results)
