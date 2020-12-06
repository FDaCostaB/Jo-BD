
CREATE TRIGGER Categorie_Participation
    BEFORE INSERT
        ON LesEquipiers
        WHEN ( 'mixte' NOT IN (SELECT distinct categorieEp FROM LesEpreuves JOIN LesInscriptions USING (numEp) WHERE numIn= New.numEq)
        AND ( (SELECT CategorieSp FROM LesSportifs_base WHERE numSp = New.numSp) NOT IN
            (SELECT distinct categorieEp FROM LesEpreuves JOIN LesInscriptions USING (numEp) WHERE numIn= New.numEq) )
            )
        AND ((SELECT distinct count(categorieEp) FROM LesEpreuves JOIN LesInscriptions USING (numEp) WHERE numIn= New.numEq) <> 0 )
    BEGIN
        SELECT RAISE(Fail, "L'equipier inscrit ne correspond avec la categorie ou l'equipe est inscrite");
    END; \