import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction 2 de la partie 2
class AppFctPart_3_3(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_part_3_3.ui", self)
        self.data = data
        self.initialiserEquipe()
        #self.initialiserInscrits()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def insertResult(self):
        try:
            identite = self.ui.comboBox_part_3_3_numSp.currentText().split();
            cursor = self.data.cursor()
            result = cursor.execute("SELECT numSp FROM LesSportifs_base WHERE prenomSp=? and nomSp=?",
                           (identite[0],identite[1]) )
            self.data.commit()
            num = [str(i[0]) for i in cursor.fetchall()]
            if self.checkBox_Delete.isChecked():
                result = cursor.execute("DELETE FROM LesEquipiers WHERE numEq=? AND numSp=?;",
                                        (self.comboBox_part_3_3_numEq.currentText(),
                                         num[0]))

            else:
                result = cursor.execute("INSERT INTO LesEquipiers (numSp, numEq) VALUES (?, ?);",
                                        (num[0],
                                         self.comboBox_part_3_3_numEq.currentText()))

            self.data.commit()
        except Exception as e:
            display.refreshLabel(self.ui.label_part_3_3, "Impossible de mettre à jour l'équipe : " + repr(e))
            print(repr(e))
        else:
            display.refreshLabel(self.ui.label_part_3_3, "Equipe mis à jour")
            self.initialiserSportifs()

    def initialiserSportifs(self):
        cursor = self.data.cursor()
        if self.checkBox_Delete.isChecked() :
            cursor.execute("SELECT prenomSp,nomSp FROM LesSportifs_base JOIN LesEquipiers USING (numSp) WHERE numEq=?",
                [self.ui.comboBox_part_3_3_numEq.currentText()])
            sportifs = [str(i[0] + " " + i[1]) for i in cursor.fetchall()]
            self.comboBox_part_3_3_numSp.clear()
            self.comboBox_part_3_3_numSp.addItems(sportifs)
        else :
            cursor.execute("WITH Country AS (SELECT DISTINCT pays FROM LesSportifs_base WHERE numSp IN (SELECT numSp FROM LesEquipiers WHERE numEq=?))SELECT prenomSp,nomSp FROM LesSportifs_base WHERE pays IN Country EXCEPT SELECT prenomSp,nomSp FROM LesSportifs_base JOIN LesEquipiers USING (numSp) WHERE numEq=1",
                       [self.ui.comboBox_part_3_3_numEq.currentText()])
            sportifs = [str(i[0] +" "+ i[1]) for i in cursor.fetchall()]
            self.comboBox_part_3_3_numSp.clear()
            self.comboBox_part_3_3_numSp.addItems(sportifs)

    def initialiserEquipe(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT numEq FROM LesEquipes")
        equipe = [str(i[0]) for i in cursor.fetchall()]
        self.comboBox_part_3_3_numEq.clear()
        self.comboBox_part_3_3_numEq.addItems(equipe)