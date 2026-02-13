from __future__ import annotations

from datetime import datetime


class Reservation:
    """
    Représente une réservation entre un client et un véhicule.

    - Le coût estimé est calculé automatiquement :
      cout_estime = cout_journalier * nb_jours (minimum 1 jour).
    """

    def __init__(
        self,
        id_reservation: str,
        id_client: str,
        id_vehicule: str,
        date_depart: str,
        date_retour: str,
        forfait_km: int | str,
        cout_journalier: float,
        prix_km_supp: float,
    ) -> None:
        self.id_reservation = id_reservation
        self.id_client = id_client
        self.id_vehicule = id_vehicule
        self.date_depart = date_depart
        self.date_retour = date_retour
        self.forfait_km = forfait_km
        self.cout_journalier = float(cout_journalier)
        self.prix_km_supp = float(prix_km_supp)

        # Calcul automatique (étape 11)
        self.cout_estime = self._calculer_cout_estime()

    def _calculer_cout_estime(self) -> float:
        """
        Calcule le coût estimé :
        - nb_jours = (date_retour - date_depart) en jours
        - minimum 1 jour
        - cout_estime = cout_journalier * nb_jours
        """
        d1 = datetime.strptime(self.date_depart, "%Y-%m-%d").date()
        d2 = datetime.strptime(self.date_retour, "%Y-%m-%d").date()

        nb_jours = (d2 - d1).days
        if nb_jours < 1:
            nb_jours = 1

        return self.cout_journalier * nb_jours

    def __str__(self) -> str:
        """Affichage lisible de la réservation."""
        return (
            f"{self.id_reservation} | Client: {self.id_client} | Véhicule: {self.id_vehicule} | "
            f"{self.date_depart} ➔ {self.date_retour} | Forfait: {self.forfait_km} km | "
            f"Coût estimé: {self.cout_estime:.2f}€"
        )

    def to_dict(self) -> dict:
        """Sérialise la réservation en dict compatible JSON."""
        return {
            "id_reservation": self.id_reservation,
            "id_client": self.id_client,
            "id_vehicule": self.id_vehicule,
            "date_depart": self.date_depart,
            "date_retour": self.date_retour,
            "forfait_km": self.forfait_km,
            "cout_journalier": self.cout_journalier,
            "prix_km_supp": self.prix_km_supp,
            "cout_estime": self.cout_estime,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Reservation":
        """
        Reconstruit une réservation depuis un dict (JSON).

        Remarque : même si le JSON contient cout_estime, on recalcule automatiquement
        via __init__ (c’est voulu).
        """
        return cls(
            id_reservation=data["id_reservation"],
            id_client=data["id_client"],
            id_vehicule=data["id_vehicule"],
            date_depart=data["date_depart"],
            date_retour=data["date_retour"],
            forfait_km=data["forfait_km"],
            cout_journalier=float(data["cout_journalier"]),
            prix_km_supp=float(data["prix_km_supp"]),
        )
