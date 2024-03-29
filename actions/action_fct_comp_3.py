import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


# Classe permettant d'afficher la fonction à compléter 3
class AppFctComp3(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_3.ui", self)
        self.data = data
        self.initaliser()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()

    def initaliser(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT DISTINCT categorieEp FROM LesEpreuves")
        result = cursor.fetchall()
        categories = [i[0] for i in result]
        self.cb_fct_comp_3.clear()
        self.cb_fct_comp_3.addItems(categories)

    def refreshResult(self):

        display.refreshLabel(self.ui.label_fct_comp_3, "")

        if not self.ui.cb_fct_comp_3.currentText():
            self.ui.table_fct_comp_3.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_3, "Veuillez indiquer un nom de catégorie")
        else:
            try:
                cursor = self.data.cursor()
                result = cursor.execute(
                    "SELECT numEp, nomEp, formeEp, nomDi, nbSportifsEp, dateEp FROM LesEpreuves WHERE categorieEp = ?",
                    [self.ui.cb_fct_comp_3.currentText()])
            except Exception as e:
                self.ui.table_fct_comp_3.setRowCount(0)
                display.refreshLabel(self.ui.label_fct_comp_3, "Impossible d'afficher les résultats : " + repr(e))
            else:
                i = display.refreshGenericData(self.ui.table_fct_comp_3, result)
                if i == 0:
                    display.refreshLabel(self.ui.label_fct_comp_3, "Aucun résultat")
