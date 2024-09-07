import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from accounts.models import CustomUser


@pytest.mark.django_db
def test_create_custom_user():
    # Prueba la creación de un CustomUser con un correo electrónico válido
    user = CustomUser.objects.create_user(email='testuser@example.com', username='testuser', password='password123', role='adopter')
    assert user.email == 'testuser@example.com'
    assert user.username == 'testuser'
    assert user.role == 'adopter'
    assert user.check_password('password123')
    assert str(user) == 'testuser@example.com'


@pytest.mark.django_db
def test_user_email_uniqueness():
    # Prueba que el correo electrónico sea único
    CustomUser.objects.create_user(email='unique@example.com', username='user1', password='password123')

    with pytest.raises(IntegrityError):
        CustomUser.objects.create_user(email='unique@example.com', username='user2', password='password123')

@pytest.mark.django_db
def test_user_str_method():
    # Prueba el metodo __str__ del CustomUser
    user = CustomUser.objects.create_user(email='testuser@example.com', username='testuser', password='password123', role='volunteer')
    assert str(user) == 'testuser@example.com'

@pytest.mark.django_db
def test_user_role_choices():
    # Prueba las opciones de rol
    roles = dict(CustomUser.ROLE_CHOICES)
    user_admin = CustomUser.objects.create_user(email='admin@example.com', username='admin', password='password123', role='admin')
    user_volunteer = CustomUser.objects.create_user(email='volunteer@example.com', username='volunteer', password='password123', role='volunteer')
    user_adopter = CustomUser.objects.create_user(email='adopter@example.com', username='adopter', password='password123', role='adopter')

    assert user_admin.role == 'admin'
    assert user_volunteer.role == 'volunteer'
    assert user_adopter.role == 'adopter'
    assert all(role in roles for role in [user_admin.role, user_volunteer.role, user_adopter.role])