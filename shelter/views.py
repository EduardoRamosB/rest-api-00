from django.shortcuts import render
from rest_framework import viewsets

from shelter.models import Animal, Adoption
from shelter.serializers import AnimalSerializer, AdoptionSerializer


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer


class AdoptionViewSet(viewsets.ModelViewSet):
    queryset = Adoption.objects.all()
    serializer_class = AdoptionSerializer
