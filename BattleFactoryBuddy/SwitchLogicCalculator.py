import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler

# A static utility class covering calculating switch-in logic given scores generated
# by Set Objects.
class SwitchLogicCalculator():
    pass

    @staticmethod
    def getTeamCountFromSwitchScoresVal(scorea, scoreb):
        retnum = SwitchLogicCalculator.doesAcomeInOverB(scorea, scoreb)
        retnum += 1 - SwitchLogicCalculator.doesAcomeInOverB(scoreb, scorea)
        return retnum

    @staticmethod
    def doesAcomeInOverB(scorea, scoreb):
        if scorea[0] > scoreb[0]:
            return 1
        elif scoreb[0] > scorea[0]:
            return 0
        elif (scoreb[0] == scorea[0]) and (scorea[0] > 0):
            return 1
        if scorea[1] < scoreb[2]:
            return 0
        else:
            return 1

    @staticmethod
    def getTeamCountFromSwitchScoresValWithBall(scorea, scoreb, ballnum):
        if ballnum == "2":
            return SwitchLogicCalculator.doesAcomeInOverB(scorea, scoreb)
        # If the mon in the 3rd ball came in it must have "won" some
        # round of calculation. i.e. the other one didn't win.
        else:
            return 1 - SwitchLogicCalculator.doesAcomeInOverB(scoreb, scorea)