from rest_framework import serializers

from accounts.models import CustomUser
from shelter.models import Animal, Adoption


class AnimalSerializer(serializers.ModelSerializer):
    created_by_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='created_by',
                                                       write_only=True, required=False)
    updated_by_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='updated_by',
                                                       write_only=True)

    created_by = serializers.ReadOnlyField(source='created_by.email')
    updated_by = serializers.ReadOnlyField(source='updated_by.email')

    class Meta:
        model = Animal
        fields = ['id', 'name', 'age', 'breed', 'kind', 'status', 'reason', 'created_at', 'updated_at', 'created_by_id',
                  'updated_by_id', 'created_by', 'updated_by']

    def update(self, instance, validated_data):
        validated_data.pop('created_by', None)
        return super().update(instance, validated_data)


class AdoptionSerializer(serializers.ModelSerializer):
    created_by_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='created_by',
                                                       write_only=True, required=False)
    updated_by_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='updated_by',
                                                       write_only=True)

    created_by = serializers.ReadOnlyField(source='created_by.email')
    updated_by = serializers.ReadOnlyField(source='updated_by.email')

    class Meta:
        model = Adoption
        fields = ['id', 'date', 'animal', 'volunteer', 'adopter', 'status', 'created_at', 'updated_at',
                  'created_by_id', 'updated_by_id', 'created_by', 'updated_by']

    def update(self, instance, validated_data):
        validated_data.pop('created_by', None)
        return super().update(instance, validated_data)