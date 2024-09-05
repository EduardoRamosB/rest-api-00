from rest_framework import serializers

from shelter.models import Animal, Adoption


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'name', 'age', 'breed', 'kind', 'status', 'reason', 'created_at', 'updated_at']


class AdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = ['id', 'date', 'animal', 'volunteer', 'adopter', 'status', 'created_at', 'updated_at']