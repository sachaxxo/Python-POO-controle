from data_manager import charger_clients, charger_vehicules, charger_reservations
from ui import boucle_menu


def main() -> None:
    clients = charger_clients()
    vehicules = charger_vehicules()
    reservations = charger_reservations()
    boucle_menu(clients, vehicules, reservations)


if __name__ == "__main__":
    main()
