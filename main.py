from models.client import Client
from models.vehicule import Vehicule

def main() -> None:
    c = Client("C001", "Dupont", "Jean", "jean@mail.com", "0600", "Tours")
    d = c.to_dict()
    c2 = Client.from_dict(d)
    print(c2)

    v = Vehicule("V001", "Peugeot", "208", 4, 12000, "2020-05-10")
    v2 = Vehicule.from_dict(v.to_dict())
    print(v2)

if __name__ == "__main__":
    main()

