# Modelos y serializadores
from rest_framework.decorators import api_view

from .models import Pelicula
from .serializers import PeliculaSerializer

# Modulos de Django Rest Framework
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

# Modulos de Django Filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

# Modulos de Django de manejo de datos
from django.db.models import Count, Q

# Importación GeoPy
from geopy.geocoders import Nominatim


# Clase para poder filtrar de manera exacta por titulo, tambien se puede filtrar por calificacion y pais.
class PeliculaFilter(filters.FilterSet):
    titulo = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Pelicula
        fields = ['titulo', 'calificacion', 'pais']


# Clase PeliculaViewSet para el servicio de peliculas
class PeliculaViewSet(viewsets.ModelViewSet):
    queryset = Pelicula.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PeliculaSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PeliculaFilter
    pagination_class = PageNumberPagination
    ordering_fields = ['titulo', 'calificacion', 'pais']

    # Función para crear una pelicula y devolver un mensaje de éxito o error
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"success": True, "data": serializer.data}, status=201, headers=headers)
        except:
            return Response({"success": False, "error": "Error al crear la pelicula"})

    # Función para actualizar una pelicula y devolver un mensaje de éxito o error
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({"success": True, "data": serializer.data})
        except:
            return Response({"success": False, "error": "Error al actualizar la pelicula"})


# Clase para poder hacer las peticiones GET y devolver un resumen de la base de datos de peliculas según los
# requerimientos
class SummaryView(APIView):
    def get(self, request):
        pais = Pelicula.objects.values('pais').annotate(count=Count('id'))
        calificacion = Pelicula.objects.values('calificacion').annotate(count=Count('id'))
        top_movies = Pelicula.objects.order_by('-calificacion').values()[:5]
        data = {
            'count_pais': len(pais),
            'count_calificacion_1': calificacion.filter(calificacion=1).count(),
            'count_calificacion_2': calificacion.filter(calificacion=2).count(),
            'count_calificacion_3': calificacion.filter(calificacion=3).count(),
            'count_calificacion_4': calificacion.filter(calificacion=4).count(),
            'count_calificacion_5': calificacion.filter(calificacion=5).count(),
        }

        return Response({'success': True, 'data': data})


# Clase adicional al requerimiento para poder hacer las peticiones GET y devolver un resumen de los paises y sus
# calificaciones
class SummaryView2(APIView):
    def get(self, request):
        pais = Pelicula.objects.values('pais').annotate(
            count_calificacion_1=Count('id', filter=Q(calificacion=1)),
            count_calificacion_2=Count('id', filter=Q(calificacion=2)),
            count_calificacion_3=Count('id', filter=Q(calificacion=3)),
            count_calificacion_4=Count('id', filter=Q(calificacion=4)),
            count_calificacion_5=Count('id', filter=Q(calificacion=5)),
        )
        return Response({'success': True, 'data': pais})


# GeoLocalización no se pudo implementar con djangorestframework-gis, problemas de incompatibilidad con windows.
# Quedó en desarrollo, se realizó un prototipo con geopy, se necesitan pruebas y ajustes.

class PeliculaGeoJSONView(ListAPIView):
    def list(self, request, *args, **kwargs):
        geolocator = Nominatim(user_agent="APP_Prueba_Backend")
        peliculas = Pelicula.objects.all()
        feature_list = []
        for pelicula in peliculas:
            location = geolocator.geocode(pelicula.pais)
            feature = {
                "type": "Feature",
                "properties": {
                    "titulo": pelicula.titulo,
                    "calificacion": pelicula.calificacion,
                    "pais": pelicula.pais
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [location.longitude, location.latitude]
                }
            }
            feature_list.append(feature)
        data = {
            "type": "FeatureCollection",
            "features": feature_list
        }
        return Response(data)
