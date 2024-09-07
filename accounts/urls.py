from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView, UserInfoAPIView, \
    VolunteerListCreateAPIView, VolunteerRetrieveUpdateDestroyAPIView, AdopterListCreateAPIView, \
    AdopterRetrieveUpdateDestroyAPIView, UserRoleListCreateAPIView, UserRoleRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register-user'),
    path('login/', UserLoginAPIView.as_view(), name='login-user'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('user_info/', UserInfoAPIView.as_view(), name='user-info'),
    path('volunteers/', VolunteerListCreateAPIView.as_view(), name='volunteer-list-create'),
    path('volunteers/<int:pk>/', VolunteerRetrieveUpdateDestroyAPIView.as_view(), name='volunteer-retrieve-update-destroy'),
    path('adopters/', AdopterListCreateAPIView.as_view(), name='adopter-list-create'),
    path('adopters/<int:pk>/', AdopterRetrieveUpdateDestroyAPIView.as_view(), name='adopter-retrieve-update-destroy'),
    # Ruta genérica para crear/listar usuarios con rol
    path('users/<str:role>/', UserRoleListCreateAPIView.as_view(), name='user-role-list-create'),
    # Ruta genérica para recuperar/actualizar/eliminar usuarios con rol
    path('users/<str:role>/<int:pk>/', UserRoleRetrieveUpdateDestroyAPIView.as_view(), name='user-role-retrieve-update-destroy'),
]