from data_manager import charger_clients, charger_vehicules
from ui import boucle_menu


def main() -> None:
    clients = charger_clients()
    vehicules = charger_vehicules()
    boucle_menu(clients, vehicules)


if __name__ == "__main__":
    main()
