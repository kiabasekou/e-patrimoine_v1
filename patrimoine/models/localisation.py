from django.db import models
# ----------- LOCALISATION -----------
class Province(models.Model):
    nom = models.CharField(max_length=100)
    

    def __str__(self):
        return self.nom

class Departement(models.Model):
    nom = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} ({self.province.nom})"

class Commune(models.Model):
    nom = models.CharField(max_length=100)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # lien avec Département / Province

    def __str__(self):
        return self.nom


class District(models.Model):
    nom = models.CharField(max_length=100)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} ({self.commune.nom})"
