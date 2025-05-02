# Créer un répertoire services/ avec des fichiers dédiés

# services/bien_service.py
from django.db.models import Sum, Count, Q
from ..models import Bien, HistoriqueValeur

class BienService:
    @staticmethod
    def filtrer_biens(categorie_id=None, entite_id=None, search_query=None):
        """Centralise la logique de filtrage des biens"""
        queryset = Bien.objects.select_related('categorie', 'entite').order_by('nom')
        
        if categorie_id:
            queryset = queryset.filter(categorie_id=categorie_id)
        
        if entite_id:
            queryset = queryset.filter(entite_id=entite_id)
            
        if search_query:
            queryset = queryset.filter(
                Q(nom__icontains=search_query) | 
                Q(categorie__nom__icontains=search_query)
            )
            
        return queryset
    
    @staticmethod
    def obtenir_statistiques(biens_queryset):
        """Calcule les statistiques pour un ensemble de biens"""
        return {
            'valeur_totale': biens_queryset.aggregate(Sum('valeur_initiale'))['valeur_initiale__sum'] or 0,
            'par_categorie': biens_queryset.values('categorie__nom').annotate(
                nb_biens=Count('id'), total=Sum('valeur_initiale')
            ),
            'par_entite': biens_queryset.values('entite__nom').annotate(
                nb_biens=Count('id'), total=Sum('valeur_initiale')
            ),
            'par_commune': biens_queryset.values('commune__nom').annotate(
                nb_biens=Count('id'), total=Sum('valeur_initiale')
            ),
        }
    
    @staticmethod
    def ajouter_valeur_historique(bien, date, valeur):
        """Ajoute une entrée d'historique de valeur"""
        historique = HistoriqueValeur(
            bien=bien,
            date=date,
            valeur=valeur
        )
        historique.save()
        return historique