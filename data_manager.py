import json
from pathlib import Path
from typing import Any

from models.client import Client
from models.vehicule import Vehicule
from models.reservation import Reservation


BASE_DIR = Path(__file__).resolve().parent

CLIENTS_FILE = BASE_DIR / "clients.json"
VEHICULES_FILE = BASE_DIR / "vehicules.json"
RESERVATIONS_FILE = BASE_DIR / "reservations.json"


def _lire_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _ecrire_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def charger_clients(path: Path | str = CLIENTS_FILE) -> list[Client]:
    path = Path(path)
    data = _lire_json(path)
    return [Client.from_dict(item) for item in data]


def charger_vehicules(path: Path | str = VEHICULES_FILE) -> list[Vehicule]:
    path = Path(path)
    data = _lire_json(path)
    return [Vehicule.from_dict(item) for item in data]


def charger_reservations(path: Path | str = RESERVATIONS_FILE) -> list[Reservation]:
    """
    Charge la liste des réservations depuis reservations.json.
    """
    path = Path(path)
    data = _lire_json(path)
    return [Reservation.from_dict(item) for item in data]


def generer_id_reservation(reservations: list[Reservation]) -> str:
    """
    Génère un nouvel ID de réservation au format R0001, R0002, ...
    (en se basant sur la liste des réservations existantes).
    """
    max_num = 0
    for r in reservations:
        # r.id_reservation attendu sous forme "R0001"
        try:
            num = int(r.id_reservation[1:])
            max_num = max(max_num, num)
        except (ValueError, TypeError, IndexError):
            # Si une réservation a un format d'ID bizarre, on l'ignore
            continue

    prochain = max_num + 1
    return f"R{prochain:04d}"


def sauvegarder_reservation(
    reservation: Reservation,
    path: Path | str = RESERVATIONS_FILE
) -> None:
    """
    Ajoute une réservation dans reservations.json (append + réécriture du fichier).
    """
    path = Path(path)

    reservations = charger_reservations(path)
    reservations.append(reservation)

    data = [r.to_dict() for r in reservations]
    _ecrire_json(path, data)


def filtrer_reservations_par_client(
    reservations: list[Reservation],
    id_client: str
) -> list[Reservation]:
    """
    Retourne les réservations correspondant à un client donné.
    """
    return [r for r in reservations if r.id_client == id_client]
