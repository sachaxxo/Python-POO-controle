from data_manager import charger_clients, charger_vehicules, charger_reservations
from ui import boucle_menu


def main() -> None:
    print("=" * 60)
    print("Chargement des données...")
    clients = charger_clients()
    vehicules = charger_vehicules()
    reservations = charger_reservations()
    print(f"✓ {len(clients)} client(s) chargé(s)")
    print(f"✓ {len(vehicules)} véhicule(s) chargé(s)")
    print("=" * 60)

    boucle_menu(clients, vehicules, reservations)


if __name__ == "__main__":
    main()
