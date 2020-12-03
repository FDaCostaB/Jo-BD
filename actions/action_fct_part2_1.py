
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 4
class AppFctPart2_1(QDialog):
    def initialiserid(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT DISTINCT numEq FROM LesEquipiers JOIN LesSportifs USING (numSp) WHERE pays =?",
                       [self.ui.comboBox_fct_4_pays.currentText()])
        ids = [str(i[0]) for i in cursor.fetchall()]
        self.comboBox_fct_4_equipe.clear()
        self.comboBox_fct_4_equipe.addItems(ids)
    def initialiserpays(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT DISTINCT pays FROM LesSportifs JOIN LesEquipiers USING (numSp)")
        pays = [i[0] for i in cursor.fetchall()]
        self.comboBox_fct_4_pays.clear()
        self.comboBox_fct_4_pays.addItems(pays)
    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_4.ui", self)
        self.data = data
        self.refreshCatList()
        self.initialiserpays()
        self.initialiserid()

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        display.refreshLabel(self.ui.label_fct_comp_4, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "WITH AgeSpOr AS (
                    WITH EqWinning AS (
                        SELECT DISTINCT "numSp","numEq"
	                    FROM "LesEquipiers" JOIN "LesResultats" ON (gold="numEq") )
                    SELECT "numSp","age"
                    FROM "LesSportifs" JOIN EqWinning USING ("numSp")
                    UNION
                    SELECT "numSp","age"
                    FROM "LesSportifs" JOIN "LesResultats" ON (gold="numSp")
                )
                SELECT AVG(age) FROM AgeSpOr;",
                [self.ui.comboBox_fct_4_pays.currentText(),self.ui.comboBox_fct_4_equipe.currentText()]
            )
        except Exception as e:
            self.ui.table_fct_comp_4.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_4, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_4, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_4, "Aucun résultat")

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
