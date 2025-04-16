import os
import django
import pandas as pd

# Initialisation Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patrimoine_project.settings")
django.setup()

from patrimoine.models import Province, Departement, Commune, Entite, Categorie, SousCategorie, Bien

# Charger le fichier CSV exporté de ChatGPT (ou la DataFrame utilisée)
df = pd.read_csv("biens_a_importer.csv")

# Création en cascade
for _, row in df.iterrows():
    # Province
    province, _ = Province.objects.get_or_create(nom=row["province"])
    
    # Département fictif (par défaut pour chaque commune, à personnaliser si besoin)
    departement, _ = Departement.objects.get_or_create(nom=f"{row['commune']} Département", province=province)
    
    # Commune
    commune, _ = Commune.objects.get_or_create(nom=row["commune"], departement=departement)

    # Entité
    entite, _ = Entite.objects.get_or_create(
        nom=row["entite"],
        defaults={"responsable": row["responsable"], "commune": commune}
    )

    if not entite.commune:
        entite.commune = commune
        entite.responsable = row["responsable"]
        entite.save()

    # Catégorie et Sous-catégorie
    cat, _ = Categorie.objects.get_or_create(nom="Bien Mobilier", type="mobilier")
    sous_cat, _ = SousCategorie.objects.get_or_create(nom=row["sous_categorie"], categorie=cat)

    # Bien
    Bien.objects.create(
        nom=row["nom"],
        categorie=cat,
        sous_categorie=sous_cat,
        entite=entite,
        valeur_initiale=row["valeur_initiale"],
        date_acquisition=row["date_acquisition"],
        description="Import automatique"
    )

print("✅ Biens importés avec succès.")
