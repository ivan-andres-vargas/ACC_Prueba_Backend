from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PeliculaViewSet, SummaryView, SummaryView2, PeliculaGeoJSONView

# Router para el servicio de peliculas
router = DefaultRouter()
router.register(r'movies', PeliculaViewSet)

# Rutas para el servicio de peliculas
urlpatterns = [
    path('', include(router.urls)),
    path('summary/', SummaryView.as_view()),  # Servicio de resumen de peliculas según los requerimientos
    path('summary02/', SummaryView2.as_view()),  # Servicio de resumen de peliculas adicional
    path('geojson/', PeliculaGeoJSONView.as_view(), name='location_geojson_list'), # Servicio geolocalización de
    # peliculas
]
