import json
from pathlib import Path
from typing import Any

from models.client import Client
from models.vehicule import Vehicule


# On cherche les JSON à la racine du projet (à côté de data_manager.py)
BASE_DIR = Path(__file__).resolve().parent
CLIENTS_FILE = BASE_DIR / "clients.json"
VEHICULES_FILE = BASE_DIR / "vehicules.json"


def _lire_json(path: Path) -> Any:
    """Lit un fichier JSON et renvoie l'objet Python correspondant (list/dict)."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def charger_clients(path: Path | str = CLIENTS_FILE) -> list[Client]:
    """
    Charge la liste des clients depuis un fichier JSON (clients.json par défaut).
    Renvoie une liste d'objets Client.
    """
    path = Path(path)
    data = _lire_json(path)

    clients: list[Client] = []
    for item in data:
        clients.append(Client.from_dict(item))
    return clients


def charger_vehicules(path: Path | str = VEHICULES_FILE) -> list[Vehicule]:
    """
    Charge la liste des véhicules depuis un fichier JSON (vehicules.json par défaut).
    Renvoie une liste d'objets Vehicule.
    """
    path = Path(path)
    data = _lire_json(path)

    vehicules: list[Vehicule] = []
    for item in data:
        vehicules.append(Vehicule.from_dict(item))
    return vehicules
