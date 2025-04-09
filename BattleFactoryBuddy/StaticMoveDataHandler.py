# A static class to hold data about moves. Logically it'd be nice if this were just in
# StaticDataHandler but Set objects need to be able to reference Move data and the
# StaticDataHandler needs to create Sets and we therefore have to dodge a circular
# dependency somehow. This was the chosen solution
import BattleFactoryBuddy.Move as Move
import BattleFactoryBuddy.StaticHTMLHandler as StaticHTMLHandler

class StaticMoveDataHandler:
    # A dictionary of all move data parsed from provided moves files.
    moveDict = {}
    # A list of all move names used on Sets provided in allPkmn.csv.
    usedMoveList = []
    # The list HTML for a "choose a move" dropdown.
    moveHtml = ""
    
    # Parse out all the moves (used for switch logic)
    with open("./BattleFactoryBuddy/InputData/moves.csv") as f:
        for line in f:
            move = Move.Move(line.strip().split(","))
            moveDict[move.getName().lower().replace("-", " ").replace(" ","") ] = move

    @staticmethod
    def addUsedMove(moveName):
        if moveName not in StaticMoveDataHandler.usedMoveList:
            StaticMoveDataHandler.usedMoveList.append(moveName)
    
    @staticmethod
    def getMoveHtml():
        if StaticMoveDataHandler.moveHtml == "":
            StaticMoveDataHandler.usedMoveList.sort()
            StaticMoveDataHandler.moveHtml = StaticHTMLHandler.StaticHTMLHandler.createListHTMLfromList(StaticMoveDataHandler.usedMoveList)
        return(StaticMoveDataHandler.moveHtml)
    
    # Different sources for moves will have different capitalisation,
    # gaps between words etc. We want to be able to map from what's
    # in the spreadsheet to what's in the move data with minimal fuss.
    # This method greases the wheels and needs to match the logic done
    # when adding moves to the dictionary above.
    @staticmethod
    def rationaliseMoveName(moveName):
        return moveName.lower().replace("-", " ").replace(" ","")
    
    @staticmethod
    def getMove(moveName):
        rationalisedName = StaticMoveDataHandler.rationaliseMoveName(moveName)
        return StaticMoveDataHandler.moveDict[rationalisedName]

    # This code isn't currently required, but it may be useful in the future when switching logic is updated in dream factory

    # @staticmethod
    # def typeCalc(intype, targettypes, invalue, dropoutbeforeghostimms):
    #     retval = invalue
    #     temp = intype.upper()
    #     intype = temp
    #     temp = []
    #     for a in targettypes:
    #         temp.append(a.upper())
    #     targettypes = temp
    #     if intype == "NORMAL":
    #             if "ROCK" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "STEEL" in targettypes:
    #                     retval = int(retval*0.5)
    #     elif intype == "FIRE":
    #             if "FIRE" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "WATER" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "GRASS" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "ICE" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "BUG" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "ROCK" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "DRAGON" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "STEEL" in targettypes:
    #                     retval = int(retval*2.0)
    #     elif intype == "WATER":
    #             if "FIRE" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "WATER" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "GRASS" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "GROUND" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "ROCK" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "DRAGON" in targettypes:
    #                     retval = int(retval*0.5)
    #     elif intype == "ELECTRIC":
    #             if "WATER" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "ELECTRIC" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "GRASS" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "GROUND" in targettypes:
    #                     retval = int(retval*0.0)
    #             if "FLYING" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "DRAGON" in targettypes:
    #                     retval = int(retval*0.5)
    #     elif intype == "GRASS":
    #             if "FIRE" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "WATER" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "GRASS" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "POISON" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "GROUND" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "FLYING" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "BUG" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "ROCK" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "DRAGON" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "STEEL" in targettypes:
    #                     retval = int(retval*0.5)
    #     elif intype == "ICE":
    #             if "WATER" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "GRASS" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "ICE" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "GROUND" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "FLYING" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "DRAGON" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "STEEL" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "FIRE" in targettypes:
    #                     retval = int(retval*0.5)
    #     elif intype == "FIGHTING":
    #             if "NORMAL" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "ICE" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "POISON" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "FLYING" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "PSYCHIC" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "BUG" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "ROCK" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "DARK" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "STEEL" in targettypes:
    #                     retval = int(retval*2.0)
    #     elif intype == "POISON":
    #             if "GRASS" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "POISON" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "GROUND" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "ROCK" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "GHOST" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "STEEL" in targettypes:
    #                     retval = int(retval*0.0)
    #     elif intype == "GROUND":
    #             if "FIRE" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "ELECTRIC" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "GRASS" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "POISON" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "FLYING" in targettypes:
    #                     retval = int(retval*0.0)
    #             if "BUG" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "ROCK" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "STEEL" in targettypes:
    #                     retval = int(retval*2.0)
    #     elif intype == "FLYING":
    #             if "ELECTRIC" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "GRASS" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "FIGHTING" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "BUG" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "ROCK" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "STEEL" in targettypes:
    #                     retval = int(retval*0.5)
    #     elif intype == "PSYCHIC":
    #             if "FIGHTING" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "POISON" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "PSYCHIC" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "DARK" in targettypes:
    #                     retval = int(retval*0.0)
    #             if "STEEL" in targettypes:
    #                     retval = int(retval*0.5)
    #     elif intype == "BUG":
    #             if "FIRE" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "GRASS" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "FIGHTING" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "POISON" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "FLYING" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "PSYCHIC" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "GHOST" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "DARK" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "STEEL" in targettypes:
    #                     retval = int(retval*0.5)
    #     elif intype == "ROCK":
    #             if "FIRE" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "ICE" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "FIGHTING" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "GROUND" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "FLYING" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "BUG" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "STEEL" in targettypes:
    #                     retval = int(retval*0.5)
    #     elif intype == "GHOST":
    #             if "NORMAL" in targettypes:
    #                     retval = int(retval*0.0)
    #             if "PSYCHIC" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "DARK" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "STEEL" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "GHOST" in targettypes:
    #                     retval = int(retval*2.0)
    #     elif intype == "DRAGON":
    #             if "DRAGON" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "STEEL" in targettypes:
    #                     retval = int(retval*0.5)
    #     elif intype == "DARK":
    #             if "FIGHTING" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "PSYCHIC" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "GHOST" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "DARK" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "STEEL" in targettypes:
    #                     retval = int(retval*0.5)
    #     elif intype == "STEEL":
    #             if "FIRE" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "WATER" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "ELECTRIC" in targettypes:
    #                     retval = int(retval*0.5)
    #             if "ICE" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "ROCK" in targettypes:
    #                     retval = int(retval*2.0)
    #             if "STEEL" in targettypes:
    #                     retval = int(retval*0.5)
    #     if dropoutbeforeghostimms:
    #             return retval
    #     if intype == "NORMAL":
    #             if "GHOST" in targettypes:
    #                     retval = int(retval*0.0)
    #     elif intype == "FIGHTING":
    #             if "GHOST" in targettypes:
    #                     retval = int(retval*0.0)
    #     return retval
