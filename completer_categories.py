import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patrimoine_project.settings")
django.setup()

from patrimoine.models import Categorie

# Nombre de catégories modifiées
modifiees = 0

# Met à jour les catégories sans type
for cat in Categorie.objects.filter(type__isnull=True):
    cat.type = 'a_classer'  # 👈 type temporaire que tu pourras corriger dans l'admin
    cat.save()
    print(f"🛠️ Catégorie mise à jour : {cat.nom} → a_classer")
    modifiees += 1

if modifiees:
    print(f"✅ {modifiees} catégories ont été mises à jour.")
else:
    print("👌 Toutes les catégories avaient déjà un type.")
