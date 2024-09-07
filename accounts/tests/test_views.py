import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.factories import CustomUserFactory
from accounts.models import CustomUser

@pytest.mark.django_db
def test_user_registration_view():
    # Prueba la creación de un usuario a través de la vista de registro
    client = APIClient()
    data = {
        'email': 'newuser@example.com',
        'username': 'newuser',
        'password': 'password123',
        'password_confirmation': 'password123'
    }
    response = client.post('/api/register/', data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'tokens' in response.data
    assert response.data['email'] == data['email']
    assert response.data['username'] == data['username']

@pytest.mark.django_db
def test_user_login_view():
    # Prueba el inicio de sesión del usuario a través de la vista de inicio de sesión
    user = CustomUserFactory(password='password123')
    client = APIClient()
    data = {
        'email': user.email,
        'password': 'password123'
    }
    response = client.post('/api/login/', data, format='json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_role_list_create_view():
    # Prueba la lista y creación de usuarios filtrados por rol
    user = CustomUserFactory(role='admin', password='password123')
    client = APIClient()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    # Datos para crear un nuevo usuario
    data = {
        'email': 'newroleuser@example.com',
        'username': 'newroleuser',
        'password': 'password123',
        'password_confirmation': 'password123'
    }

    # Endpoint para crear un nuevo usuario con el rol 'adopter'
    response = client.post('/api/users/adopter/', data, format='json')

    # Verificar que la respuesta sea 201 Created
    assert response.status_code == status.HTTP_201_CREATED

    # Verificar los detalles del usuario creado
    assert response.data['email'] == data['email']
    assert response.data['username'] == data['username']


@pytest.mark.django_db
def test_user_role_retrieve_update_destroy_view():
    # Prueba la recuperación, actualización y eliminación de un usuario por rol
    user = CustomUserFactory(role='volunteer', password='password123')
    client = APIClient()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    # Prueba la recuperación del usuario
    response = client.get(f'/api/users/volunteer/{user.id}/')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_user_logout_view():
    # Prueba el cierre de sesión del usuario a través de la vista de cierre de sesión
    user = CustomUserFactory(password='password123')
    client = APIClient()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    # Prueba el cierre de sesión
    response = client.post('/api/logout/', {'refresh': str(token)}, format='json')
    assert response.status_code == status.HTTP_205_RESET_CONTENT

@pytest.mark.django_db
def test_user_info_view():
    # Prueba la visualización de la información del usuario autenticado
    user = CustomUserFactory(password='password123')
    client = APIClient()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    # Prueba la recuperación de la información del usuario autenticado
    response = client.get('/api/user_info/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == user.email


@pytest.mark.django_db
def test_user_update_view():
    # Prueba para actualizar un user
    user = CustomUserFactory(role='admin', password='password123')
    client = APIClient()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    # Crear un nuevo usuario
    new_user = CustomUserFactory(role='adopter', password='password123')

    # Datos para actualizar el usuario
    data = {
        'email': 'updatedemail@example.com',
        'username': 'updatedusername',
        'password': 'newpassword123',
        'password_confirmation': 'newpassword123'
    }

    response = client.put(f'/api/users/adopter/{new_user.id}/', data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == data['email']
    assert response.data['username'] == data['username']


@pytest.mark.django_db
def test_user_delete_view():
    # Prueba para borrar un user
    user = CustomUserFactory(role='admin', password='password123')
    client = APIClient()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    # Crear un nuevo usuario
    user_to_delete = CustomUserFactory(role='adopter', password='password123')

    response = client.delete(f'/api/users/adopter/{user_to_delete.id}/')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not CustomUser.objects.filter(id=user_to_delete.id).exists()