class Client:
    """Client de l’agence (identité + contact)."""

    def __init__(
        self,
        id_client: str,
        nom: str,
        prenom: str,
        mail: str,
        telephone: str,
        adresse: str,
    ) -> None:
        self.id_client = id_client
        self.nom = nom
        self.prenom = prenom
        self.mail = mail
        self.telephone = telephone
        self.adresse = adresse

    def __str__(self) -> str:
        """Affichage court du client."""
        return f"{self.id_client} - {self.prenom} {self.nom}"

    def to_dict(self) -> dict:
        """Sérialise l’objet en dictionnaire compatible JSON."""
        return {
            "id_client": self.id_client,
            "nom": self.nom,
            "prenom": self.prenom,
            "mail": self.mail,
            "telephone": self.telephone,
            "adresse": self.adresse,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Client":
        """Reconstruit un Client depuis un dictionnaire (JSON)."""
        return cls(
            id_client=data["id_client"],
            nom=data["nom"],
            prenom=data["prenom"],
            mail=data["mail"],
            telephone=data["telephone"],
            adresse=data["adresse"],
        )
