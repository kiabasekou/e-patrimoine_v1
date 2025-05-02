# models/audit.py
from django.db import models
from django.utils import timezone
import json

class JournalAudit(models.Model):
    ACTION_CHOICES = [
        ('create', 'Création'),
        ('update', 'Modification'),
        ('delete', 'Suppression'),
        ('view', 'Consultation'),
        ('export', 'Exportation'),
    ]
    
    utilisateur = models.ForeignKey('UtilisateurPatrimoine', on_delete=models.SET_NULL, null=True)
    date_action = models.DateTimeField(default=timezone.now)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    modele = models.CharField(max_length=50)
    objet_id = models.IntegerField()
    details = models.JSONField(default=dict)
    adresse_ip = models.GenericIPAddressField()
    
    class Meta:
        ordering = ['-date_action']
        verbose_name = "Journal d'audit"
        verbose_name_plural = "Journal d'audit"
    
    def __str__(self):
        return f"{self.get_action_display()} - {self.modele} #{self.objet_id} - {self.date_action}"

    def set_changes(self, ancien, nouveau):
        """Enregistre les changements entre deux états"""
        changes = {}
        
        # Parcourir les champs de l'objet
        if isinstance(ancien, dict) and isinstance(nouveau, dict):
            for key in set(ancien.keys()) | set(nouveau.keys()):
                if key not in ancien:
                    changes[key] = {'old': None, 'new': nouveau[key]}
                elif key not in nouveau:
                    changes[key] = {'old': ancien[key], 'new': None}
                elif ancien[key] != nouveau[key]:
                    changes[key] = {'old': ancien[key], 'new': nouveau[key]}
        
        self.details['changes'] = changes
        self.save()