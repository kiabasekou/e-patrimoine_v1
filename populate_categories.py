import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patrimoine_project.settings")
django.setup()

from patrimoine.models import Categorie, SousCategorie

CATEGORIES = {
    "Bien Immobilier": {
        "type": "immobilier",
        "sous_categories": [
            "Bâtiments administratifs",
            "Infrastructures sanitaires",
            "Terrains",
            "Installations techniques"
        ]
    },
    "Bien Mobilier": {
        "type": "mobilier",
        "sous_categories": [
            "Équipement médical",
            "Matériel informatique",
            "Mobilier de bureau",
            "Véhicules de service",
            "Consommables de valeur et stocks stratégiques"
        ]
    }
}

compteur_c = 0
compteur_sc = 0

for cat_nom, data in CATEGORIES.items():
    type_cat = data["type"]
    sous_cats = data["sous_categories"]

    # Crée ou récupère la catégorie
    cat, created = Categorie.objects.get_or_create(
        nom=cat_nom,
        defaults={"type": type_cat}
    )
    if created:
        print(f"✅ Catégorie créée : {cat_nom}")
        compteur_c += 1
    else:
        print(f"🔁 Catégorie existante : {cat_nom}")

    # Crée les sous-catégories
    for sc_nom in sous_cats:
        sc, created = SousCategorie.objects.get_or_create(
            nom=sc_nom,
            categorie=cat
        )
        if created:
            print(f"  └─ 🆕 Sous-catégorie : {sc_nom}")
            compteur_sc += 1
        else:
            print(f"  └─ 🔁 Déjà existante : {sc_nom}")

print(f"\n🎉 Total : {compteur_c} catégories créées, {compteur_sc} sous-catégories ajoutées.")
