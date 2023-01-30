
# Validadores de campos
from django.core.validators import MaxValueValidator, MinValueValidator

# Modelos de Django
from django.db import models


# Clase Pelicula que hereda de la clase models.Model
# Creamos la clase de la tabla de la base de datos
class Pelicula(models.Model):
    titulo = models.CharField(max_length=100)
    # Por optimizacion de la base de datos, solo se permite un valor de 1 a 5,
    calificacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    pais = models.CharField(max_length=25)
    # Null y blank para que no sea obligatorio y adelante se pueda agregar con el pais de origen
    ubicacion = models.PointField()
