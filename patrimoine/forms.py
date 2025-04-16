from django import forms

# Importation des modèles
from .models import (
    Bien,
    HistoriqueValeur,
    SousCategorie,
    
)

from .profils import ProfilVehicule, ProfilImmeuble, ProfilInformatique, ProfilEquipementMedical


# Les classes de formulaires peuvent être définies ici
# class BienForm(forms.ModelForm):
#     ...

class HistoriqueValeurForm(forms.ModelForm):
    class Meta:
        model = HistoriqueValeur
        fields = ['date', 'valeur']




class BienForm(forms.ModelForm):
    class Meta:
        model = Bien
        fields = [
            'nom', 'categorie', 'sous_categorie',
            'valeur_initiale', 'date_acquisition',
            'entite'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sous_categorie'].queryset = SousCategorie.objects.none()

        if 'categorie' in self.data:
            try:
                cat_id = int(self.data.get('categorie'))
                self.fields['sous_categorie'].queryset = SousCategorie.objects.filter(categorie_id=cat_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.categorie:
            self.fields['sous_categorie'].queryset = self.instance.categorie.sous_categories.all()



class ProfilVehiculeForm(forms.ModelForm):
    class Meta:
        model = ProfilVehicule
        exclude = ['bien']

class ProfilImmeubleForm(forms.ModelForm):
    class Meta:
        model = ProfilImmeuble
        exclude = ['bien']



class ProfilInformatiqueForm(forms.ModelForm):
    class Meta:
        model = ProfilInformatique
        exclude = ['bien']
        widgets = {
            'date_fabrication': forms.DateInput(attrs={'type': 'date'}),
            'date_acquisition': forms.DateInput(attrs={'type': 'date'}),
            'date_mise_service': forms.DateInput(attrs={'type': 'date'}),
            'date_derniere_maintenance': forms.DateInput(attrs={'type': 'date'}),
            'prochaine_maintenance': forms.DateInput(attrs={'type': 'date'}),
        }

class ProfilEquipementMedicalForm(forms.ModelForm):
    class Meta:
        model = ProfilEquipementMedical
        exclude = ['bien']
        widgets = {
            'date_fabrication': forms.DateInput(attrs={'type': 'date'}),
            'date_installation': forms.DateInput(attrs={'type': 'date'}),
            'date_acquisition': forms.DateInput(attrs={'type': 'date'}),
            'fin_garantie': forms.DateInput(attrs={'type': 'date'}),
            'date_derniere_maintenance': forms.DateInput(attrs={'type': 'date'}),
        }
