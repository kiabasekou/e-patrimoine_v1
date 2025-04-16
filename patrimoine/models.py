from django.db import models
from .profils import ProfilVehicule, ProfilImmeuble, ProfilInformatique, ProfilEquipementMedical

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
        null=True,  # 👈 ajouté pour éviter l’erreur au moment de la migration
        blank=True,
        help_text="Code système unique (ex: 'ambulance', 'serveur')"
    )
    
    def __str__(self):
        return f"{self.nom} – {self.categorie.nom}"


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
    def __str__(self):
        return f"{self.nom} ({self.departement.nom})"

class District(models.Model):
    nom = models.CharField(max_length=100)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nom} ({self.commune.nom})"

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

# ----------- BIEN -----------
class Bien(models.Model):
    nom = models.CharField(max_length=100)
    categorie = models.ForeignKey('Categorie', on_delete=models.PROTECT)
    sous_categorie = models.ForeignKey(SousCategorie, on_delete=models.PROTECT, null=True, blank=True)
    entite = models.ForeignKey('Entite', on_delete=models.CASCADE)
    valeur_initiale = models.DecimalField(max_digits=12, decimal_places=2)
    date_acquisition = models.DateField()
    description = models.TextField(blank=True)
    numero_serie = models.CharField(max_length=100, blank=True, null=True)
    duree_amortissement = models.IntegerField(blank=True, null=True)
    superficie = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    annee_construction = models.PositiveIntegerField(null=True, blank=True)
    statut_juridique = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nom

    @property
    def responsable_actuel(self):
        return self.responsabilites.filter(type_affectation='permanent').first()

# ----------- HISTORIQUE -----------
class HistoriqueValeur(models.Model):
    bien = models.ForeignKey('Bien', on_delete=models.CASCADE, related_name='historiques')
    date = models.DateField()
    valeur = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.bien.nom} - {self.valeur} au {self.date}"

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

    bien = models.ForeignKey('Bien', on_delete=models.CASCADE, related_name='responsabilites')
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

# ----------- PROFILS TECHNIQUES -----------
# Déplacés dans profils.py :
# - ProfilVehicule
# - ProfilImmeuble
# - ProfilInformatique
# - ProfilEquipementMedical
