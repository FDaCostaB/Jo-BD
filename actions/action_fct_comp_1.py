
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 1
class AppFctComp1(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_1.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

        display.refreshLabel(self.ui.label_fct_comp_1, "")
        if not self.ui.lineEdit.text().strip():
            self.ui.table_fct_comp_1.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_1, "Veuillez indiquer un numéro d'équipe")
        else:
            try:
                cursor = self.data.cursor()
                result = cursor.execute("SELECT nomSp, prenomSp, pays, categorieSp, date(dateNaisSp) FROM LesSportifs_base JOIN LesEquipiers USING (numSp) WHERE numEq = ?", [self.ui.lineEdit.text().strip()])
            except Exception as e:
                self.ui.table_fct_comp_1.setRowCount(0)
                display.refreshLabel(self.ui.label_fct_comp_1, "Impossible d'afficher les résultats : " + repr(e))
            else:
                i = display.refreshGenericData(self.ui.table_fct_comp_1, result)
                if i == 0:
                    display.refreshLabel(self.ui.label_fct_comp_1, "Aucun résultat")