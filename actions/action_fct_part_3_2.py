import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction 2 de la partie 2
class AppFctPart_3_2(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_part_3_2.ui", self)
        self.data = data
        self.initialiserEpreuve()
        self.initialiserInscrits()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def insertResult(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("INSERT INTO LesResultats (numEp, gold, silver, bronze) VALUES (?, ?, ?, ?);",
                                    (self.comboBox_part_3_2_numEp.currentText(),
                                    self.comboBox_part_3_2_or.currentText(),
                                    self.comboBox_part_3_2_argent.currentText(),
                                    self.comboBox_part_3_2_bronze.currentText()))
            self.data.commit()
        except Exception as e:
            display.refreshLabel(self.ui.label_part_3_2, "Impossible de valider les résultats : " + repr(e))
        else:
            display.refreshLabel(self.ui.label_part_3_2, "Résultat validé")

    def initialiserInscrits(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT numIN FROM LesInscriptions WHERE (numEp=?)",
                       [self.ui.comboBox_part_3_2_numEp.currentText()])
        inscrits = [str(i[0]) for i in cursor.fetchall()]
        self.comboBox_part_3_2_or.clear()
        self.comboBox_part_3_2_argent.clear()
        self.comboBox_part_3_2_bronze.clear()
        self.comboBox_part_3_2_or.addItems(inscrits)
        self.comboBox_part_3_2_argent.addItems(inscrits)
        self.comboBox_part_3_2_bronze.addItems(inscrits)

    def initialiserEpreuve(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT numEp FROM LesEpreuves WHERE date(dateEp) < date()")
        epreuve = [str(i[0]) for i in cursor.fetchall()]
        self.comboBox_part_3_2_numEp.clear()
        self.comboBox_part_3_2_numEp.addItems(epreuve)
