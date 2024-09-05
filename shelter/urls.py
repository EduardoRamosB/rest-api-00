from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnimalViewSet, AdopterViewSet


router = DefaultRouter()
router.register(r'animals', AnimalViewSet)
router.register(r'adopters', AdopterViewSet)

urlpatterns = [
    path('', include('shelter.urls')),
]