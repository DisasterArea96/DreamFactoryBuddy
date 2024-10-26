import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler
import BattleFactoryBuddy.SetCalcHandler as SetCalcHandler
import BattleFactoryBuddy.SetQueryHTMLHandler as SetQueryHTMLHandler
import BattleFactoryBuddy.Results as Results
import traceback

# The main entry point to the server code for the "main" buddy functionality. Takes in a dictionary of info
# posted from the browser and returns back the same dictionary with added HTML covering answers or
# errors.
class SetQueryHandler:
    seenSpeciesKey = ("Species1", "Species2", "Species3")
    blockedSpeciesKey = ("Team1", "Team2", "Team3", "LastOpp1", "LastOpp2", "LastOpp3")

    def __init__(self, inputdict):
        self.inputdict = inputdict

    def handleQuery(self):
        htmlHandler = SetQueryHTMLHandler.SetQueryHTMLHandler()
        results = Results.Results(self.inputdict)
        try:            
            (valid, results) = self.validateQueryAndNormaliseInputs(results)
            if not valid:
                self.inputdict = htmlHandler.buildHTML(self.inputdict, results)
                return self.inputdict
            results = SetCalcHandler.SetCalcHandler().calculate(self.inputdict, results)
            self.inputdict = htmlHandler.buildHTML(self.inputdict, results)
        except Exception:
            print(traceback.format_exc())
            results.addError("Battle Factory Buddy hit an error :(\n Please try again and / or report the issue.")
            self.inputdict = htmlHandler.buildHTML(self.inputdict, results)
        return self.inputdict

    # Handles checking whether the query we've been given is valid. This mostly covers users inputting`
    # invalid option combinations. We also normalise anything left unfilled, e.g. not adding a
    # Magic Number for switch logic.
    def validateQueryAndNormaliseInputs(self, results):
        # Check we've got a good round.
        oppivs = self.inputdict["Battle"]  # "3","7","11"
        round = self.inputdict["Round"]  # 1-8 - 8 refers to 8+
        level = self.inputdict["Level"]  # "50","100"

        # Check if Noland is being invoked incorrectly.
        if round not in ["3", "6", "8"] and oppivs == "11":
            results.addError(
                "Error: Opponent type has been entered as Noland but this is not a Noland round."
            )
            return (False, results)
        elif round in ["3", "6"] and oppivs == "7":
            results.addError(
                "Error: Opponent type has not been entered as Noland but this is a Noland round."
            )
            return (False, results)

        # If it's Noland and there's no input mons, just return a reminder
        # that there's nothing to check.
        if oppivs == "11":
            foundMonForNoland = False
            for seenSpeciesKey in SetQueryHandler.seenSpeciesKey:
                if self.inputdict[seenSpeciesKey] != "":
                    foundMonForNoland = True
                    break
            if not foundMonForNoland:
                results.addError("Noland Time! He can have any set you don't have.")
                return (False, results)

        # Check if any of the seen mons are mons we've said can't happen.
        for seenSpeciesKey in SetQueryHandler.seenSpeciesKey:
            if self.inputdict[seenSpeciesKey] != "":
                for blockedSpeciesKey in SetQueryHandler.blockedSpeciesKey:
                    if (
                        self.inputdict[seenSpeciesKey]
                        == self.inputdict[blockedSpeciesKey]
                    ):
                        results.addError(
                            "Error: Opponent species %s is entered as being on your team or the last team."%(self.inputdict[seenSpeciesKey])
                        )
                        return (False, results)

        # Add in the magic number if the user hasn't entered one and switch-in logic is on.
        if (
            "switchin" in self.inputdict
            and "targetmon" in self.inputdict
            and self.inputdict["targetmon"] != ""
            and self.inputdict["Species2"] != ""
            and self.inputdict["Species1"] != ""
        ):
            if (
                "magicnumber" not in self.inputdict
                or self.inputdict["magicnumber"] == ""
            ):
                self.inputdict["magicnumber"] = 40

        # If we've got Probability sort and NoOdds selected, deselect probability sort.
        if "NoOdds" in self.inputdict and "ProbabilitySort" in self.inputdict:
            self.inputdict.pop("ProbabilitySort")

        # If we've got Detail Mode and NoOdds selected, deselect NoOdds.
        if "NoOdds" in self.inputdict and "DetailMode" in self.inputdict:
            self.inputdict.pop("DetailMode")

        # If we've got here then we've not found anything wrong. Return true and the (unedited) Results Object.
        return (True, results)
