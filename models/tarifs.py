class TarifsManager:
    """
    Gestionnaire des tarifs.

    TARIFS : {cylindree: {forfait_km: (cout_journalier, prix_km_supp)}}
    forfait_km peut être 100/200/300 (int) ou "+300" (str).
    """

    TARIFS: dict[int, dict[int | str, tuple[float, float]]] = {
        4: {
            100: (35.00, 0.25),
            200: (50.00, 0.20),
            300: (65.00, 0.15),
            "+300": (80.00, 0.10),
        },
        5: {
            100: (45.00, 0.30),
            200: (60.00, 0.25),
            300: (75.00, 0.20),
            "+300": (95.00, 0.15),
        },
        6: {
            100: (60.00, 0.40),
            200: (80.00, 0.35),
            300: (100.00, 0.30),
            "+300": (120.00, 0.25),
        },
    }

    @classmethod
    def obtenir_tarif(cls, cylindree: int, forfait_km: int | str) -> tuple[float, float]:
        """
        Renvoie (cout_journalier, prix_km_supp) selon cylindree et forfait_km.

        Raises:
            ValueError si cylindree ou forfait_km est invalide.
        """
        if cylindree not in cls.TARIFS:
            raise ValueError(f"Cylindrée invalide: {cylindree} (attendu 4, 5 ou 6)")

        # Normalisation du forfait
        if isinstance(forfait_km, str):
            forfait_normalise: int | str = forfait_km.strip()
        else:
            forfait_normalise = int(forfait_km)

        if forfait_normalise not in cls.TARIFS[cylindree]:
            raise ValueError("Forfait invalide (attendu 100, 200, 300 ou +300)")

        return cls.TARIFS[cylindree][forfait_normalise]

    @classmethod
    def afficher_grille(cls) -> None:
        """Affiche la grille tarifaire formatée."""
        print("=" * 70)
        print("GRILLE TARIFAIRE")
        print("=" * 70)
        print(f"{'Cylindrée':<12} {'Forfait':<8} {'Coût/jour':<10} {'Prix km supp.':<12}")
        print("-" * 70)

        for cylindree in (4, 5, 6):
            for forfait in (100, 200, 300, "+300"):
                cout_jour, prix_km = cls.TARIFS[cylindree][forfait]
                lib_cyl = f"{cylindree} cylindres"
                print(
                    f"{lib_cyl:<12} {str(forfait):<8} {cout_jour:>6.2f}€   {prix_km:>5.2f}€/km"
                )
            print("-" * 70)
