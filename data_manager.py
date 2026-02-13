import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from models.client import Client
from models.vehicule import Vehicule
from models.reservation import Reservation


BASE_DIR = Path(__file__).resolve().parent

CLIENTS_FILE = BASE_DIR / "clients.json"
VEHICULES_FILE = BASE_DIR / "vehicules.json"
RESERVATIONS_FILE = BASE_DIR / "reservations.json"


def _message_erreur(prefix: str, path: Path, details: str) -> None:
    print(f"✗ {prefix} : {path.name}")
    print(f"  → {details}")


def _lire_json(path: Path) -> Any:
    """
    Lit un fichier JSON et renvoie l'objet Python correspondant.
    En cas d'erreur (fichier manquant, JSON invalide), renvoie [] (par défaut).
    """
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        _message_erreur("Fichier introuvable", path, "Vérifiez qu'il est bien présent à la racine du projet.")
        return []
    except JSONDecodeError as e:
        _message_erreur("JSON invalide", path, f"Erreur de parsing à la ligne {e.lineno}, colonne {e.colno}.")
        return []
    except OSError as e:
        _message_erreur("Erreur d'accès au fichier", path, str(e))
        return []


def _ecrire_json(path: Path, data: Any) -> None:
    """
    Écrit des données dans un fichier JSON.
    En cas d'erreur d'écriture, affiche un message clair.
    """
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        _message_erreur("Impossible d'écrire dans le fichier", path, str(e))


def charger_clients(path: Path | str = CLIENTS_FILE) -> list[Client]:
    path = Path(path)
    data = _lire_json(path)

    if not isinstance(data, list):
        _message_erreur("Format JSON invalide", path, "Attendu : une liste de clients.")
        return []

    clients: list[Client] = []
    for item in data:
        try:
            clients.append(Client.from_dict(item))
        except (KeyError, TypeError, ValueError) as e:
            _message_erreur("Entrée client invalide", path, f"{e} (entrée ignorée)")
    return clients


def charger_vehicules(path: Path | str = VEHICULES_FILE) -> list[Vehicule]:
    path = Path(path)
    data = _lire_json(path)

    if not isinstance(data, list):
        _message_erreur("Format JSON invalide", path, "Attendu : une liste de véhicules.")
        return []

    vehicules: list[Vehicule] = []
    for item in data:
        try:
            vehicules.append(Vehicule.from_dict(item))
        except (KeyError, TypeError, ValueError) as e:
            _message_erreur("Entrée véhicule invalide", path, f"{e} (entrée ignorée)")
    return vehicules


def charger_reservations(path: Path | str = RESERVATIONS_FILE) -> list[Reservation]:
    path = Path(path)
    data = _lire_json(path)

    if not isinstance(data, list):
        _message_erreur("Format JSON invalide", path, "Attendu : une liste de réservations.")
        return []

    reservations: list[Reservation] = []
    for item in data:
        try:
            reservations.append(Reservation.from_dict(item))
        except (KeyError, TypeError, ValueError) as e:
            _message_erreur("Entrée réservation invalide", path, f"{e} (entrée ignorée)")
    return reservations


def generer_id_reservation(reservations: list[Reservation]) -> str:
    max_num = 0
    for r in reservations:
        try:
            num = int(str(r.id_reservation)[1:])
            max_num = max(max_num, num)
        except (ValueError, TypeError, IndexError):
            continue
    return f"R{max_num + 1:04d}"


def sauvegarder_reservation(reservation: Reservation, path: Path | str = RESERVATIONS_FILE) -> None:
    path = Path(path)

    reservations = charger_reservations(path)
    reservations.append(reservation)

    data = [r.to_dict() for r in reservations]
    _ecrire_json(path, data)


def filtrer_reservations_par_client(reservations: list[Reservation], id_client: str) -> list[Reservation]:
    return [r for r in reservations if r.id_client == id_client]
