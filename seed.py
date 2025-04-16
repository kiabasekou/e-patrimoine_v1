import os
import django
from random import choice, randint
from datetime import date

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patrimoine_project.settings')
django.setup()

from patrimoine.models import Categorie, Entite, Bien

# Réinitialisation des données (optionnel)
Bien.objects.all().delete()
Categorie.objects.all().delete()
Entite.objects.all().delete()

# Création de catégories
categories = ['Matériel informatique', 'Mobilier', 'Véhicule']
categorie_objs = [Categorie.objects.create(nom=cat) for cat in categories]

# Création d'entités
entites_data = [
    {'nom': 'Direction Informatique', 'responsable': 'M. Biyoghe'},
    {'nom': 'Service Financier', 'responsable': 'Mme Ndong'}
]
entite_objs = [Entite.objects.create(**data) for data in entites_data]

# Création de biens aléatoires
for i in range(1, 6):
    Bien.objects.create(
        nom=f'Bien Test {i}',
        categorie=choice(categorie_objs),
        entite=choice(entite_objs),
        valeur_initiale=randint(100000, 1000000),
        date_acquisition=date(2023, randint(1, 12), randint(1, 28)),
        description=f'Description du bien {i}'
    )

print("✅ Données insérées avec succès.")
