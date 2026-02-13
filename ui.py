from models.client import Client
from models.vehicule import Vehicule


def afficher_menu() -> str:
    print("\n===== MENU PRINCIPAL =====")
    print("1. Afficher les clients")
    print("2. Afficher les véhicules")
    print("0. Quitter")
    return input("Votre choix : ").strip()


def afficher_clients(clients: list[Client]) -> None:
    print("\n" + "=" * 60)
    print("LISTE DES CLIENTS")
    print("=" * 60)
    for c in clients:
        print(f"{c.id_client} - {c.prenom} {c.nom} ({c.mail})")
    print("=" * 60)


def afficher_vehicules(vehicules: list[Vehicule]) -> None:
    print("\n" + "=" * 60)
    print("LISTE DES VÉHICULES")
    print("=" * 60)
    for v in vehicules:
        print(f"{v.id_vehicule} - {v.marque} {v.modele} ({v.cylindree} cyl., {int(v.kilometrage_actuel)} km)")
    print("=" * 60)


def boucle_menu(clients: list[Client], vehicules: list[Vehicule]) -> None:
    while True:
        choix = afficher_menu()

        if choix == "1":
            afficher_clients(clients)
        elif choix == "2":
            afficher_vehicules(vehicules)
        elif choix == "0":
            print("Au revoir !")
            break
        else:
            print("Choix invalide, réessayez.")
