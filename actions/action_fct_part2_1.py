
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 4
class AppFctPart2_1(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_part2_1.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        display.refreshLabel(self.ui.label_fct_part2_1, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "WITH EqWinning AS ( SELECT DISTINCT numSp,numEq  FROM LesEquipiers JOIN LesResultats ON (gold=numEq) ) SELECT numEq,ROUND(AVG(age),2) FROM LesSportifs JOIN EqWinning USING (numSp) GROUP BY numEq")
        except Exception as e:
            self.ui.table_fct_part2_1.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_part2_1, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_part2_1, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_part2_1, "Aucun résultat")

    # Fonction de mise à jour des catégories
    @pyqtSlot()
    def refreshCatList(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT pays FROM LesSportifs_base ORDER BY pays")
        except Exception as e:
            self.ui.comboBox_fct_4_pays.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_fct_4_pays, result)
