from django.urls import path
from .views import kpi_data

urlpatterns = [
    path('data/', kpi_data, name='kpi_data'),
]
