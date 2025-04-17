from django.urls import path
from . import views

app_name = 'biens'  # 👈 Obligatoire pour le namespace

urlpatterns = [
    path('', views.BienListView.as_view(), name='bien_list'),
    path('ajouter/', views.BienCreateView.as_view(), name='bien_create'),
    path('<int:pk>/', views.BienDetailView.as_view(), name='bien_detail'),
    path('<int:pk>/modifier/', views.BienUpdateView.as_view(), name='bien_update'),
    path('<int:pk>/supprimer/', views.BienDeleteView.as_view(), name='bien_delete'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # Vues AJAX
    path('ajax/get-profil-form/', views.get_profil_form, name='get_profil_form'),  # 👈 Important
    path('ajax/load-sous-categories/', views.load_sous_categories, name='ajax_load_sous_categories'),

    # Vue combinée
    path('ajouter-complet/', views.ajouter_bien, name='ajouter_bien_complet'),
]