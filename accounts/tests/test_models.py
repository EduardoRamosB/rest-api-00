import pytest
from django.db import IntegrityError

from accounts.factories import CustomUserFactory
from accounts.models import CustomUser


@pytest.mark.django_db
def test_create_custom_user():
    # Prueba la creación de un CustomUser con un correo electrónico válido
    user = CustomUserFactory(email='testuser@example.com', username='testuser', role='adopter')
    user.set_password('password123')
    user.save()

    assert user.email == 'testuser@example.com'
    assert user.username == 'testuser'
    assert user.role == 'adopter'
    assert user.check_password('password123')
    assert str(user) == 'testuser@example.com'

@pytest.mark.django_db
def test_user_email_uniqueness():
    # Prueba que el correo electrónico sea único
    CustomUserFactory(email='unique@example.com', username='user1', role='adopter')

    with pytest.raises(IntegrityError):
        CustomUserFactory(email='unique@example.com', username='user2', role='adopter')

@pytest.mark.django_db
def test_user_str_method():
    # Prueba el metodo __str__ del CustomUser
    user = CustomUserFactory(email='testuser@example.com', username='testuser', role='volunteer')
    user.set_password('password123')
    user.save()

    assert str(user) == 'testuser@example.com'

@pytest.mark.django_db
def test_user_role_choices():
    # Prueba las opciones de rol
    roles = dict(CustomUser.ROLE_CHOICES)
    user_admin = CustomUserFactory(email='admin@example.com', username='admin', role='admin')
    user_volunteer = CustomUserFactory(email='volunteer@example.com', username='volunteer', role='volunteer')
    user_adopter = CustomUserFactory(email='adopter@example.com', username='adopter', role='adopter')

    user_admin.set_password('password123')
    user_volunteer.set_password('password123')
    user_adopter.set_password('password123')
    user_admin.save()
    user_volunteer.save()
    user_adopter.save()

    assert user_admin.role == 'admin'
    assert user_volunteer.role == 'volunteer'
    assert user_adopter.role == 'adopter'
    assert all(role in roles for role in [user_admin.role, user_volunteer.role, user_adopter.role])
