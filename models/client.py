class Client:
    """Représente un client de l'agence de location."""

    def __init__(self, id_client: str, nom: str, prenom: str,
                 mail: str, telephone: str, adresse: str) -> None:
        self.id_client = id_client
        self.nom = nom
        self.prenom = prenom
        self.mail = mail
        self.telephone = telephone
        self.adresse = adresse

    def __str__(self) -> str:
        return f"{self.id_client} - {self.prenom} {self.nom}"
