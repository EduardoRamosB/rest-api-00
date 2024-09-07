from rest_framework.decorators import api_view
from rest_framework.response import Response
from shelter.models import Animal, Adoption


@api_view(['GET'])
def kpi_data(request):
    # KPI 1: Perros en el albergue (que no están adoptados o eutanasiados)
    dogs_count = Animal.objects.filter(kind='dog').exclude(status__in=['adopted', 'euthanized']).count()

    # KPI 2: Gatos en el albergue (que no están adoptados o eutanasiados)
    cats_count = Animal.objects.filter(kind='cat').exclude(status__in=['adopted', 'euthanized']).count()

    # KPI 3: Adopciones en progreso por tipo de animal
    adoptions_in_progress_dog = Adoption.objects.filter(status='in_progress', animal__kind='dog').count()
    adoptions_in_progress_cat = Adoption.objects.filter(status='in_progress', animal__kind='cat').count()

    # KPI 4: Adopciones completadas por tipo de animal
    adoptions_completed_dog = Adoption.objects.filter(status='completed', animal__kind='dog').count()
    adoptions_completed_cat = Adoption.objects.filter(status='completed', animal__kind='cat').count()

    # Retornar los datos en formato JSON
    return Response({
        'dogs_count': dogs_count,
        'cats_count': cats_count,
        'adoptions_in_progress': {
            'dog': adoptions_in_progress_dog,
            'cat': adoptions_in_progress_cat,
        },
        'adoptions_completed': {
            'dog': adoptions_completed_dog,
            'cat': adoptions_completed_cat,
        },
    })
