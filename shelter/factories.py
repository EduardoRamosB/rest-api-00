import factory
from django.contrib.auth import get_user_model
from shelter.models import Animal, Adoption

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = factory.Iterator(['admin', 'adopter', 'volunteer'])

class AnimalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Animal

    name = factory.Faker('word')
    age = factory.Faker('random_int', min=1, max=15)
    breed = factory.Faker('word')
    kind = factory.Faker('word')
    status = factory.Iterator(['available', 'adopted', 'pending'])
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SubFactory(UserFactory)

class AdoptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Adoption

    animal = factory.SubFactory(AnimalFactory)
    adopter = factory.SubFactory(UserFactory)
    volunteer = factory.SubFactory(UserFactory)
    status = factory.Iterator(['requested', 'in_progress', 'completed'])
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SubFactory(UserFactory)
