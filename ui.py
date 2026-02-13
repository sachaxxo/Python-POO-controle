from models.client import Client
from models.vehicule import Vehicule
from models.reservation import Reservation
from models.tarifs import TarifsManager

from data_manager import (
    generer_id_reservation,
    sauvegarder_reservation,
    filtrer_reservations_par_client,
)


def afficher_menu() -> str:
    print("\n" + "=" * 60)
    print("SYSTÈME DE LOCATION DE VÉHICULES")
    print("=" * 60)
    print("1. Afficher les clients")
    print("2. Afficher les véhicules")
    print("3. Créer une réservation")
    print("4. Afficher la grille tarifaire")
    print("5. Afficher toutes les réservations")
    print("6. Afficher les réservations d'un client")
    print("7. Quitter")
    print("=" * 60)
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


def _trouver_client(clients: list[Client], id_client: str) -> Client | None:
    for c in clients:
        if c.id_client == id_client:
            return c
    return None


def _trouver_vehicule(vehicules: list[Vehicule], id_vehicule: str) -> Vehicule | None:
    for v in vehicules:
        if v.id_vehicule == id_vehicule:
            return v
    return None


def afficher_reservations(reservations: list[Reservation]) -> None:
    print("\n" + "=" * 70)
    print("LISTE DES RÉSERVATIONS")
    print("=" * 70)
    if not reservations:
        print("Aucune réservation.")
        print("=" * 70)
        return

    for r in reservations:
        print(
            f"{r.id_reservation} | client {r.id_client} | vehicule {r.id_vehicule} | "
            f"{r.date_depart} -> {r.date_retour} | forfait {r.forfait_km} | "
            f"cout estimé {r.cout_estime:.2f}€"
        )
    print("=" * 70)


def afficher_reservations_client(reservations: list[Reservation], id_client: str) -> None:
    res_client = filtrer_reservations_par_client(reservations, id_client)
    print("\n" + "=" * 70)
    print(f"RÉSERVATIONS DU CLIENT {id_client}")
    print("=" * 70)
    if not res_client:
        print("Aucune réservation pour ce client.")
        print("=" * 70)
        return

    for r in res_client:
        print(
            f"{r.id_reservation} | vehicule {r.id_vehicule} | "
            f"{r.date_depart} -> {r.date_retour} | forfait {r.forfait_km} | "
            f"cout estimé {r.cout_estime:.2f}€"
        )
    print("=" * 70)


def demander_reservation(
    clients: list[Client],
    vehicules: list[Vehicule],
    reservations: list[Reservation],
) -> Reservation | None:
    print("\n" + "=" * 60)
    print("CRÉER UNE NOUVELLE RÉSERVATION")
    print("=" * 60)

    print("Clients disponibles :")
    for c in clients:
        print(f"- {c.id_client} - {c.prenom} {c.nom} ({c.mail})")
    id_client = input("ID du client : ").strip()

    client = _trouver_client(clients, id_client)
    if client is None:
        print("✗ ID client introuvable.")
        return None

    print("Véhicules disponibles :")
    for v in vehicules:
        print(f"- {v.id_vehicule} - {v.marque} {v.modele} ({v.cylindree} cyl. {int(v.kilometrage_actuel)} km)")
    id_vehicule = input("ID du véhicule : ").strip()

    vehicule = _trouver_vehicule(vehicules, id_vehicule)
    if vehicule is None:
        print("✗ ID véhicule introuvable.")
        return None

    date_depart = input("Date de départ (AAAA-MM-JJ) : ").strip()
    date_retour = input("Date de retour (AAAA-MM-JJ) : ").strip()

    print("Forfaits disponibles : 100, 200, 300, +300")
    forfait_str = input("Forfait kilométrique : ").strip()

    if forfait_str in ("100", "200", "300"):
        forfait_km = int(forfait_str)
    elif forfait_str == "+300":
        forfait_km = "+300"
    else:
        print("✗ Forfait invalide.")
        return None

    cout_journalier, prix_km_supp = TarifsManager.obtenir_tarif(vehicule.cylindree, forfait_km)
    id_reservation = generer_id_reservation(reservations)

    reservation = Reservation(
        id_reservation=id_reservation,
        id_client=client.id_client,
        id_vehicule=vehicule.id_vehicule,
        date_depart=date_depart,
        date_retour=date_retour,
        forfait_km=forfait_km,
        cout_journalier=cout_journalier,
        prix_km_supp=prix_km_supp,
    )

    print("\n" + "=" * 60)
    print("RÉCAPITULATIF DE LA RÉSERVATION")
    print("=" * 60)
    print(f"Réservation {reservation.id_reservation}")
    print(f"Client: {reservation.id_client}")
    print(f"Véhicule: {reservation.id_vehicule}")
    print(f"Du {reservation.date_depart} au {reservation.date_retour}")
    print(f"Forfait: {reservation.forfait_km} km")
    print(f"Coût journalier: {reservation.cout_journalier}€")
    print(f"Prix km supp.: {reservation.prix_km_supp}€/km")
    print(f"Coût estimé: {reservation.cout_estime:.2f}€")
    print("=" * 60)

    rep = input("Sauvegarder cette réservation ? (o/n) : ").strip().lower()
    if rep == "o":
        sauvegarder_reservation(reservation)
        reservations.append(reservation)
        print("✓ Réservation sauvegardée dans reservations.json")
        print("✓ Réservation enregistrée avec succès !")
        return reservation

    print("Réservation annulée.")
    return None


def boucle_menu(
    clients: list[Client],
    vehicules: list[Vehicule],
    reservations: list[Reservation],
) -> None:
    while True:
        choix = afficher_menu()

        if choix == "1":
            afficher_clients(clients)
        elif choix == "2":
            afficher_vehicules(vehicules)
        elif choix == "3":
            demander_reservation(clients, vehicules, reservations)
        elif choix == "4":
            TarifsManager.afficher_grille()
        elif choix == "5":
            afficher_reservations(reservations)
        elif choix == "6":
            id_client = input("ID du client : ").strip()
            afficher_reservations_client(reservations, id_client)
        elif choix == "7":
            print("Au revoir !")
            break
        else:
            print("Choix invalide ou fonctionnalité pas encore implémentée.")
