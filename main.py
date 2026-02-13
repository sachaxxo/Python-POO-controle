from models.tarifs import TarifsManager

def main() -> None:
    TarifsManager.afficher_grille()
    print(TarifsManager.obtenir_tarif(6, 200))   # doit renvoyer (80.0, 0.35)

if __name__ == "__main__":
    main()
