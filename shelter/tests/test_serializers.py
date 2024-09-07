from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from shelter.factories import UserFactory, AnimalFactory, AdoptionFactory
from shelter.serializers import AnimalSerializer, CustomUserSerializer, AdoptionCreateSerializer, AdoptionDetailSerializer
from shelter.models import Animal, Adoption

class AnimalSerializerTests(APITestCase):

    def setUp(self):
        # Crea usuarios y un animal usando fábricas
        self.created_by = UserFactory()
        self.updated_by = UserFactory()
        self.animal = AnimalFactory(created_by=self.created_by, updated_by=self.updated_by)

    def test_animal_serializer(self):
        # Verifica que el AnimalSerializer serializa los datos correctamente
        serializer = AnimalSerializer(self.animal)
        data = serializer.data
        self.assertEqual(data['name'], self.animal.name)
        self.assertEqual(data['age'], self.animal.age)
        self.assertEqual(data['breed'], self.animal.breed)
        self.assertEqual(data['kind'], self.animal.kind)
        self.assertEqual(data['status'], self.animal.status)
        self.assertEqual(data['created_by'], f"{self.created_by.first_name} {self.created_by.last_name}")
        self.assertEqual(data['updated_by'], f"{self.updated_by.first_name} {self.updated_by.last_name}")

    def test_animal_serializer_update(self):
        # Verifica que el método update del AnimalSerializer funciona correctamente
        serializer = AnimalSerializer(instance=self.animal, data={'name': 'Updated Name'}, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_animal = serializer.save()
        self.assertEqual(updated_animal.name, 'Updated Name')

class CustomUserSerializerTests(APITestCase):

    def setUp(self):
        # Crea un usuario usando una fábrica
        self.user = UserFactory()

    def test_custom_user_serializer(self):
        # Verifica que el CustomUserSerializer serializa los datos correctamente
        serializer = CustomUserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data['full_name'], f"{self.user.first_name} {self.user.last_name}")

class AdoptionSerializerTests(APITestCase):

    def setUp(self):
        # Crea usuarios, un animal y una adopción usando fábricas
        self.adopter = UserFactory(role='adopter')
        self.volunteer = UserFactory(role='volunteer')
        self.admin = UserFactory(role='admin')
        self.animal = AnimalFactory(created_by=self.admin, updated_by=self.admin)
        self.adoption = AdoptionFactory(animal=self.animal, adopter=self.adopter, volunteer=self.volunteer, created_by=self.admin, updated_by=self.admin)

    # crear test para test_adoption_create_serializer_with_optional_volunteer

    def test_adoption_create_serializer_without_volunteer(self):
        # Verifica que el AdoptionCreateSerializer maneja correctamente la ausencia de volunteer
        adoption_no_volunteer = AdoptionFactory(animal=self.animal, adopter=self.adopter, created_by=self.admin, updated_by=self.admin, volunteer=None)
        serializer = AdoptionCreateSerializer(adoption_no_volunteer)
        data = serializer.data
        self.assertEqual(data['animal'], self.animal.id)
        self.assertEqual(data['adopter'], self.adopter.id)
        self.assertIsNone(data.get('volunteer'))
        self.assertEqual(data['status'], adoption_no_volunteer.status)
        self.assertEqual(data['created_by'], f"{self.admin.first_name} {self.admin.last_name}")

    def test_adoption_detail_serializer(self):
        # Verifica que el AdoptionDetailSerializer serializa los datos detallados correctamente
        serializer = AdoptionDetailSerializer(self.adoption)
        data = serializer.data
        self.assertEqual(data['animal']['name'], self.animal.name)
        self.assertEqual(data['adopter']['full_name'], f"{self.adopter.first_name} {self.adopter.last_name}")
        self.assertEqual(data['volunteer']['full_name'], f"{self.volunteer.first_name} {self.volunteer.last_name}")
        self.assertEqual(data['status'], self.adoption.status)
        self.assertEqual(data['created_by'], f"{self.admin.first_name} {self.admin.last_name}")
