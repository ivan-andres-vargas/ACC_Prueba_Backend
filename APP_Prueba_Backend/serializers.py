from rest_framework import serializers
from rest_framework.fields import GeometryField
from .models import Pelicula


# Serializers Pelicula.
class PeliculaSerializer(serializers.ModelSerializer):
    ubicacion = GeometryField()

    class Meta:
        model = Pelicula
        fields = ('id', 'titulo', 'calificacion', 'pais', 'ubicacion')
        filter_fields = ['titulo', 'calificacion', 'pais']
