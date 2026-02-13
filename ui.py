def afficher_menu() -> str:
    """Affiche le menu principal et renvoie le choix utilisateur."""
    print("\n===== MENU PRINCIPAL =====")
    print("1. Afficher les clients")
    print("2. Afficher les véhicules")
    print("0. Quitter")

    choix = input("Votre choix : ").strip()
    return choix


def boucle_menu() -> None:
    """Boucle principale du menu."""
    while True:
        choix = afficher_menu()

        if choix == "1":
            print("Fonctionnalité bientôt disponible : afficher les clients")
        elif choix == "2":
            print("Fonctionnalité bientôt disponible : afficher les véhicules")
        elif choix == "0":
            print("Au revoir !")
            break
        else:
            print("Choix invalide, réessayez.")
