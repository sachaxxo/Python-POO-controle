class Vehicule:
    """Représente un véhicule disponible à la location."""

    def __init__(self, id_vehicule: str, marque: str, modele: str,
                 cylindree: int, kilometrage_actuel: float,
                 date_mise_en_circulation: str) -> None:
        self.id_vehicule = id_vehicule
        self.marque = marque
        self.modele = modele
        self.cylindree = cylindree
        self.kilometrage_actuel = kilometrage_actuel
        self.date_mise_en_circulation = date_mise_en_circulation

    def __str__(self) -> str:
        return f"{self.id_vehicule} - {self.marque} {self.modele} ({self.cylindree} cyl)"

    def to_dict(self) -> dict:
        return {
            "id_vehicule": self.id_vehicule,
            "marque": self.marque,
            "modele": self.modele,
            "cylindree": self.cylindree,
            "kilometrage_actuel": self.kilometrage_actuel,
            "date_mise_en_circulation": self.date_mise_en_circulation
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id_vehicule=data["id_vehicule"],
            marque=data["marque"],
            modele=data["modele"],
            cylindree=int(data["cylindree"]),
            kilometrage_actuel=float(data["kilometrage_actuel"]),
            date_mise_en_circulation=data["date_mise_en_circulation"]
        )
