from django.db import models
# ----------- RESPONSABLES -----------
class ResponsableBien(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    matricule = models.CharField(max_length=50, unique=True)
    fonction = models.CharField(max_length=100)
    categorie = models.CharField(max_length=50)
    corps = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom} – {self.fonction}"

class BienResponsabilite(models.Model):
    AFFECTATION_CHOICES = [
        ('permanent', 'Permanent'),
        ('temporaire', 'Temporaire'),
    ]

    bien = models.ForeignKey(Bien, on_delete=models.CASCADE, related_name='responsabilites')
    responsable = models.ForeignKey(ResponsableBien, on_delete=models.CASCADE)
    date_affectation = models.DateField()
    type_affectation = models.CharField(max_length=20, choices=AFFECTATION_CHOICES)
    motif = models.TextField(blank=True)

    numero_permis = models.CharField(max_length=50, blank=True, null=True)
    date_permis = models.DateField(blank=True, null=True)
    categorie_permis = models.CharField(max_length=10, blank=True, null=True)
    composition_foyer = models.TextField(blank=True, null=True)
    conditions_occupation = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    formations = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date_affectation']
        verbose_name = "Responsabilité d’un bien"
        verbose_name_plural = "Responsabilités des biens"

    def __str__(self):
        return f"{self.responsable} – {self.bien} ({self.date_affectation})"