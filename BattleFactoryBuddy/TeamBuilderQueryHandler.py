import itertools
import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler


class TeamResult():
    def __init__(self, teamTuples, oppIVs, level="100", round="8"):
        self.teamTuples = teamTuples
        self.teamSets = []
        for tuple in self.teamTuples:
            self.teamSets.append(tuple[0])
        self.winDict = {}
        self.resultsList = []
        self.deadList = []
        self.veryBadList = []
        self.badList = []
        self.midList = []
        self.stompList = []
        self.level = level
        self.round = round
        self.oppIVs = oppIVs
        self.blockedsets = {}
        if self.oppIVs != "3":
            for oppSetId in self.teamSets:
                self.blockedsets[oppSetId] = 1
        else:
            for oppSetId in self.teamSets:
                i = 1
                while i < 11:
                    self.blockedsets[oppSetId.split("-")[0] + "-" + str(i)] = 1
                    i += 1                
    
    def generateResults(self):
        level = self.level
        round = self.round
        teamSetList = []
        if (level == "50" and round == "8") or (level == "100" and int(round) > 4):
            teamSetList += ["5"]
            if level == "100":
                teamSetList += ["6"]
            teamSetList += ["4", "3", "2", "1"]
        elif (level == "50" and round == "7") or (level == "100" and round == "4"):
            teamSetList += ["4"]
        elif (level == "50" and round == "6") or (level == "100" and round == "3"):
            teamSetList += ["3"]
        elif (level == "50" and round == "5") or (level == "100" and round == "2"):
            teamSetList += ["2"]
        elif (level == "50" and round == "4") or (level == "100" and round == "1"):
            teamSetList += ["1"]
        for teamSet in self.teamTuples:
            for (oppSetId, result) in StaticDataHandler.StaticDataHandler.iterGetH2HResult(*teamSet,self.oppIVs):
                if str(StaticDataHandler.StaticDataHandler.getSetFromName(oppSetId).roundInfo) not in teamSetList:
                    continue                
                if oppSetId in self.blockedsets:
                    continue                    
                if oppSetId not in self.winDict:
                    self.winDict[oppSetId] = 0                              
                self.winDict[oppSetId] += result[0]
        
        for (oppSetId, result) in self.winDict.items():
            self.resultsList.append((oppSetId,result))
            self.resultsList.sort(key=lambda tuple: tuple[0])    
            self.resultsList.sort(key=lambda tuple: tuple[1])

        for (oppSetId, result) in self.resultsList:
            if result < 6:
                self.deadList.append((oppSetId,result))
            elif result < 12:
                self.veryBadList.append((oppSetId,result))
            elif result < 24:
                self.badList.append((oppSetId,result))
            elif result < 40:
                self.midList.append((oppSetId,result))
            else:
                self.stompList.append((oppSetId,result))
        
    def getResults(self):            
        strFrag = "{} ({} wins), "
        retstr = ""        
        retstr += "<b>----Dead (0-5 wins)----"        
        printstr = " {} sets found <br></b>".format(str(len(self.deadList)))
        for (oppSetId, result) in self.deadList:
            printstr += strFrag.format(oppSetId,result)
        retstr += printstr + "<br>"

        retstr += "<b>----Very Bad (6-11 wins)---- "
        printstr = "{} sets found<br></b>".format(str(len(self.veryBadList)))
        for (oppSetId, result) in self.veryBadList:
            printstr += strFrag.format(oppSetId,result)
        retstr +=printstr + "<br>"

        retstr += "<b>----Bad (12-23 wins)---- "
        printstr = "{} sets found <br></b>".format(str(len(self.badList)))        
        for (oppSetId, result) in self.badList:
            printstr += strFrag.format(oppSetId,result)
        retstr+=printstr + "<br>"

        retstr += "<b>----Mid (24-39 wins)---- "
        retstr += "{} sets found<br></b>".format(str(len(self.midList)))        
        

        retstr += "<b>----Stomp (40-60 wins)---- "
        retstr += "{} sets found<br></b>".format(str(len(self.stompList)))        
        return(retstr)
        
    
    def getTeamScore(self):
        score = 0
        score += 20*len(self.deadList)
        score += 12*len(self.veryBadList)
        score += 5*len(self.badList)
        score += 0.5*len(self.midList)
        return(score)

    def getSummary(self):           
        retstr =  "<b>{}</b> - {} ({} / {} / {})".format(self.getTeamScore(),self.getTeamString(),len(self.deadList),len(self.veryBadList),len(self.badList))
        return(retstr)

    def getTeamString(self):
        retstr = ""
        for teamtuple in self.teamTuples:
            retstr += "{} ({}IVs), ".format(*teamtuple) 
        retstr = retstr[:-2]
        return(retstr)

