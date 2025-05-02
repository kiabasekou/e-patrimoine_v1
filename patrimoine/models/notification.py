# models/notification.py
from django.db import models
from django.utils import timezone

class Notification(models.Model):
    TYPE_CHOICES = [
        ('info', 'Information'),
        ('success', 'Succès'),
        ('warning', 'Avertissement'),
        ('danger', 'Alerte')
    ]
    
    utilisateur = models.ForeignKey('UtilisateurPatrimoine', on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField(max_length=100)
    message = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='info')
    date_creation = models.DateTimeField(default=timezone.now)
    lue = models.BooleanField(default=False)
    lien = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.titre} ({self.utilisateur.username})"