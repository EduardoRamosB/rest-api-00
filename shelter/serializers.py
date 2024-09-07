from rest_framework import serializers
from accounts.models import CustomUser
from shelter.models import Animal, Adoption

class AnimalSerializer(serializers.ModelSerializer):
    created_by_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='created_by',
                                                       write_only=True, required=False)
    updated_by_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='updated_by',
                                                       write_only=True)

    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    class Meta:
        model = Animal
        fields = ['id', 'name', 'age', 'breed', 'kind', 'status', 'reason', 'created_at', 'updated_at', 'created_by_id',
                  'updated_by_id', 'created_by', 'updated_by']

    def get_created_by(self, obj):
        if obj.created_by.first_name and obj.created_by.last_name:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}"
        return obj.created_by.username

    def get_updated_by(self, obj):
        if obj.updated_by.first_name and obj.updated_by.last_name:
            return f"{obj.updated_by.first_name} {obj.updated_by.last_name}"
        return obj.updated_by.username

    def update(self, instance, validated_data):
        validated_data.pop('created_by', None)
        return super().update(instance, validated_data)

class CustomUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.first_name and obj.last_name else obj.username

class AdoptionCreateSerializer(serializers.ModelSerializer):
    animal = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all())
    adopter = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    volunteer = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='volunteer'),
        write_only=True,
        allow_null=True,
        required=False
    )
    created_by_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='created_by', write_only=True, required=False)
    updated_by_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='updated_by', write_only=True, required=False)
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    class Meta:
        model = Adoption
        fields = ['id', 'date', 'animal', 'volunteer', 'adopter', 'status', 'created_at', 'updated_at',
                  'created_by_id', 'updated_by_id', 'created_by', 'updated_by']

    def validate_status(self, value):
        if value not in dict(self.Meta.model.STATUS_CHOICES).keys():
            raise serializers.ValidationError("Invalid status value")
        return value

    def get_created_by(self, obj):
        if obj.created_by.first_name and obj.created_by.last_name:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}"
        return obj.created_by.username

    def get_updated_by(self, obj):
        if obj.updated_by.first_name and obj.updated_by.last_name:
            return f"{obj.updated_by.first_name} {obj.updated_by.last_name}"
        return obj.updated_by.username


class AdoptionDetailSerializer(serializers.ModelSerializer):
    animal = AnimalSerializer()  # Usar el AnimalSerializer para detalles completos del animal
    adopter = CustomUserSerializer()  # Usar el CustomUserSerializer para detalles del adoptante
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    volunteer = CustomUserSerializer()  # Para mostrar detalles del volunteer si es necesario

    class Meta:
        model = Adoption
        fields = ['id', 'date', 'animal', 'volunteer', 'adopter', 'status', 'created_at', 'updated_at',
                  'created_by_id', 'updated_by_id', 'created_by', 'updated_by']

    def get_created_by(self, obj):
        if obj.created_by.first_name and obj.created_by.last_name:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}"
        return obj.created_by.username

    def get_updated_by(self, obj):
        if obj.updated_by.first_name and obj.updated_by.last_name:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}"
        return obj.updated_by.username
