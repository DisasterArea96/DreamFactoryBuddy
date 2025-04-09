import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler


def calc(onLead):
    if onLead:
        filename = "./BattleFactoryBuddy/Data/MoveFrequencyOnLead.csv"
    else:
        filename = "./BattleFactoryBuddy/Data/MoveFrequencyOnTeam.csv"
    StaticDataHandler.StaticDataHandler.populateCache()
    movesToCheck = []
    for set in StaticDataHandler.StaticDataHandler.setList:
        for move in set.moveList:
            if move not in movesToCheck:
                movesToCheck.append(move)
    with open(filename, "w") as output:
        line = ","
        for type in StaticDataHandler.StaticDataHandler.teamLists:
            for phrase in StaticDataHandler.StaticDataHandler.teamLists[type]:
                line += type + "-" + phrase + ","
        output.write(line + "\n")
        movecounted = 0
        for movetocheck in movesToCheck:
            line = movetocheck + ","
            for type in StaticDataHandler.StaticDataHandler.teamLists:
                for phrase in StaticDataHandler.StaticDataHandler.teamLists[type]:
                    foundcount = 0
                    checkedcount = 0
                    for team in StaticDataHandler.StaticDataHandler.iterGetTeamList(
                        type, phrase
                    ):
                        # Assume that each set is an equal chance to be lead. Not quite true but not far off.
                        if onLead:
                            for setid in team[0:3]:
                                checkedcount += 1
                                set = StaticDataHandler.StaticDataHandler.getSetFromId(
                                    setid
                                )
                                for move in set.moveList:
                                    if move == movetocheck:
                                        foundcount += 1
                                        break
                        else:
                            checkedcount += 1
                            teamMoves = []
                            for setid in team[0:3]:
                                set = StaticDataHandler.StaticDataHandler.getSetFromId(
                                    setid
                                )
                                teamMoves += set.moveList
                            if movetocheck in teamMoves:
                                foundcount += 1
                    line += "{:.5f}%,".format((float(foundcount) / checkedcount) * 100)
            movecounted += 1
            print(
                "Completed %s - %s/%s"
                % (movetocheck, str(movecounted), str(len(movesToCheck)))
            )
            output.write(line + "\n")


if __name__ == "__main__":
    # calc(True)
    calc(False)
