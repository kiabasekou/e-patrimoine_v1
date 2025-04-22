from django.db import models

# Profils techniques pour chaque type de Bien

class ProfilVehicule(models.Model):
    bien = models.OneToOneField('Bien', on_delete=models.CASCADE, related_name='profil_vehicule')
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    matricule = models.CharField(max_length=50, null=True, blank=True)
    numero_chassis = models.CharField(max_length=100, null=True, blank=True)
    date_fabrication = models.DateField(null=True, blank=True)
    date_acquisition = models.DateField(null=True, blank=True)
    date_derniere_maintenance = models.DateField(null=True, blank=True)
    prochaine_maintenance = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.matricule})"

class ProfilImmeuble(models.Model):
    bien = models.OneToOneField('Bien', on_delete=models.CASCADE, related_name='profil_immeuble')
    surface = models.DecimalField(max_digits=8, decimal_places=2)
    nb_etages = models.PositiveIntegerField()
    annee_construction = models.PositiveIntegerField()
    securite = models.CharField(max_length=255)

    def __str__(self):
        return f"Immeuble {self.bien.nom} - {self.surface} m²"

class ProfilInformatique(models.Model):
    STATUT_CHOICES = [
        ('en_service', 'En service'),
        ('en_maintenance', 'En maintenance'),
        ('hors_service', 'Hors service'),
        ('en_attente', 'En attente de déploiement'),
    ]
    TYPE_CHOICES = [
        ('ordinateur_fixe', 'Ordinateur fixe'),
        ('ordinateur_portable', 'Ordinateur portable'),
        ('serveur', 'Serveur'),
        ('imprimante', 'Imprimante'),
        ('scanner', 'Scanner'),
        ('photocopieur', 'Photocopieur'),
        ('reseau', 'Équipement réseau'),
        ('stockage', 'Solution de stockage'),
        ('autre', 'Autre'),
    ]

    bien = models.OneToOneField('Bien', on_delete=models.CASCADE, related_name='profil_informatique')
    type_equipement = models.CharField(max_length=50, choices=TYPE_CHOICES)
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100)
    date_fabrication = models.DateField(null=True, blank=True)
    processeur = models.CharField(max_length=100, blank=True)
    memoire_ram = models.CharField(max_length=50, blank=True)
    capacite_stockage = models.CharField(max_length=50, blank=True)
    carte_graphique = models.CharField(max_length=100, blank=True)
    spec_tech = models.TextField(blank=True)
    os = models.CharField(max_length=100, blank=True)
    version_os = models.CharField(max_length=50, blank=True)
    logiciels = models.TextField(blank=True)
    adresse_ip = models.GenericIPAddressField(null=True, blank=True)
    adresse_mac = models.CharField(max_length=17, blank=True)
    nom_reseau = models.CharField(max_length=100, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_service')
    date_derniere_maj = models.DateField(auto_now=True)
    date_derniere_maintenance = models.DateField(null=True, blank=True)
    prochaine_maintenance = models.DateField(null=True, blank=True)
    date_acquisition = models.DateField(null=True, blank=True)
    date_mise_service = models.DateField(null=True, blank=True)
    fin_garantie = models.DateField(null=True, blank=True)
    contrat_maintenance = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.get_type_equipement_display()} - {self.marque} {self.modele}"

class ProfilEquipementMedical(models.Model):
    CLASSE_RISQUE_CHOICES = [
        ('i', 'Classe I - Risque faible'),
        ('iia', 'Classe IIa - Risque modéré'),
        ('iib', 'Classe IIb - Risque élevé'),
        ('iii', 'Classe III - Risque critique'),
    ]
    STATUT_CHOICES = [
        ('actif', 'Actif - En service'),
        ('maintenance', 'En maintenance'),
        ('stockage', 'En stockage'),
        ('inutilisable', 'Hors service'),
        ('calibration', 'En calibration'),
    ]
    TYPE_CHOICES = [
        ('diagnostic', 'Diagnostic'),
        ('therapeutique', 'Thérapeutique'),
        ('laboratoire', 'Laboratoire'),
        ('monitoring', 'Surveillance'),
        ('imagerie', 'Imagerie'),
        ('chirurgical', 'Chirurgical'),
        ('sterilisation', 'Stérilisation'),
        ('autre', 'Autre'),
    ]

    bien = models.OneToOneField('Bien', on_delete=models.CASCADE, related_name='profil_equipement_medical')
    type_equipement = models.CharField(max_length=50, choices=TYPE_CHOICES)
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100)
    date_fabrication = models.DateField(null=True, blank=True)
    certification = models.CharField(max_length=100, blank=True)
    classe_risque = models.CharField(max_length=3, choices=CLASSE_RISQUE_CHOICES, blank=True)
    normes_applicables = models.TextField(blank=True)
    organisme_certification = models.CharField(max_length=100, blank=True)
    parametres_techniques = models.TextField(blank=True)
    source_energie = models.CharField(max_length=100, blank=True)
    consommation = models.CharField(max_length=50, blank=True)
    duree_vie = models.PositiveIntegerField(null=True, blank=True)
    date_installation = models.DateField(null=True, blank=True)
    date_derniere_maintenance = models.DateField(null=True, blank=True)
    frequence_maintenance = models.PositiveIntegerField(default=365)
    maintenance = models.TextField(blank=True)
    pieces = models.TextField(blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif')
    departement_utilisation = models.CharField(max_length=100, blank=True)
    utilisateurs_formes = models.TextField(blank=True)
    date_acquisition = models.DateField(null=True, blank=True)
    fin_garantie = models.DateField(null=True, blank=True)
    contrat_maintenance = models.CharField(max_length=100, blank=True)
    fournisseur_service = models.CharField(max_length=100, blank=True)
    contact_sav = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.get_type_equipement_display()} - {self.marque} {self.modele}" 

class ProfilMobilier(models.Model):
    bien = models.OneToOneField('Bien', on_delete=models.CASCADE, related_name='profil_mobilier')
    materiau = models.CharField(max_length=100)
    couleur = models.CharField(max_length=50)
    fabricant = models.CharField(max_length=100)
    annee_fabrication = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Mobilier {self.bien.nom} - {self.materiau} ({self.couleur})"

class ProfilTerrain(models.Model):
    bien = models.OneToOneField('Bien', on_delete=models.CASCADE, related_name='profil_terrain')
    superficie = models.DecimalField(max_digits=12, decimal_places=2)
    statut_juridique = models.CharField(max_length=255)
    usage = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Terrain {self.bien.nom} - {self.superficie} m²"

class ProfilConsommable(models.Model):
    bien = models.OneToOneField('Bien', on_delete=models.CASCADE, related_name='profil_consommable')
    quantite_initiale = models.PositiveIntegerField()
    unite = models.CharField(max_length=50)
    stock_securite = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Consommable {self.bien.nom} - {self.quantite_initiale} {self.unite}"
