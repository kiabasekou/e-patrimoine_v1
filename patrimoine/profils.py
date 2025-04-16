from django.db import models

class ProfilVehicule(models.Model):
    bien = models.OneToOneField('Bien', on_delete=models.CASCADE, related_name='profil_vehicule')
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    immatriculation = models.CharField(max_length=20)
    puissance = models.CharField(max_length=50)
    consommation = models.CharField(max_length=50)
    assurance = models.CharField(max_length=100)

class ProfilImmeuble(models.Model):
    bien = models.OneToOneField('Bien', on_delete=models.CASCADE, related_name='profil_immeuble')
    surface = models.DecimalField(max_digits=8, decimal_places=2)
    nb_etages = models.PositiveIntegerField()
    annee_construction = models.PositiveIntegerField()
    securite = models.CharField(max_length=255)

class ProfilInformatique(models.Model):
    STATUT_CHOICES = [
        ('EN_SERVICE', 'En service'),
        ('EN_MAINTENANCE', 'En maintenance'),
        ('HORS_SERVICE', 'Hors service'),
        ('EN_ATTENTE', 'En attente de déploiement'),
    ]

    TYPE_CHOICES = [
        ('ORDINATEUR_FIXE', 'Ordinateur fixe'),
        ('ORDINATEUR_PORTABLE', 'Ordinateur portable'),
        ('SERVEUR', 'Serveur'),
        ('IMPRIMANTE', 'Imprimante'),
        ('SCANNER', 'Scanner'),
        ('PHOTOCOPIEUR', 'Photocopieur'),
        ('RESEAU', 'Équipement réseau'),
        ('STOCKAGE', 'Solution de stockage'),
        ('AUTRE', 'Autre'),
    ]

    bien = models.OneToOneField('Bien', on_delete=models.CASCADE, related_name='profil_informatique')
    type_equipement = models.CharField(max_length=50, choices=TYPE_CHOICES)
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    numero_serie = models.CharField("Numéro de série", max_length=100)
    date_fabrication = models.DateField("Date de fabrication", null=True, blank=True)
    processeur = models.CharField(max_length=100, blank=True)
    memoire_ram = models.CharField("Mémoire RAM", max_length=50, blank=True)
    capacite_stockage = models.CharField("Capacité de stockage", max_length=50, blank=True)
    carte_graphique = models.CharField("Carte graphique", max_length=100, blank=True)
    spec_tech = models.TextField("Spécifications techniques additionnelles")
    os = models.CharField("Système d'exploitation", max_length=100, blank=True)
    version_os = models.CharField("Version OS", max_length=50, blank=True)
    logiciels = models.TextField(blank=True, help_text="Liste des logiciels installés et leurs versions")
    adresse_ip = models.GenericIPAddressField("Adresse IP", null=True, blank=True)
    adresse_mac = models.CharField("Adresse MAC", max_length=17, blank=True)
    nom_reseau = models.CharField("Nom sur le réseau", max_length=100, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_SERVICE')
    date_derniere_maj = models.DateField("Dernière mise à jour", auto_now=True)
    date_derniere_maintenance = models.DateField("Dernière maintenance", null=True, blank=True)
    prochaine_maintenance = models.DateField("Maintenance prévue", null=True, blank=True)
    date_acquisition = models.DateField(null=True, blank=True)
    date_mise_service = models.DateField("Date de mise en service", null=True, blank=True)
    fin_garantie = models.DateField("Fin de garantie", null=True, blank=True)
    contrat_maintenance = models.CharField("Contrat de maintenance", max_length=100, blank=True)

class ProfilEquipementMedical(models.Model):
    CLASSE_RISQUE_CHOICES = [
        ('I', 'Classe I - Risque faible'),
        ('IIa', 'Classe IIa - Risque modéré'),
        ('IIb', 'Classe IIb - Risque élevé'),
        ('III', 'Classe III - Risque critique'),
    ]

    STATUT_CHOICES = [
        ('ACTIF', 'Actif - En service'),
        ('MAINTENANCE', 'En maintenance'),
        ('STOCKAGE', 'En stockage'),
        ('INUTILISABLE', 'Hors service'),
        ('CALIBRATION', 'En calibration'),
    ]

    TYPE_CHOICES = [
        ('DIAGNOSTIC', 'Équipement de diagnostic'),
        ('THERAPEUTIQUE', 'Équipement thérapeutique'),
        ('LABORATOIRE', 'Équipement de laboratoire'),
        ('MONITORING', 'Équipement de surveillance'),
        ('IMAGERIE', 'Équipement d\'imagerie'),
        ('CHIRURGICAL', 'Équipement chirurgical'),
        ('STERILISATION', 'Équipement de stérilisation'),
        ('AUTRE', 'Autre'),
    ]

    bien = models.OneToOneField('Bien', on_delete=models.CASCADE, related_name='profil_equipement_medical')
    type_equipement = models.CharField(max_length=50, choices=TYPE_CHOICES)
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    numero_serie = models.CharField("Numéro de série", max_length=100)
    date_fabrication = models.DateField("Date de fabrication", null=True, blank=True)
    certification = models.CharField(max_length=100, help_text="Numéro de certification ou d'homologation")
    classe_risque = models.CharField("Classe de risque", max_length=3, choices=CLASSE_RISQUE_CHOICES, blank=True)
    normes_applicables = models.TextField("Normes applicables", blank=True)
    organisme_certification = models.CharField("Organisme de certification", max_length=100, blank=True)
    parametres_techniques = models.TextField("Paramètres techniques", blank=True)
    source_energie = models.CharField("Source d'énergie", max_length=100, blank=True)
    consommation = models.CharField("Consommation énergétique", max_length=50, blank=True)
    duree_vie = models.PositiveIntegerField("Durée de vie estimée (mois)", null=True, blank=True)
    date_installation = models.DateField("Date d'installation", null=True, blank=True)
    date_derniere_maintenance = models.DateField("Dernière maintenance", null=True, blank=True)
    frequence_maintenance = models.PositiveIntegerField("Fréquence de maintenance (jours)", default=365)
    maintenance = models.TextField("Protocole de maintenance", blank=True)
    pieces = models.TextField("Pièces détachées", blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ACTIF')
    departement_utilisation = models.CharField("Département d'utilisation", max_length=100, blank=True)
    utilisateurs_formes = models.TextField("Personnel formé à l'utilisation", blank=True)
    date_acquisition = models.DateField(null=True, blank=True)
    fin_garantie = models.DateField("Fin de garantie", null=True, blank=True)
    contrat_maintenance = models.CharField("Contrat de maintenance", max_length=100, blank=True)
    fournisseur_service = models.CharField("Fournisseur de service", max_length=100, blank=True)
    contact_sav = models.CharField("Contact SAV", max_length=100, blank=True)
