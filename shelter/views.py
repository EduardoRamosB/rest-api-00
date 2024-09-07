from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from accounts.models import CustomUser
from shelter.models import Animal, Adoption
from shelter.serializers import AnimalSerializer, AdoptionCreateSerializer, AdoptionDetailSerializer

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def get_queryset(self):
        role = self.request.query_params.get('role')

        if role == 'admin' or role == 'volunteer':
            return Animal.objects.all().order_by('-created_at')
        elif role == 'adopter':
            return Animal.objects.filter(status='available').order_by('-created_at')
        else:
            return Animal.objects.none()

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
        updated_by = get_object_or_404(CustomUser, id=updated_by_id)
        serializer.save(updated_by=updated_by)


class AdoptionViewSet(viewsets.ModelViewSet):
    queryset = Adoption.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AdoptionDetailSerializer
        return AdoptionCreateSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        role = self.request.query_params.get('role')

        if self.action in ['list', 'retrieve']:
            if role == 'admin' or role == 'volunteer':
                return Adoption.objects.all().order_by('-created_at')
            elif role == 'adopter':
                if not user_id:
                    raise ValidationError("User ID is required for role 'adopter'.")
                return Adoption.objects.filter(adopter_id=user_id).order_by('-created_at')
            else:
                return Adoption.objects.none()
        return Adoption.objects.all().order_by('-created_at')


    def perform_create(self, serializer):
        created_by_id = self.request.data.get('created_by_id')
        updated_by_id = self.request.data.get('updated_by_id')
        animal_id = self.request.data.get('animal')

        if not created_by_id:
            raise ValidationError("Created By ID is required.")
        if not updated_by_id:
            raise ValidationError("Updated By ID is required.")
        if not animal_id:
            raise ValidationError("Animal ID is required.")

        created_by = get_object_or_404(CustomUser, id=created_by_id)
        updated_by = get_object_or_404(CustomUser, id=updated_by_id)
        animal = get_object_or_404(Animal, id=animal_id)

        serializer.save(
            created_by=created_by,
            updated_by=updated_by,
            date=timezone.now()
        )

        animal.status = 'requested'
        animal.save()

    def perform_update(self, serializer):
        updated_by_id = self.request.data.get('updated_by_id')
        if not updated_by_id:
            raise ValidationError("Updated By ID is required.")

        updated_by = get_object_or_404(CustomUser, id=updated_by_id)
        status = self.request.data.get('status')

        if status:
            if status not in dict(Adoption.STATUS_CHOICES).keys():
                raise ValidationError("Invalid status value")

            # Save the adoption with the updated status
            serializer.save(updated_by=updated_by)

            # Update the animal status based on the adoption status
            animal = get_object_or_404(Animal, id=serializer.instance.animal.id)

            if status == 'in_progress':
                animal.status = 'pending'
            elif status == 'completed':
                animal.status = 'adopted'
            else:
                # If the status is not 'in_progress' or 'completed', don't change the animal status
                pass

            animal.save()
