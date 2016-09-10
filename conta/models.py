from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from girocomercial.models import Giro


class PersonaJuridica(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    razon_social = models.CharField(max_length=300, blank=True)
    rut = models.CharField(max_length=25, unique=True)
    giro = models.ForeignKey(Giro, on_delete=models.DO_NOTHING)
    direccion = models.CharField('dirección', max_length=300)
    telefono = models.CharField('teléfono', max_length=30)
    contacto = models.CharField(max_length=500, blank=True, default='')
    url = models.URLField('página web', blank=True, default='')

    def __str__(self):
        return '{} {}'.format(self.rut, self.nombre)


class Proveedor(models.Model):
    persona_juridica = models.ForeignKey(PersonaJuridica, on_delete=models.CASCADE)


class Cliente(PersonaJuridica):
    persona_juridica = models.ForeignKey(PersonaJuridica, on_delete=models.CASCADE)


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=1000, blank=True)
    precio_compra = models.FloatField()
    precio_venta = models.FloatField()

    def __str__(self):
        return self.nombre


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nombre


class Documento(models.Model):
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.DO_NOTHING)
    numero = models.IntegerField('número')
    neto = models.FloatField()
    iva = models.FloatField()

    class Meta:
        abstract = True

    @property
    def total(self):
        return int(self.neto + self.iva)


class DocumentoVenta(Documento):
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    detalle = GenericRelation(DetalleDocumento)

    class Meta:
        unique_together = 'tipo_documento', 'numero'


class DocumentoProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.DO_NOTHING)
    detalle = GenericRelation(DetalleDocumento)

    class Meta:
        unique_together = 'tipo_documento', 'proveedor', 'numero'


class DetalleDocumento(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    cantidad = models.PositiveIntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    precio_unidad = models.FloatField()

    def __str__(self):
        return '{} unidades de {} a ${} c/u'.format(self.cantidad, self.producto, self.precio_unidad)

    @property
    def total(self):
        return self.cantidad * self.precio_unidad