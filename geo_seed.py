import os
import django
import pandas as pd

# Initialisation Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patrimoine_project.settings")
django.setup()

from patrimoine.models import Province, Departement, Commune

# Lecture du fichier CSV avec encodage ISO-8859-1 et séparateur ;
file_path = "decoupage administratif gabon.csv"
df = pd.read_csv(file_path, encoding="ISO-8859-1", sep=';')

# Nettoyage des espaces superflus
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Statistiques
print(f"📄 Fichier chargé : {len(df)} lignes")

# Création en cascade
for _, row in df.iterrows():
    province_nom = row['Province']
    departement_nom = row['Departement']
    commune_nom = row['Commune']

    province, _ = Province.objects.get_or_create(nom=province_nom)
    departement, _ = Departement.objects.get_or_create(nom=departement_nom, province=province)
    Commune.objects.get_or_create(nom=commune_nom, departement=departement)

print("✅ Import géographique terminé avec succès.")
