from django.db.models import Sum, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView, TemplateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Bien, Categorie, SousCategorie, Entite, HistoriqueValeur
from .forms import (
    BienForm,
    HistoriqueValeurForm,
    ProfilVehiculeForm,
    ProfilImmeubleForm,
    ProfilInformatiqueForm,
    ProfilEquipementMedicalForm
)

class BienListView(ListView):
    model = Bien
    template_name = 'patrimoine/bien_list.html'
    context_object_name = 'biens'


class BienCreateView(CreateView):
    model = Bien
    form_class = BienForm
    template_name = 'patrimoine/bien_form.html'
    success_url = reverse_lazy('biens:bien_list')


class BienUpdateView(UpdateView):
    model = Bien
    form_class = BienForm
    template_name = 'patrimoine/bien_form.html'
    success_url = reverse_lazy('biens:bien_list')


class BienDeleteView(DeleteView):
    model = Bien
    template_name = 'patrimoine/bien_confirm_delete.html'
    success_url = reverse_lazy('biens:bien_list')


class DashboardView(TemplateView):
    template_name = 'patrimoine/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['valeur_totale'] = Bien.objects.aggregate(Sum('valeur_initiale'))['valeur_initiale__sum'] or 0
        context['par_categorie'] = Bien.objects.values('categorie__nom').annotate(nb_biens=Count('id'), total=Sum('valeur_initiale')).order_by('-nb_biens')
        context['par_entite'] = Bien.objects.values('entite__nom').annotate(nb_biens=Count('id'), total=Sum('valeur_initiale')).order_by('-nb_biens')
        return context


class BienDetailView(DetailView):
    model = Bien
    template_name = 'patrimoine/bien_detail.html'
    context_object_name = 'bien'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historiques'] = self.object.historiques.order_by('date')
        context['form'] = HistoriqueValeurForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = HistoriqueValeurForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.bien = self.object
            instance.save()
            return redirect('biens:bien_detail', pk=self.object.pk)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


def load_sous_categories(request):
    categorie_id = request.GET.get('categorie')
    sous_categories = SousCategorie.objects.filter(categorie_id=categorie_id).order_by('nom')
    return HttpResponse(render_to_string('patrimoine/sous_categorie_dropdown_list.html', {'sous_categories': sous_categories}))


def ajouter_bien(request):
    bien_form = BienForm(request.POST or None)
    profil_form = None

    if request.method == 'POST' and bien_form.is_valid():
        bien = bien_form.save(commit=False)
        sous_categorie = bien_form.cleaned_data['sous_categorie']
        code = sous_categorie.code  # 👈 usage du code plutôt que nom

        form_classes = {
            'ambulance': ProfilVehiculeForm,
            'vehicule_service': ProfilVehiculeForm,
            'batiment_admin': ProfilImmeubleForm,
            'infra_sante': ProfilImmeubleForm,
            'serveur': ProfilInformatiqueForm,
            'ordinateur': ProfilInformatiqueForm,
            'scanner_medical': ProfilEquipementMedicalForm,
            'appareil_imagerie': ProfilEquipementMedicalForm,
            'centrifugeuse': ProfilEquipementMedicalForm,
        }

        profil_class = form_classes.get(code)
        if profil_class:
            profil_form = profil_class(request.POST)
            if profil_form.is_valid():
                bien.save()
                profil = profil_form.save(commit=False)
                profil.bien = bien
                profil.save()
                return redirect('biens:bien_detail', pk=bien.pk)

    return render(request, 'patrimoine/ajouter_bien.html', {
        'bien_form': bien_form,
        'profil_form': profil_form
    })

def get_profil_form(request):
    sous_categorie_id = request.GET.get('sous_categorie_id')
    try:
        sous_cat = SousCategorie.objects.get(id=sous_categorie_id)
        code = sous_cat.code

        templates_forms = {
            'ambulance': ('patrimoine/_form_vehicule.html', ProfilVehiculeForm),
            'vehicule_service': ('patrimoine/_form_vehicule.html', ProfilVehiculeForm),
            'batiment_admin': ('patrimoine/_form_immeuble.html', ProfilImmeubleForm),
            'infra_sante': ('patrimoine/_form_immeuble.html', ProfilImmeubleForm),
            'serveur': ('patrimoine/_form_informatique.html', ProfilInformatiqueForm),
            'ordinateur': ('patrimoine/_form_informatique.html', ProfilInformatiqueForm),
            'scanner_medical': ('patrimoine/_form_equipement_medical.html', ProfilEquipementMedicalForm),
            'centrifugeuse': ('patrimoine/_form_equipement_medical.html', ProfilEquipementMedicalForm),
            'appareil_imagerie': ('patrimoine/_form_equipement_medical.html', ProfilEquipementMedicalForm),
        }

        template, form_class = templates_forms.get(code, (None, None))
        if template and form_class:
            html = render_to_string(template, {'profil_form': form_class()}, request=request)
            return JsonResponse({'form': html})

    except SousCategorie.DoesNotExist:
        return JsonResponse({'error': 'Sous-catégorie introuvable'})

    return JsonResponse({'form': ''})
