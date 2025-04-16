# 🏛️ Gestion du Patrimoine - Django App

Application web de gestion du patrimoine des biens matériels, développée avec Django.  
Elle permet de suivre l'inventaire, la valeur actuelle, et l'évolution des actifs.

---

## 🚀 Fonctionnalités principales

- 🔎 Liste, ajout, modification, suppression de biens
- 🏷️ Gestion des catégories et des entités d'affectation
- 📈 Suivi de l'historique de la valeur des biens dans le temps
- 🧾 Dashboard synthétique : valeur totale, répartition par catégorie/entité
- 📊 Visualisation graphique de l’évolution de la valeur (Chart.js)
- 🔐 Interface d’administration Django

---

## 🛠️ Technologies utilisées

- [Django 5.x](https://www.djangoproject.com/)
- [SQLite](https://www.sqlite.org/index.html) (dev) / PostgreSQL (prod)
- [python-decouple](https://pypi.org/project/python-decouple/)
- [Chart.js](https://www.chartjs.org/) pour les graphiques
- Bootstrap (optionnel pour mise en forme)

---

## 📦 Installation locale

### 1. Cloner le dépôt

```bash
git clone https://github.com/kiabasekou/gestion_patrimoine.git
cd gestion_patrimoine

python -m venv env
env\Scripts\activate  # sous Windows

pip install -r requirements.txt

SECRET_KEY=votre-cle-secrete
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

python manage.py runserver


gestion_patrimoine/
├── patrimoine_project/    ← configuration Django
├── patrimoine/            ← logique métier
├── templates/             ← HTML global (base, dashboard)
├── static/                ← fichiers statiques (optionnels)
├── .env                   ← variables sensibles (non versionné)
├── db.sqlite3             ← base de données locale
└── README.md


✍️ Auteur
Ahmed Souaré
Ministère de la Santé, République Gabonaise