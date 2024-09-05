from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords


class Animal(models.Model):
    TYPE_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
    ]

    STATUS_CHOICES = [
        ('waiting', 'Waiting'),  # En espera de adopción por diversas razones, primer status
        ('available', 'Available'),  # Disponible para adopción, se viene aqui de 'waiting'
        ('pending', 'Pending'),  # Proceso de adopción en curso, se viene aqui de 'available'
        ('adopted', 'Adopted'),  # Adoptado exitosamente, se viene aqui de 'pending'
        ('euthanized', 'Euthanized'),  # Eutanasiado por razones médicas, se viene aqui de 'waiting'
        ('aggressive', 'Aggressive'),  # Comportamiento agresivo, no apto para adopción, se viene aqui de 'waiting'
        ('returned', 'Returned'),  # Regresado al albergue después de una adopción, se viene aqui de 'adopted', el admin lo puede pasar a 'waiting'
    ]

    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    breed = models.CharField(max_length=100)
    kind = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Adoption(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    date = models.DateTimeField(auto_now_add=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'volunteer'},
        related_name='adoptions_volunteer'
    )
    adopter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'adopter'},
        related_name='adoptions_adopter'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return (f'Adoption of {self.animal.name} by {self.adopter.first_name} {self.adopter.last_name} '
                f'and registered by {self.volunteer.first_name} {self.volunteer.last_name}')