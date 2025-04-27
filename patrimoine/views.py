from django.db.models import Sum, Count, Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from .models import Bien, Categorie, SousCategorie, Entite, HistoriqueValeur, Province, Commune
from .forms import (
    BienForm,
    HistoriqueValeurForm,
    ProfilVehiculeForm,
    ProfilImmeubleForm,
    ProfilInformatiqueForm,
    ProfilEquipementMedicalForm,
    ProfilMobilierForm,
    ProfilTerrainForm,
    ProfilConsommableForm,
)

from collections import defaultdict
import openpyxl
from openpyxl.utils import get_column_letter
from django.db.models.functions import ExtractYear
from django.utils.timezone import now



def accueil_view(request):
    context = {
        "now": now()  # pour afficher l'année dans le footer
    }
    return render(request, "home.html", context)


# --- Mapping centralisé code -> (FormClass, template) ---
# Mapping unifié basé sur vos codes en base
FORM_MAPPING = {
    'batiments_administratifs': {'form': ProfilImmeubleForm, 'template': 'patrimoine/_form_immeuble.html'},
    'infrastructures_sanitaires': {'form': ProfilImmeubleForm, 'template': 'patrimoine/_form_immeuble.html'},
    'terrains': {'form': ProfilTerrainForm, 'template': 'patrimoine/_form_terrain.html'},
    'installations_techniques': {'form': ProfilImmeubleForm, 'template': 'patrimoine/_form_immeuble.html'},
    'equipement_medical': {'form': ProfilEquipementMedicalForm, 'template': 'patrimoine/_form_equipement_medical.html'},
    'materiel_informatique': {'form': ProfilInformatiqueForm, 'template': 'patrimoine/_form_informatique.html'},
    'mobilier_de_bureau': {'form': ProfilMobilierForm, 'template': 'patrimoine/_form_mobilier.html'},
    'vehicules_de_service': {'form': ProfilVehiculeForm, 'template': 'patrimoine/_form_vehicule.html'},
    'consommables_de_valeur_et_stocks_strategiques': {
        'form': ProfilConsommableForm,
        'template': 'patrimoine/_form_consommables.html',
    },
}


# --- Class-based views ---
class BienListView(ListView):
    model = Bien
    template_name = 'patrimoine/bien_list.html'
    context_object_name = 'biens'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('categorie', 'entite').order_by('nom')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(nom__icontains=search_query) | Q(categorie__nom__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


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


class DetailViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historiques'] = self.object.historiques.order_by('date')
        return context


class BienDetailView(DetailView, DetailViewMixin):
    model = Bien
    template_name = 'patrimoine/bien_detail.html'
    context_object_name = 'bien'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = HistoriqueValeurForm(request.POST)
        if form.is_valid():
            history_entry = form.save(commit=False)
            history_entry.bien = self.object
            history_entry.save()
            return redirect('biens:bien_detail', pk=self.object.pk)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)



class DashboardView(TemplateView):
    template_name = 'patrimoine/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Export Excel
        if self.request.GET.get('format') == 'excel':
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = "Tableau de bord"
            worksheet.append(['Catégorie', 'Nombre de biens', 'Valeur totale (FCFA)'])

            biens_par_categorie = Bien.objects.values('categorie__nom').annotate(
                nb_biens=Count('id'), total=Sum('valeur_initiale')
            )

            for category_data in biens_par_categorie:
                worksheet.append([
                    category_data['categorie__nom'],
                    category_data['nb_biens'],
                    float(category_data['total'] or 0),
                ])

            for col_idx in range(1, 4):
                worksheet.column_dimensions[get_column_letter(col_idx)].width = 25

            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=dashboard.xlsx'
            workbook.save(response)
            return response

        # Filtres
        all_biens = Bien.objects.select_related('commune', 'categorie', 'entite')
        selected_year = self.request.GET.get('annee')
        selected_commune = self.request.GET.get('commune')

        if selected_year:
            all_biens = all_biens.filter(date_acquisition__year=selected_year)
        if selected_commune:
            all_biens = all_biens.filter(commune__id=selected_commune)

        context.update({
            'valeur_totale': all_biens.aggregate(Sum('valeur_initiale'))['valeur_initiale__sum'] or 0,
            'par_categorie': all_biens.values('categorie__nom').annotate(
                nb_biens=Count('id'), total=Sum('valeur_initiale')
            ),
            'par_entite': all_biens.values('entite__nom').annotate(
                nb_biens=Count('id'), total=Sum('valeur_initiale')
            ),
            'par_commune': all_biens.values('commune__nom').annotate(
                nb_biens=Count('id'), total=Sum('valeur_initiale')
            ),
            'annees_disponibles': Bien.objects.annotate(annee=ExtractYear('date_acquisition'))
                .values_list('annee', flat=True)
                .distinct()
                .order_by('-annee'),
            'communes': Commune.objects.all(),
        })

        return context


