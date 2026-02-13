from datetime import datetime

from models.client import Client
from models.vehicule import Vehicule
from models.reservation import Reservation
from models.tarifs import TarifsManager

from data_manager import (
    generer_id_reservation,
    sauvegarder_reservation,
    filtrer_reservations_par_client,
)


def pause() -> None:
    """Pause console pour laisser le temps de lire l'affichage."""
    input("\nAppuyez sur Entrée pour continuer...")


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
        print(
            f"{v.id_vehicule} - {v.marque} {v.modele} "
            f"({v.cylindree} cyl., {int(v.kilometrage_actuel)} km)"
        )
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


def _parse_date(date_str: str):
    """Retourne une date (datetime.date) ou None si format invalide."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


def _normaliser_forfait(forfait_str: str):
    """Retourne 100/200/300 (int) ou '+300' (str) ou None si invalide."""
    if forfait_str in ("100", "200", "300"):
        return int(forfait_str)
    if forfait_str == "+300":
        return "+300"
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
            f"{r.id_reservation} | Client: {r.id_client} | Véhicule: {r.id_vehicule} | "
            f"{r.date_depart} ➔ {r.date_retour} | Forfait: {r.forfait_km} km | "
            f"Coût estimé: {r.cout_estime:.2f}€"
        )
    print("=" * 70)


def afficher_reservations_client(clients: list[Client], reservations: list[Reservation]) -> None:
    id_client = input("ID du client à rechercher : ").strip()

    if _trouver_client(clients, id_client) is None:
        print("✗ ID client inexistant.")
        return

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
            f"{r.id_reservation} | Véhicule: {r.id_vehicule} | "
            f"{r.date_depart} ➔ {r.date_retour} | Forfait: {r.forfait_km} km | "
            f"Coût estimé: {r.cout_estime:.2f}€"
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
        print("✗ ID client inexistant.")
        return None

    print("Véhicules disponibles :")
    for v in vehicules:
        print(f"- {v.id_vehicule} - {v.marque} {v.modele} ({v.cylindree} cyl. {int(v.kilometrage_actuel)} km)")
    id_vehicule = input("ID du véhicule : ").strip()

    vehicule = _trouver_vehicule(vehicules, id_vehicule)
    if vehicule is None:
        print("✗ ID véhicule inexistant.")
        return None

    date_depart_str = input("Date de départ (AAAA-MM-JJ) : ").strip()
    date_retour_str = input("Date de retour (AAAA-MM-JJ) : ").strip()

    d_depart = _parse_date(date_depart_str)
    d_retour = _parse_date(date_retour_str)

    if d_depart is None:
        print("✗ Date de départ invalide (format attendu : AAAA-MM-JJ).")
        return None
    if d_retour is None:
        print("✗ Date de retour invalide (format attendu : AAAA-MM-JJ).")
        return None

    if d_retour < d_depart:
        print("✗ Dates incohérentes : la date de retour est avant la date de départ.")
        return None

    print("Forfaits disponibles : 100, 200, 300, +300")
    forfait_str = input("Forfait kilométrique : ").strip()
    forfait_km = _normaliser_forfait(forfait_str)

    if forfait_km is None:
        print("✗ Forfait kilométrique invalide (attendu : 100, 200, 300 ou +300).")
        return None

    try:
        cout_journalier, prix_km_supp = TarifsManager.obtenir_tarif(vehicule.cylindree, forfait_km)
    except ValueError as e:
        print(f"✗ Tarifs introuvables : {e}")
        return None

    id_reservation = generer_id_reservation(reservations)

    reservation = Reservation(
        id_reservation=id_reservation,
        id_client=client.id_client,
        id_vehicule=vehicule.id_vehicule,
        date_depart=date_depart_str,
        date_retour=date_retour_str,
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
    if rep not in ("o", "n"):
        print("✗ Réponse invalide (attendu : o ou n). Réservation annulée.")
        return None

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
            pause()
        elif choix == "2":
            afficher_vehicules(vehicules)
            pause()
        elif choix == "3":
            demander_reservation(clients, vehicules, reservations)
            pause()
        elif choix == "4":
            TarifsManager.afficher_grille()
            pause()
        elif choix == "5":
            afficher_reservations(reservations)
            pause()
        elif choix == "6":
            afficher_reservations_client(clients, reservations)
            pause()
        elif choix == "7":
            print("Au revoir !")
            break
        else:
            print("Choix invalide, réessayez.")
            pause()