class TeamBuilderQueryHandler():
    def __init__(self, inputdict):
        self.inputdict = inputdict        

    def handleQuery(self):
        if self.inputdict["Level"] == "50" and self.inputdict["Round"] in ["1","2","3"]:
            self.inputdict["output"] = "Sorry - level 50 rounds 1 - 3 aren't supported yet."
            return(self.inputdict)
        teamSets = []
        for key in ["set1","set2","set3","set4","set5","set6"]:
            if self.inputdict[key] == "":
                continue
            teamSets.append((self.inputdict[key],self.inputdict[key+"IVs"]))
        if len(teamSets) < 3:
            self.inputdict["output"] = "Not enough mons provided"
            return(self.inputdict)

        swapMode = True if self.inputdict.get("SwapMode", "off") == "on" else False
        currentTeam = teamSets[0:3]

        outputstr = ""
        minScore = 0
        mintr = None
        trResultList = []
        possibleTeams = itertools.combinations(teamSets, 3)

        for teamTuples in possibleTeams:
            # If using swap mode, pass over teams which don't contain
            # two of the first three sets
            if swapMode and (len(set(teamTuples) & set(currentTeam)) < 2):
                continue
            
            # If we have 2 of the same species, don't allow a team with both. Impossible during the rounds
            # but possible during the draft.
            if len(set([teamTuples[0][0].split("-")[0],teamTuples[1][0].split("-")[0],teamTuples[2][0].split("-")[0]])) != 3:
                continue           

            tr = TeamResult(
                teamTuples,
                self.inputdict["OppIVs"],
                self.inputdict["Level"],
                self.inputdict["Round"],
            )
            tr.generateResults()
            if (mintr == None) or (tr.getTeamScore() < minScore):
                mintr = tr
                minScore = mintr.getTeamScore()
            trResultList.append((tr.getTeamScore(), tr))

        trResultList.sort(key=lambda tuple: tuple[0])
        topTeam = trResultList[0][1]

        if swapMode:
            swapString = ""
            difference = set(topTeam.teamTuples).symmetric_difference(set(currentTeam))
            if len(difference) == 2:
                mon1 = difference.pop()
                mon2 = difference.pop()
                if (mon1) in currentTeam:
                    exitingMon = mon1
                    arrivingMon = mon2
                else:
                    arrivingMon = mon1
                    exitingMon = mon2

                exitingStr = "{} ({}IVs) ".format(*exitingMon)
                arrivingStr = "{} ({}IVs) ".format(*arrivingMon)
                swapString += (
                    f"Best swap found: Old <b>{exitingStr}</b> -> New <b>{arrivingStr}</b><br>"
                )
            else:
                swapString += "No swaps found to improve the current team <br>"

        outputstr += """<font size="2"><i> Please note, this is a fundamentally limited tool that looks only at the result of each of your sets doing 20 head-to-head matchups against each opposing set (so a team can have a max of 60 wins across all 3 mons). Use this as a resource to think about potential weaknesses but do not rely on it as any sort of source of truth. It also has no logic about team ordering, you're on your own for that.</i></font><br>"""
        if swapMode:
            outputstr += swapString
        outputstr += "Best team found: <b>{}</b><br><br>".format(topTeam.getSummary())        
        accordionContainer = """<div class="col" style="max-width:1200px"> 
                    <div class="accordion" id="accordionOne">{}                    
                    </div>
                </div>"""
        accordionSection = """
                        <div class="accordion-item" style="margin-left:10px;">
                            <h2 class="accordion-header" id="heading{}">
                                <button class="accordion-button {}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{}" aria-expanded="{}" aria-controls="collapse{}">
                                    {}
                                </button>
                            </h2>
                            <div id="collapse{}" class="accordion-collapse collapse {}" aria-labelledby="heading{}" data-bs-parent="#accordionExample">
                                <div class="accordion-body"><font size="2">
                                {} </font>
                                </div>
                            </div>                        
                        </div>
                    """
        sectionstr = ""
        i = 0
        for (result, tr) in trResultList:
            if i == 0:
                sectionstr += accordionSection.format(str(i),"",str(i),"true",str(i),tr.getSummary(),str(i),"show",str(i),tr.getResults())
            else:
                sectionstr += accordionSection.format(str(i),"collapsed",str(i),"false",str(i),tr.getSummary(),str(i),"hide",str(i),tr.getResults())        
            i+=1
        outputstr += accordionContainer.format(sectionstr)
        self.inputdict["output"] = outputstr
        return(self.inputdict)
