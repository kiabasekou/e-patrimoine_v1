from django.db.models import Sum, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView, TemplateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.serializers.json import DjangoJSONEncoder
import openpyxl
from openpyxl.utils import get_column_letter
import json
from django.db.models.functions import ExtractYear
from patrimoine.models import Bien, Province

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
        if self.request.GET.get('format') == 'excel':
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Tableau de bord"

            ws.append(['Catégorie', 'Nombre de biens', 'Valeur totale (FCFA)'])
            par_cat = Bien.objects.values('categorie__nom').annotate(
                nb_biens=Count('id'), total=Sum('valeur_initiale')
            )
            for cat in par_cat:
                ws.append([
                    cat['categorie__nom'],
                    cat['nb_biens'],
                    float(cat['total'] or 0)
                ])

            # Largeur des colonnes
            for col in range(1, 4):
                ws.column_dimensions[get_column_letter(col)].width = 25

            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=dashboard_export.xlsx'
            wb.save(response)
            return response

        context = super().get_context_data(**kwargs)

        annee = self.request.GET.get('annee')
        province_id = self.request.GET.get('province')

        biens = Bien.objects.all()

        if annee:
            biens = biens.filter(date_acquisition__year=annee)
        if province_id:
            biens = biens.filter(entite__commune__departement__province__id=province_id)

        context['valeur_totale'] = biens.aggregate(Sum('valeur_initiale'))['valeur_initiale__sum'] or 0

        par_cat = biens.values('categorie__nom').annotate(nb_biens=Count('id'), total=Sum('valeur_initiale'))
        par_entite = biens.values('entite__nom').annotate(nb_biens=Count('id'), total=Sum('valeur_initiale'))
        par_province = biens.values('entite__commune__departement__province__nom').annotate(nb_biens=Count('id'), total=Sum('valeur_initiale'))

        context['par_categorie'] = par_cat
        context['par_entite'] = par_entite
        context['par_province'] = par_province

        context['categorie_labels'] = json.dumps([e['categorie__nom'] for e in par_cat], cls=DjangoJSONEncoder)
        context['categorie_data'] = json.dumps([e['nb_biens'] for e in par_cat], cls=DjangoJSONEncoder)

        context['entite_labels'] = json.dumps([e['entite__nom'] for e in par_entite], cls=DjangoJSONEncoder)
        context['entite_data'] = json.dumps([e['nb_biens'] for e in par_entite], cls=DjangoJSONEncoder)

        context['province_labels'] = json.dumps([e['entite__commune__departement__province__nom'] for e in par_province], cls=DjangoJSONEncoder)
        context['province_data'] = json.dumps([e['nb_biens'] for e in par_province], cls=DjangoJSONEncoder)

        context['annee'] = annee
        context['province'] = province_id

        context['annees_disponibles'] = (
            Bien.objects
            .annotate(annee=ExtractYear('date_acquisition'))
            .values_list('annee', flat=True)
            .distinct()
            .order_by('-annee')
        )

        context['provinces'] = Province.objects.all()

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




@csrf_exempt
def ajouter_bien(request):
    bien_form = BienForm(request.POST or None)
    profil_form = None

    if request.method == 'POST':
        if bien_form.is_valid():
            bien = bien_form.save(commit=False)
            sous_categorie = bien_form.cleaned_data['sous_categorie']
            code = sous_categorie.code

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
            profil_form = profil_class(request.POST) if profil_class else None

            if not profil_class or (profil_form and profil_form.is_valid()):
                bien.save()
                if profil_form:
                    profil = profil_form.save(commit=False)
                    profil.bien = bien
                    profil.save()

                # ✅ Réponse AJAX
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})

                return redirect('biens:bien_detail', pk=bien.pk)

        # En cas d'erreurs :
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': bien_form.errors if bien_form.errors else profil_form.errors if profil_form else None})

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