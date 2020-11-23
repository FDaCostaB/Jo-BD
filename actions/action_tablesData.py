
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fenêtre de visualisation des données
class AppTablesData(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/tablesData.ui", self)
        self.data = data

        # On met à jour l'affichage avec les données actuellement présentes dans la base
        self.refreshAllTables()

    ####################################################################################################################
    # Méthodes permettant de rafraichir les différentes tables
    ####################################################################################################################

    # Fonction de mise à jour de l'affichage d'une seule table
    def refreshTable(self, label, table, query):
        display.refreshLabel(label, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            table.setRowCount(0)
            display.refreshLabel(label, "Impossible d'afficher les données de la table : " + repr(e))
        else:
            display.refreshGenericData(table, result)


    # Fonction permettant de mettre à jour toutes les tables
    @pyqtSlot()
    def refreshAllTables(self):

        self.refreshTable(self.ui.label_equipiers, self.ui.tableEquipiers, "SELECT numEq, numSp  FROM LesEquipiers")
        self.refreshTable(self.ui.label_epreuves, self.ui.tableEpreuves, "SELECT numEp, nomEp, formeEp, categorieEp, nbSportifsEp, dateEp FROM LesEpreuves")
        self.refreshTable(self.ui.label_inscriptions, self.ui.tableInscriptions, "SELECT numIn, numEp FROM LesInscriptions")
        self.refreshTable(self.ui.label_resultats, self.ui.tableResultats, "SELECT numEp, gold, silver, bronze FROM LesResultats")
        self.refreshTable(self.ui.label_sportifs, self.ui.tableSportifs, "SELECT numSp, nomSp, prenomSp, pays, categorieSp, date(dateNaisSp) FROM LesSportifs_base")
        # TODO 1.2b : ajouter l'affichage des éléments de la vue LesSportifs après l'avoir créée
        # TODO 1.3d : afficher le contenu de la table LesDisciplines et ajouter l'attribut discipline dans l'affichage de la table LesEpreuves
        # TODO 1.4b : ajouter l'affichage des éléments de la vue LesEquipes après l'avoir créée
