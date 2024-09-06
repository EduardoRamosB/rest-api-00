from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from accounts.models import CustomUser
from shelter.models import Animal, Adoption
from shelter.serializers import AnimalSerializer, AdoptionSerializer


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def perform_create(self, serializer):
        created_by_id = self.request.data.get('created_by_id')
        updated_by_id = self.request.data.get('updated_by_id')

        if not created_by_id:
            raise ValidationError("Created By ID is required.")
        if not updated_by_id:
            raise ValidationError("Updated By ID is required.")

        created_by = get_object_or_404(CustomUser, id=created_by_id)
        updated_by = get_object_or_404(CustomUser, id=updated_by_id)

        serializer.save(created_by=created_by, updated_by=updated_by)


class AdoptionViewSet(viewsets.ModelViewSet):
    queryset = Adoption.objects.all()
    serializer_class = AdoptionSerializer

    def perform_create(self, serializer):
        created_by_id = self.request.data.get('created_by_id')
        updated_by_id = self.request.data.get('updated_by_id')

        if not created_by_id:
            raise ValidationError("Created By ID is required.")
        if not updated_by_id:
            raise ValidationError("Updated By ID is required.")

        created_by = get_object_or_404(CustomUser, id=created_by_id)
        updated_by = get_object_or_404(CustomUser, id=updated_by_id)

        serializer.save(created_by=created_by, updated_by=updated_by)

    def perform_update(self, serializer):
        updated_by_id = self.request.data.get('updated_by_id')

        if not updated_by_id:
            raise ValidationError("Updated By ID is required.")

        updated_by = get_object_or_404(CustomUser, id=updated_by_id)

        serializer.save(updated_by=updated_by)
