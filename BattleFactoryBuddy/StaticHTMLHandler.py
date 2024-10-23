
# A class to cover HTML generation that isn't specific to a given query.
# This is currently mostly lists that go into the UI such as potential
# species, moves and items.
class StaticHTMLHandler():
    listOption = "<option value=\"{}\">{}</option>"

    @staticmethod
    def createListHTMLfromList(inputList):
        html = ""
        for item in inputList:
            html += StaticHTMLHandler.listOption.format(item,item)
        return(html)
