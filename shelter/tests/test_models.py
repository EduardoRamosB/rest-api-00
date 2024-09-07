from django.test import TestCase
from django.db import IntegrityError
from shelter.factories import UserFactory, AnimalFactory, AdoptionFactory

class AnimalModelTests(TestCase):

    def setUp(self):
        # Crea usuarios y un animal usando factories
        self.created_by = UserFactory()
        self.updated_by = UserFactory()
        self.animal = AnimalFactory(created_by=self.created_by, updated_by=self.updated_by)

    def test_animal_creation(self):
        # Verifica que el animal se crea con los datos correctos
        self.assertEqual(self.animal.name, self.animal.name)
        self.assertEqual(self.animal.age, self.animal.age)
        self.assertEqual(self.animal.breed, self.animal.breed)
        self.assertEqual(self.animal.kind, self.animal.kind)
        self.assertEqual(self.animal.status, self.animal.status)
        self.assertEqual(self.animal.created_by, self.created_by)
        self.assertEqual(self.animal.updated_by, self.updated_by)

    def test_animal_str_method(self):
        # Verifica que el metodo __str__() devuelve el nombre del animal
        self.assertEqual(str(self.animal), self.animal.name)

    def test_animal_unique_constraints(self):
        # Verifica que se lanza una excepción si se intenta crear un animal duplicado
        try:
            AnimalFactory(name=self.animal.name, age=self.animal.age, breed=self.animal.breed, kind=self.animal.kind, created_by=self.created_by, updated_by=self.updated_by)
        except IntegrityError as e:
            self.assertIn('UNIQUE constraint failed', str(e))

class AdoptionModelTests(TestCase):

    def setUp(self):
        # Crea usuarios, un animal y una adopcion usando factories
        self.adopter = UserFactory(role='adopter')
        self.volunteer = UserFactory(role='volunteer')
        self.admin = UserFactory(role='admin')
        self.animal = AnimalFactory(created_by=self.admin, updated_by=self.admin)
        self.adoption = AdoptionFactory(animal=self.animal, adopter=self.adopter, volunteer=self.volunteer, created_by=self.admin, updated_by=self.admin)

    def test_adoption_creation(self):
        # Verifica que la adopción se crea con los datos correctos
        self.assertEqual(self.adoption.animal, self.animal)
        self.assertEqual(self.adoption.adopter, self.adopter)
        self.assertEqual(self.adoption.volunteer, self.volunteer)
        self.assertEqual(self.adoption.status, self.adoption.status)
        self.assertEqual(self.adoption.created_by, self.admin)
        self.assertEqual(self.adoption.updated_by, self.admin)

    def test_adoption_str_method(self):
        # Verifica que el metodo __str__() devuelve la descripcion correcta de la adopcion
        expected_str = f'Adoption of {self.animal.name} by {self.adopter.first_name} {self.adopter.last_name} and registered by {self.volunteer.first_name}'
        self.assertEqual(str(self.adoption), expected_str)

    def test_adoption_unique_constraints(self):
        # Verifica que se lanza una excepcion si se intenta crear una adopcion duplicada
        try:
            AdoptionFactory(animal=self.animal, adopter=self.adopter, volunteer=self.volunteer, created_by=self.admin, updated_by=self.admin)
        except IntegrityError as e:
            self.assertIn('UNIQUE constraint failed', str(e))
