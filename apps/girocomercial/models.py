from django.db import models


class ClaseGiro(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
      return self.nombre

    class Meta:
        verbose_name        = "Clase de Giro"
        verbose_name_plural = "Clases de Giro"

class CategoriaGiro(models.Model):
    clase  = models.ForeignKey(ClaseGiro, related_name="categorias")
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría de Giro"
        verbose_name_plural = "Categorías de Giro"


class Giro(models.Model):
    categoria_giro = models.ForeignKey(CategoriaGiro, related_name="giros")
    codigo = models.IntegerField("Código")
    nombre = models.CharField(max_length=100, unique=True)
    afecto_iva = models.NullBooleanField(default=True)
    categoria_tributaria = models.CharField("Categoría Tributaria", max_length=1, choices=(('1','1'),('2','2'),('3','ND')))
    disponible_internet = models.BooleanField(default=True)

    def __str__(self):
        return str(self.codigo) + ": " + self.nombre

    class Meta:
        verbose_name = "Giro Comercial"
        verbose_name_plural = "Giros Comerciales"
