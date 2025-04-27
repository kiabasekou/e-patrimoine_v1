import os
import django
import pandas as pd

# Initialisation Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patrimoine_project.settings")
django.setup()

from patrimoine.models import Province, Departement, Commune

# Lecture du fichier CSV corrigé
file_path = "decoupage_gabon_corrige.csv"
df = pd.read_csv(file_path, encoding="latin1", sep=',')

print("🚀 Colonnes disponibles :", df.columns.tolist())



# Nettoyage des noms (remplacer , et . par é)
def nettoyer_nom(val):
    if isinstance(val, str):
        return val.replace(",", "é").replace(".", "é").strip()
    return val

df = df.applymap(nettoyer_nom)

print(f"📄 Fichier chargé : {len(df)} lignes")

# Injection des données géographiques
for _, row in df.iterrows():
    province_nom = row['Province']
    departement_nom = row['Departement']
    commune_nom = row['Commune']

    # Ne pas arrondir, prendre tous les floats
    latitude = float(row.get('Latitude', 0))
    longitude = float(row.get('Longitude', 0))

    province, _ = Province.objects.get_or_create(nom=province_nom)
    departement, _ = Departement.objects.get_or_create(nom=departement_nom, province=province)

    Commune.objects.update_or_create(
        nom=commune_nom,
        departement=departement,
        defaults={
            'latitude': latitude,
            'longitude': longitude,
        }
    )

    print(f"✅ {commune_nom} -> lat: {latitude}, long: {longitude}")

print("🎯 Mise à jour des communes terminée.")
