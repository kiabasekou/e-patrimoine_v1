from django.db import models

# ----------- CATEGORISATION -----------
class Categorie(models.Model):
    TYPE_CHOICES = [
        ('immobilier', 'Bien Immobilier'),
        ('mobilier', 'Bien Mobilier'),
    ]
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.get_type_display()})"

class SousCategorie(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='sous_categories')
    nom = models.CharField(max_length=100)
    code = models.SlugField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        help_text="Code système unique (ex: 'ambulance', 'serveur')"
    )

    def __str__(self):
        return f"{self.nom} – {self.categorie.nom}"


# ----------- ENTITÉ -----------
class Entite(models.Model):
    nom = models.CharField(max_length=100)
    responsable = models.CharField(max_length=100)
    commune = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nom

    @property
    def departement(self):
        return self.commune.departement if self.commune else None

    @property
    def province(self):
        return self.commune.departement.province if self.commune else None



# ----------- HISTORIQUE -----------
class HistoriqueValeur(models.Model):
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE, related_name='historiques')
    date = models.DateField()
    valeur = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.bien.nom} - {self.valeur} au {self.date}"

