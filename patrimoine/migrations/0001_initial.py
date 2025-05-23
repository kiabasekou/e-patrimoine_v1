# Generated by Django 5.2 on 2025-04-22 02:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('type', models.CharField(blank=True, choices=[('immobilier', 'Bien Immobilier'), ('mobilier', 'Bien Mobilier')], max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ResponsableBien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('matricule', models.CharField(max_length=50, unique=True)),
                ('fonction', models.CharField(max_length=100)),
                ('categorie', models.CharField(max_length=50)),
                ('corps', models.CharField(max_length=100)),
                ('telephone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('departement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patrimoine.departement')),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('commune', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patrimoine.commune')),
            ],
        ),
        migrations.CreateModel(
            name='Entite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('responsable', models.CharField(max_length=100)),
                ('commune', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patrimoine.commune')),
            ],
        ),
        migrations.CreateModel(
            name='Bien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('valeur_initiale', models.DecimalField(decimal_places=2, max_digits=12)),
                ('date_acquisition', models.DateField()),
                ('description', models.TextField(blank=True)),
                ('numero_serie', models.CharField(blank=True, max_length=100, null=True)),
                ('duree_amortissement', models.IntegerField(blank=True, null=True)),
                ('superficie', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('annee_construction', models.PositiveIntegerField(blank=True, null=True)),
                ('statut_juridique', models.CharField(blank=True, max_length=100)),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='patrimoine.categorie')),
                ('entite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patrimoine.entite')),
            ],
        ),
        migrations.CreateModel(
            name='HistoriqueValeur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('valeur', models.DecimalField(decimal_places=2, max_digits=12)),
                ('bien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historiques', to='patrimoine.bien')),
            ],
        ),
        migrations.CreateModel(
            name='ProfilEquipementMedical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_equipement', models.CharField(choices=[('DIAGNOSTIC', 'Équipement de diagnostic'), ('THERAPEUTIQUE', 'Équipement thérapeutique'), ('LABORATOIRE', 'Équipement de laboratoire'), ('MONITORING', 'Équipement de surveillance'), ('IMAGERIE', "Équipement d'imagerie"), ('CHIRURGICAL', 'Équipement chirurgical'), ('STERILISATION', 'Équipement de stérilisation'), ('AUTRE', 'Autre')], max_length=50)),
                ('marque', models.CharField(max_length=100)),
                ('modele', models.CharField(max_length=100)),
                ('numero_serie', models.CharField(max_length=100, verbose_name='Numéro de série')),
                ('date_fabrication', models.DateField(blank=True, null=True, verbose_name='Date de fabrication')),
                ('certification', models.CharField(help_text="Numéro de certification ou d'homologation", max_length=100)),
                ('classe_risque', models.CharField(blank=True, choices=[('I', 'Classe I - Risque faible'), ('IIa', 'Classe IIa - Risque modéré'), ('IIb', 'Classe IIb - Risque élevé'), ('III', 'Classe III - Risque critique')], max_length=3, verbose_name='Classe de risque')),
                ('normes_applicables', models.TextField(blank=True, verbose_name='Normes applicables')),
                ('organisme_certification', models.CharField(blank=True, max_length=100, verbose_name='Organisme de certification')),
                ('parametres_techniques', models.TextField(blank=True, verbose_name='Paramètres techniques')),
                ('source_energie', models.CharField(blank=True, max_length=100, verbose_name="Source d'énergie")),
                ('consommation', models.CharField(blank=True, max_length=50, verbose_name='Consommation énergétique')),
                ('duree_vie', models.PositiveIntegerField(blank=True, null=True, verbose_name='Durée de vie estimée (mois)')),
                ('date_installation', models.DateField(blank=True, null=True, verbose_name="Date d'installation")),
                ('date_derniere_maintenance', models.DateField(blank=True, null=True, verbose_name='Dernière maintenance')),
                ('frequence_maintenance', models.PositiveIntegerField(default=365, verbose_name='Fréquence de maintenance (jours)')),
                ('maintenance', models.TextField(blank=True, verbose_name='Protocole de maintenance')),
                ('pieces', models.TextField(blank=True, verbose_name='Pièces détachées')),
                ('statut', models.CharField(choices=[('ACTIF', 'Actif - En service'), ('MAINTENANCE', 'En maintenance'), ('STOCKAGE', 'En stockage'), ('INUTILISABLE', 'Hors service'), ('CALIBRATION', 'En calibration')], default='ACTIF', max_length=20)),
                ('departement_utilisation', models.CharField(blank=True, max_length=100, verbose_name="Département d'utilisation")),
                ('utilisateurs_formes', models.TextField(blank=True, verbose_name="Personnel formé à l'utilisation")),
                ('date_acquisition', models.DateField(blank=True, null=True)),
                ('fin_garantie', models.DateField(blank=True, null=True, verbose_name='Fin de garantie')),
                ('contrat_maintenance', models.CharField(blank=True, max_length=100, verbose_name='Contrat de maintenance')),
                ('fournisseur_service', models.CharField(blank=True, max_length=100, verbose_name='Fournisseur de service')),
                ('contact_sav', models.CharField(blank=True, max_length=100, verbose_name='Contact SAV')),
                ('bien', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profil_equipement_medical', to='patrimoine.bien')),
            ],
        ),
        migrations.CreateModel(
            name='ProfilImmeuble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surface', models.DecimalField(decimal_places=2, max_digits=8)),
                ('nb_etages', models.PositiveIntegerField()),
                ('annee_construction', models.PositiveIntegerField()),
                ('securite', models.CharField(max_length=255)),
                ('bien', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profil_immeuble', to='patrimoine.bien')),
            ],
        ),
        migrations.CreateModel(
            name='ProfilInformatique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_equipement', models.CharField(choices=[('ORDINATEUR_FIXE', 'Ordinateur fixe'), ('ORDINATEUR_PORTABLE', 'Ordinateur portable'), ('SERVEUR', 'Serveur'), ('IMPRIMANTE', 'Imprimante'), ('SCANNER', 'Scanner'), ('PHOTOCOPIEUR', 'Photocopieur'), ('RESEAU', 'Équipement réseau'), ('STOCKAGE', 'Solution de stockage'), ('AUTRE', 'Autre')], max_length=50)),
                ('marque', models.CharField(max_length=100)),
                ('modele', models.CharField(max_length=100)),
                ('numero_serie', models.CharField(max_length=100, verbose_name='Numéro de série')),
                ('date_fabrication', models.DateField(blank=True, null=True, verbose_name='Date de fabrication')),
                ('processeur', models.CharField(blank=True, max_length=100)),
                ('memoire_ram', models.CharField(blank=True, max_length=50, verbose_name='Mémoire RAM')),
                ('capacite_stockage', models.CharField(blank=True, max_length=50, verbose_name='Capacité de stockage')),
                ('carte_graphique', models.CharField(blank=True, max_length=100, verbose_name='Carte graphique')),
                ('spec_tech', models.TextField(verbose_name='Spécifications techniques additionnelles')),
                ('os', models.CharField(blank=True, max_length=100, verbose_name="Système d'exploitation")),
                ('version_os', models.CharField(blank=True, max_length=50, verbose_name='Version OS')),
                ('logiciels', models.TextField(blank=True, help_text='Liste des logiciels installés et leurs versions')),
                ('adresse_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='Adresse IP')),
                ('adresse_mac', models.CharField(blank=True, max_length=17, verbose_name='Adresse MAC')),
                ('nom_reseau', models.CharField(blank=True, max_length=100, verbose_name='Nom sur le réseau')),
                ('statut', models.CharField(choices=[('EN_SERVICE', 'En service'), ('EN_MAINTENANCE', 'En maintenance'), ('HORS_SERVICE', 'Hors service'), ('EN_ATTENTE', 'En attente de déploiement')], default='EN_SERVICE', max_length=20)),
                ('date_derniere_maj', models.DateField(auto_now=True, verbose_name='Dernière mise à jour')),
                ('date_derniere_maintenance', models.DateField(blank=True, null=True, verbose_name='Dernière maintenance')),
                ('prochaine_maintenance', models.DateField(blank=True, null=True, verbose_name='Maintenance prévue')),
                ('date_acquisition', models.DateField(blank=True, null=True)),
                ('date_mise_service', models.DateField(blank=True, null=True, verbose_name='Date de mise en service')),
                ('fin_garantie', models.DateField(blank=True, null=True, verbose_name='Fin de garantie')),
                ('contrat_maintenance', models.CharField(blank=True, max_length=100, verbose_name='Contrat de maintenance')),
                ('bien', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profil_informatique', to='patrimoine.bien')),
            ],
        ),
        migrations.CreateModel(
            name='ProfilVehicule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marque', models.CharField(max_length=100)),
                ('modele', models.CharField(max_length=100)),
                ('immatriculation', models.CharField(max_length=20)),
                ('puissance', models.CharField(max_length=50)),
                ('consommation', models.CharField(max_length=50)),
                ('assurance', models.CharField(max_length=100)),
                ('bien', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profil_vehicule', to='patrimoine.bien')),
            ],
        ),
        migrations.AddField(
            model_name='departement',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patrimoine.province'),
        ),
        migrations.CreateModel(
            name='BienResponsabilite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_affectation', models.DateField()),
                ('type_affectation', models.CharField(choices=[('permanent', 'Permanent'), ('temporaire', 'Temporaire')], max_length=20)),
                ('motif', models.TextField(blank=True)),
                ('numero_permis', models.CharField(blank=True, max_length=50, null=True)),
                ('date_permis', models.DateField(blank=True, null=True)),
                ('categorie_permis', models.CharField(blank=True, max_length=10, null=True)),
                ('composition_foyer', models.TextField(blank=True, null=True)),
                ('conditions_occupation', models.TextField(blank=True, null=True)),
                ('certifications', models.TextField(blank=True, null=True)),
                ('formations', models.TextField(blank=True, null=True)),
                ('bien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsabilites', to='patrimoine.bien')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patrimoine.responsablebien')),
            ],
            options={
                'verbose_name': 'Responsabilité d’un bien',
                'verbose_name_plural': 'Responsabilités des biens',
                'ordering': ['-date_affectation'],
            },
        ),
        migrations.CreateModel(
            name='SousCategorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('code', models.SlugField(blank=True, help_text="Code système unique (ex: 'ambulance', 'serveur')", null=True, unique=True)),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sous_categories', to='patrimoine.categorie')),
            ],
        ),
        migrations.AddField(
            model_name='bien',
            name='sous_categorie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='patrimoine.souscategorie'),
        ),
    ]
