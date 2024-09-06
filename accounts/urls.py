from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView, UserInfoAPIView, \
    VolunteerListCreateAPIView, VolunteerRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register-user'),
    path('login/', UserLoginAPIView.as_view(), name='login-user'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('user_info/', UserInfoAPIView.as_view(), name='user-info'),
    path('volunteers/', VolunteerListCreateAPIView.as_view(), name='volunteer-list-create'),
    path('volunteers/<int:pk>/', VolunteerRetrieveUpdateDestroyAPIView.as_view(), name='volunteer-retrieve-update-destroy'),
]