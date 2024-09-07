# accounts/tests/test_serializers.py
import pytest
from rest_framework.exceptions import ValidationError
from accounts.serializers import CustomUserSerializer, UserRegistrationSerializer, UserLoginSerializer
from accounts.factories import CustomUserFactory


@pytest.mark.django_db
def test_custom_user_serializer():
    # Prueba la serialización del CustomUser
    user = CustomUserFactory()
    serializer = CustomUserSerializer(user)
    data = serializer.data

    assert data['email'] == user.email
    assert data['username'] == user.username
    assert data['role'] == user.role
    assert data[
               'full_name'] == f"{user.first_name} {user.last_name}" if user.first_name and user.last_name else user.username


@pytest.mark.django_db
def test_custom_user_serializer_update():
    # Prueba la actualización de un CustomUser a través del serializer
    user = CustomUserFactory()
    serializer = CustomUserSerializer(instance=user,
                                      data={'first_name': 'New', 'last_name': 'Name', 'password': 'newpassword123'},
                                      partial=True)
    assert serializer.is_valid()
    updated_user = serializer.save()

    assert updated_user.first_name == 'New'
    assert updated_user.last_name == 'Name'
    assert updated_user.check_password('newpassword123')


@pytest.mark.django_db
def test_user_registration_serializer_valid_data():
    # Prueba la validación y creación de un usuario con datos válidos
    data = {
        'email': 'register@example.com',
        'username': 'registeruser',
        'password': 'password123',
        'password_confirmation': 'password123'
    }
    serializer = UserRegistrationSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()

    assert user.email == data['email']
    assert user.username == data['username']
    assert user.check_password(data['password'])


@pytest.mark.django_db
def test_user_registration_serializer_invalid_password_confirmation():
    # Prueba la validación con confirmación de contraseña incorrecta
    data = {
        'email': 'register@example.com',
        'username': 'registeruser',
        'password': 'password123',
        'password_confirmation': 'differentpassword'
    }
    serializer = UserRegistrationSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Passwords do not match' in serializer.errors['non_field_errors']


@pytest.mark.django_db
def test_user_registration_serializer_short_password():
    # Prueba la validación con una contraseña demasiado corta
    data = {
        'email': 'register@example.com',
        'username': 'registeruser',
        'password': 'short',
        'password_confirmation': 'short'
    }
    serializer = UserRegistrationSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Password must be at least 8 characters' in serializer.errors['non_field_errors']


@pytest.mark.django_db
def test_user_login_serializer_valid_data():
    # Prueba el inicio de sesión con credenciales válidas
    user = CustomUserFactory(password='password123')
    data = {'email': user.email, 'password': 'password123'}
    serializer = UserLoginSerializer(data=data)
    assert serializer.is_valid()
    authenticated_user = serializer.validate(data)
    assert authenticated_user == user


@pytest.mark.django_db
def test_user_login_serializer_invalid_credentials():
    # Prueba el inicio de sesión con credenciales inválidas
    data = {'email': 'nonexistent@example.com', 'password': 'wrongpassword'}
    serializer = UserLoginSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.validate(data)
