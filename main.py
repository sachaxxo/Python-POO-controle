from models.client import Client
from models.vehicule import Vehicule


def main() -> None:
    c = Client("C001", "Dupont", "Jean", "jean@mail.com", "0600000000", "Tours")
    v = Vehicule("V001", "Peugeot", "208", 4, 12000, "2020-05-10")

    print(c)
    print(v)


if __name__ == "__main__":
    main()

