from django.db import models
# ----------- BIEN -----------
class Bien(models.Model):
    nom = models.CharField(max_length=100)
    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT)
    sous_categorie = models.ForeignKey(SousCategorie, on_delete=models.PROTECT, null=True, blank=True)
    entite = models.ForeignKey(Entite, on_delete=models.CASCADE)
    commune = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True, blank=True)  # 🔁 Ajout ici
    valeur_initiale = models.DecimalField(max_digits=12, decimal_places=2)
    date_acquisition = models.DateField()
    description = models.TextField(blank=True)
    numero_serie = models.CharField(max_length=100, blank=True, null=True)
    duree_amortissement = models.IntegerField(blank=True, null=True)
    superficie = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    annee_construction = models.PositiveIntegerField(null=True, blank=True)
    statut_juridique = models.CharField(max_length=100, blank=True)
    justificatif = models.FileField(upload_to='justificatifs/', null=True, blank=True)

    def __str__(self):
        return self.nom

    @property
    def responsable_actuel(self):
        return self.responsabilites.filter(type_affectation='permanent').first()