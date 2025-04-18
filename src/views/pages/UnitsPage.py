from src.views.pages.BasePageWidget import BasePageWidget
from src.views.components.UnitsTable import UnitsTable
from src.controllers.unitsController import UnitsController

class UnitsPage(BasePageWidget):
    def __init__(self, mainWindow=None):
        self.buttonText = "Add Unit"
        super().__init__(UnitsTable, self.buttonText, mainWindow=mainWindow)

    def updatePage(self):
        self.table.updateTable()

    def handleAddButton(self):
        response = UnitsController.addRecord(None)
        self.table.updateTable()