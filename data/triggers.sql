CREATE TRIGGER Meme_Nationalité_Dans_Equipe
    BEFORE INSERT
        ON EquipeEngage
        WHEN (EXISTS (SELECT Equipe.Nationalité FROM Equipe WHERE (New.Id_Equipe = Equipe.Id)) and
            New.Nationalité NOT IN (SELECT Equipe.Nationalité FROM Equipe WHERE (New.Id_Equipe = Equipe.Id)))
BEGIN
    SELECT RAISE(Fail, "Contrainte violée T1");
END; \

CREATE TRIGGER Meme_Categorie_Dans_Equipe
    BEFORE INSERT
        ON EquipeEngage
        WHEN (EXISTS (SELECT Equipe.Categorie FROM Equipe WHERE (New.Id_Equipe = Equipe.Id)) and
            New.Categorie NOT IN (SELECT Equipe.Categorie FROM Equipe WHERE (New.Id_Equipe = Equipe.Id))
            and (SELECT Equipe.Categorie FROM Equipe WHERE (New.Id_Equipe = Equipe.Id) <> 'Mixte'))
BEGIN
    SELECT RAISE(Fail, "Contrainte violée T2");
END;\

CREATE TRIGGER Meme_Categorie_Dans_Epreuve
    BEFORE INSERT
        ON SportifsParticipe
        WHEN (
            (SELECT Sexe FROM Sportifs WHERE Sportifs.Id = New.Id_Sportifs) <>
                (SELECT Categorie FROM Epreuve WHERE Epreuve.Id = New.Id_Epreuve)
            and ((SELECT Categorie FROM Epreuve WHERE Epreuve.Id = New.Id_Epreuve) <> 'Mixte'))
BEGIN
    SELECT RAISE(Fail, "Contrainte violée T3");
END; \

CREATE TRIGGER Taille_Participation_Equipe
    BEFORE INSERT
        ON EquipeParticipe
        WHEN ((SELECT TailleEq FROM Epreuve WHERE Epreuve.Id = New.Id_Epreuve) <>
            (SELECT count(Id) FROM EquipeEngage WHERE EquipeEngage.Id_Equipe = New.Id_Equipe))
    BEGIN
        SELECT RAISE(Fail, "Contrainte violée T8");
    END; \

CREATE TRIGGER Taille_Pariticpation_Solo
    BEFORE INSERT
        ON SportifsParticipe
        WHEN ((SELECT TailleEq FROM Epreuve WHERE Epreuve.Id = New.Id_Epreuve) <> 1)
    BEGIN
        SELECT RAISE(Fail,"Contrainte violée T9");
    END; \

CREATE TRIGGER C1 --EpreuveAppartient(Id) C Epreuve(Id)
    BEFORE INSERT
        ON EpreuveAppartient
        WHEN (NOT EXISTS(SELECT Id FROM Epreuve WHERE Id = New.Id))
BEGIN
    SELECT RAISE(Fail, "Contrainte violée T4");
END; \

CREATE TRIGGER C2 --EquipeEngage(Id_Equipe) C Equipe(Id) et EquipeEngage(Id) C Sportifs(Id)
    BEFORE INSERT
        ON EquipeEngage
        WHEN (NOT EXISTS(SELECT Id FROM Equipe WHERE Id = New.Id_Equipe) or
        NOT EXISTS(SELECT Id FROM Sportifs WHERE Id = New.Id))
BEGIN
    SELECT RAISE(Fail, "Contrainte violée T5");
END; \

CREATE TRIGGER C3 --EquipeParticipe(Id_Equipe) C Equipe(Id) et EquipeParticipe(Id_Epreuve) C Epreuve(Id)
    BEFORE INSERT
        ON EquipeParticipe
        WHEN (NOT EXISTS(SELECT Id FROM Equipe WHERE Id = New.Id_Equipe) or
        NOT EXISTS(SELECT Id FROM Epreuve WHERE Id = New.Id_Epreuve))
BEGIN
    SELECT RAISE(Fail, "Contrainte violée T6");
END; \

CREATE TRIGGER C4 --SportifsParticipe(Id_Sportifs) C Sportifs(Id) et SportifsParticipe(Id_Epreuve) C Epreuve(Id)
    BEFORE INSERT
        ON SportifsParticipe
        WHEN (NOT EXISTS(SELECT Id FROM Sportifs WHERE Id = New.Id_Sportifs) or
        NOT EXISTS(SELECT Id FROM Epreuve WHERE Id = New.Id_Epreuve))
BEGIN
    SELECT RAISE(Fail, "Contrainte violée T7");
END; \

CREATE TRIGGER DEL_EQUIPE
    BEFORE DELETE
        ON EquipeEngage
        WHEN ((SELECT Count(*)
              FROM EquipeEngage
              WHERE OLD.IdEquipe = IdEquipe) = 2)
BEGIN
    SELECT RAISE(Fail, "Contrainte violée");
END; CREATE TRIGGER UneSeuleMedaille --UneSeuleMedaille
    BEFORE INSERT
        ON LesResultats
        WHEN New.gold = NEW.silver OR NEW.gold = NEW.bronze OR NEW.silver = NEW.bronze
BEGIN
    SELECT RAISE(Fail, "Une participant ne peut gagner qu'une seule médaille");
END; \