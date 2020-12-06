import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction 2 de la partie 2
class AppFctPart_3_1(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_part_3_1.ui", self)
        self.data = data
        self.initialiser_epreuves()


    def initialiser_epreuves(self):
        #Fonction qui filtre les numéros des epreuves, les epreuves qui n'ont pas de date de debut sont enlevées
        cursor = self.data.cursor()
        cursor.execute("SELECT numEp FROM LesEpreuves")
        numEplist = [str(i[0]) for i in cursor.fetchall()]
        i=0
        while i<len(numEplist):
            cursor.execute("SELECT dateEp FROM LesEpreuves WHERE numEp=?",[numEplist[i]])
            fetch = cursor.fetchall()
            if fetch[0][0]==None:
                numEplist.pop(i)
            else: i+=1
        self.comboBox_part_3_1_numEp.clear()
        self.comboBox_part_3_1_numEp.addItems(numEplist)

    def initialiser_participants(self):
        #Fonction qui filtre les listes des sportifs et celles des equipes par rapport à la taille de l'équipe, catégorie et la date de naissance des sportifs
        cursor = self.data.cursor()
        numEp = self.ui.comboBox_part_3_1_numEp.currentText()
        cursor.execute("SELECT formeEp,nbSportifsEp,categorieEp,dateEp FROM LesEpreuves WHERE numEp = ?",[numEp])
        fetch = cursor.fetchall()
        forme = str(fetch[0][0])
        nbSportifs = fetch[0][1]
        categorie = str(fetch[0][2])
        dateEp = str(fetch[0][3])
        if forme == "individuelle":
            cursor.execute("SELECT numSp FROM LesSportifs_base WHERE categorieSp = ? and date(dateNaisSp)<date(?)", [categorie,dateEp])
            id = [str(i[0]) for i in cursor.fetchall()]
        if nbSportifs != None:
            if forme == "par couple" or forme == "par equipe":
                cursor.execute("SELECT numEq FROM LesEquipes WHERE nbEquipiersEq = ?",[nbSportifs])
                id = [str(i[0]) for i in cursor.fetchall()]
                i = 0
                while i<len(id):
                    cursor.execute("SELECT nbEquipiersEq FROM LesEquipes WHERE numEq=?",[int(id[i])])
                    fetch = cursor.fetchall()
                    equipe_size = fetch[0][0]
                    cursor.execute("SELECT count(numSp) FROM LesEquipiers JOIN LesSportifs USING (numSp) WHERE numEq=? and categorieSp=?",[id[i],categorie])
                    fetch = cursor.fetchall()
                    if fetch[0][0] != equipe_size and categorie!="mixte":
                        id.pop(i)
                    else:
                        i+=1
        elif nbSportifs == None:
            if forme == "par couple":
                cursor.execute("SELECT numEq FROM LesEquipes WHERE nbEquipiersEq = 2")
                id = [str(i[0]) for i in cursor.fetchall()]
                i = 0
                while i < len(id):
                    cursor.execute("SELECT nbEquipiersEq FROM LesEquipes WHERE numEq=?",[id[i]])
                    fetch = cursor.fetchall()
                    equipe_size = fetch[0][0]
                    cursor.execute(
                        "SELECT count(numSp) FROM LesEquipiers JOIN LesSportifs USING (numSp) WHERE numEq=? and categorieSp=?",[id[i], categorie])
                    fetch = cursor.fetchall()
                    if fetch[0][0] != equipe_size and categorie!="mixte":
                        id.pop(i)
                    else:
                        i += 1
            elif forme == "par equipe":
                cursor.execute("SELECT numEq FROM LesEquipes WHERE nbEquipiersEq > 1")
                id = [str(i[0]) for i in cursor.fetchall()]
                i = 0
                while i < len(id):
                    cursor.execute("SELECT nbEquipiersEq FROM LesEquipes WHERE numEq=?", [id[i]])
                    fetch = cursor.fetchall()
                    equipe_size = fetch[0][0]
                    cursor.execute(
                        "SELECT count(numSp) FROM LesEquipiers JOIN LesSportifs USING (numSp) WHERE numEq=? and categorieSp=?",
                        [id[i], categorie])
                    fetch = cursor.fetchall()
                    if fetch[0][0] != equipe_size and categorie != "mixte":
                        id.pop(i)
                    else:
                        i += 1
        self.comboBox_part_3_1_numSpEq.clear()
        if len(id)>0:
            self.comboBox_part_3_1_numSpEq.addItems(id)

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        try:
            cursor = self.data.cursor()
            cursor.execute("INSERT INTO LesInscriptions(numEp,numIn) VALUES (?, ?);",[self.comboBox_part_3_1_numEp.currentText(),self.comboBox_part_3_1_numSpEq.currentText()])
            self.data.commit()
        except Exception as e:
            display.refreshLabel(self.ui.label_part_3_1, "Impossible de valider les résultats : " + repr(e))
        else:
            display.refreshLabel(self.ui.label_part_3_1, "Résultat validé")
