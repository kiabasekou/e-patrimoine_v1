# models/user.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class UtilisateurPatrimoine(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('gestionnaire', 'Gestionnaire'),
        ('consultant', 'Consultant'),
        ('responsable', 'Responsable de bien')
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='consultant')
    entite = models.ForeignKey('Entite', on_delete=models.SET_NULL, null=True, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
    def est_admin(self):
        return self.role == 'admin' or self.is_superuser
    
    def est_gestionnaire(self):
        return self.role == 'gestionnaire' or self.est_admin()
    
    def est_responsable_du_bien(self, bien):
        return bien.responsabilites.filter(
            responsable__user=self, 
            type_affectation='permanent'
        ).exists()