@csrf_exempt
def ajouter_bien(request):
    bien_form = BienForm(request.POST or None, request.FILES or None)
    profil_form = None

    if request.method == 'POST' and bien_form.is_valid():
        bien = bien_form.save(commit=False)
        sous_categorie_code = bien_form.cleaned_data['sous_categorie'].code
        profil_form_class = FORM_MAPPING.get(sous_categorie_code, {}).get('form')
        profil_valid = True

        if profil_form_class:
            profil_form = profil_form_class(request.POST, request.FILES)
            profil_valid = profil_form.is_valid()

        bien.save()

        if profil_form_class and profil_valid:
            profil = profil_form.save(commit=False)
            profil.bien = bien
            profil.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('biens:bien_detail', pk=bien.pk)

    return render(request, 'patrimoine/ajouter_bien.html', {'bien_form': bien_form, 'profil_form': profil_form})


@csrf_exempt
def get_profil_form(request):
    sous_categorie_id = request.GET.get('sous_categorie_id')
    if not sous_categorie_id or not sous_categorie_id.isdigit():
        return JsonResponse({'error': 'ID invalide'}, status=400)
    try:
        sous_categorie = SousCategorie.objects.get(pk=int(sous_categorie_id))
        form_config = FORM_MAPPING.get(sous_categorie.code)
        if form_config and form_config['form']:
            html_form = render_to_string(
                form_config['template'], {'profil_form': form_config['form']()}, request=request
            )
            return JsonResponse({'form': html_form})
        return JsonResponse({'form': ''})
    except SousCategorie.DoesNotExist:
        return JsonResponse({'error': 'Sous-catégorie introuvable'}, status=404)


@csrf_exempt
def load_sous_categories(request):
    categorie_id = request.GET.get('categorie')
    sous_categories = SousCategorie.objects.filter(categorie_id=categorie_id).order_by('nom')
    html_dropdown = render_to_string('patrimoine/sous_categorie_dropdown_list.html', {'sous_categories': sous_categories})
    return HttpResponse(html_dropdown)




from collections import defaultdict
from django.views.generic import TemplateView
from patrimoine.models import Bien, Province, Entite

class CarteView(TemplateView):
    template_name = 'patrimoine/carte.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        biens = Bien.objects.select_related(
            'commune__departement__province',
            'categorie',
            'entite'
        )

        carte_data = []

        for bien in biens:
            commune = bien.commune
            if commune and commune.latitude and commune.longitude:
                carte_data.append({
                    'commune_nom': commune.nom,
                    'latitude': float(commune.latitude),
                    'longitude': float(commune.longitude),
                    'categorie': bien.categorie.nom if bien.categorie else '',
                    'annee': bien.date_acquisition.year if bien.date_acquisition else '',
                    'province_nom': commune.departement.province.nom if commune.departement and commune.departement.province else '',
                    'entite_nom': bien.entite.nom if bien.entite else '',
                    'nb_biens': 1,
                    'total': float(bien.valeur_initiale) if bien.valeur_initiale else 0,
                })

        context['carte_data'] = carte_data
        context['categories'] = sorted({bien.categorie.nom for bien in biens if bien.categorie})
        context['annees'] = sorted({bien.date_acquisition.year for bien in biens if bien.date_acquisition}, reverse=True)
        context['provinces'] = list(Province.objects.values_list('nom', flat=True))
        context['entites'] = list(Entite.objects.values_list('nom', flat=True))

        return context
