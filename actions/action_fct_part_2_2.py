import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction 2 de la partie 2
class AppFctPart_2_2(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_part_2_2.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("WITH list_pays(id,pays) as (SELECT DISTINCT numSp as id, pays FROM LesSportifs UNION SELECT DISTINCT numEq, pays FROM LesEquipiers JOIN LesSportifs USING (numSp)),res_or(pays,nbOr) AS (SELECT pays, count(gold) as nbOr FROM list_pays LEFT JOIN LesResultats ON (id=gold) GROUP BY pays), res_silver(pays,nbArgent) as (SELECT pays, count(silver) as nbArgent FROM list_pays LEFT JOIN LesResultats ON (id=silver) GROUP BY pays),res_bronze(pays,nbBronze) as (SELECT pays, count(bronze) as nbBronze FROM list_pays LEFT JOIN LesResultats ON (id=bronze) GROUP BY pays) SELECT pays,nbOr,nbArgent,nbBronze FROM res_or JOIN res_silver USING (pays) JOIN res_bronze USING (pays) ORDER BY nbOr DESC, nbArgent DESC, nbBronze DESC")
        except Exception as e:
            self.ui.table_fct_part_2_2.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_part_2_2, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_part_2_2, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_part_2_2, "Aucun résultat")