class TarifsManager:
    """
    Gestionnaire des tarifs.

    TARIFS : dict
        {cylindree: {forfait_km: (cout_journalier, prix_km_supp)}}
    """

    # Grille partielle (complétée à l'étape 6)
    TARIFS = {
        4: {
            100: (35.00, 0.25),
            200: (50.00, 0.20),
        },
        5: {
            100: (45.00, 0.30),
        },
        6: {
            100: (60.00, 0.40),
        },
    }

    @classmethod
    def obtenir_tarif(cls, cylindree: int, forfait_km):
        """
        Doit renvoyer (cout_journalier, prix_km_supp) selon cylindree et forfait_km.
        Implémentation complète attendue à l'étape 6.
        """
        raise NotImplementedError("À implémenter à l'étape 6 (tarifs complets).")

    @classmethod
    def afficher_grille(cls) -> None:
        """
        Doit afficher la grille tarifaire formatée.
        Implémentation complète attendue à l'étape 6.
        """
        raise NotImplementedError("À implémenter à l'étape 6 (affichage complet).")
