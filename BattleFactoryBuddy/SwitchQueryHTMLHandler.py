import BattleFactoryBuddy.StaticDataHandler as StaticDataHandler

class SwitchQueryHTMLHandler():
    speciesTable = """
    <table class="table w-auto" style="margin-left:10px;">
  <thead>
    <tr>
      <th scope="col" style="left-margin:10px;">Set</th>
      <th scope="col" style="border-left: 1px solid LightGrey">Section 1 score</th>
      <th scope="col" style="border-left: 1px solid LightGrey">Section 2 score<br>(2nd in party)</th>
      <th scope="col">Section 2 score<br>(3rd in party)</th>
    </tr>
  </thead>
  <tbody>
    {}    
  </tbody>
</table> 
"""
    speciesTableRow = """<tr>      
      <td><b>{}</b></td>
      <td style="border-left: 1px solid LightGrey">{}</td>
      <td style="border-left: 1px solid LightGrey">{}</td>
      <td>{}</td>      
    </tr>"""

    h2htablehtml = """
    <table class="table w-auto table-bordered" style="margin-left:10px;">
  <thead>
    <tr>
      <th scope="col" style="left-margin:10px;">H2H</th>
      {}
    </tr>
  </thead>
  <tbody>
    {}    
  </tbody>
</table> 
"""
    h2htablecolumn = """
        <th scope="col">{}</th>"""
    h2htablerow = """<tr>{}
    </tr>"""
    h2htablecell = """<td>{}</td>"""

    def __init__(self):
        pass

    def generateHTML(self, inputdict, results):        
        h2hHTML = ""        
        speciesTableList = []

        # Process the H2H table first if we've got 2 species.
        if len(results.switchResultsDict) == 2:
            headersList = []
            headersdone = False
            rowList = []
            for set1id in results.h2hResultsDict:                
                cellList = [self.h2htablecell.format(StaticDataHandler.StaticDataHandler.getNameFromId(set1id))]
                for set2id in results.h2hResultsDict[set1id]:
                    if not headersdone:
                        headersList.append(self.h2htablecolumn.format(StaticDataHandler.StaticDataHandler.getNameFromId(set2id)))
                    cellList.append(self.h2htablecell.format(results.h2hResultsDict[set1id][set2id]))
                headersdone = True
                rowList.append(self.h2htablerow.format("".join(cellList)))
            h2hHTML = self.h2htablehtml.format("".join(headersList),"".join(rowList))
            
        # Then populate each species table.
        for species in results.switchResultsDict:
            cellList = []
            for setuid in results.switchResultsDict[species]:
                setResult = results.switchResultsDict[species][setuid]
                cellList.append(self.speciesTableRow.format(StaticDataHandler.StaticDataHandler.getNameFromId(setuid),setResult[0],setResult[1] if setResult[0] == 0 else "-",setResult[2] if setResult[0] == 0 else "-"))
            speciesTableList.append(self.speciesTable.format("".join(cellList)))    
        inputdict["output"] = h2hHTML + "<br>".join(speciesTableList)
        return(inputdict)