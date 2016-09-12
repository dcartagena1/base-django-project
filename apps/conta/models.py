from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from apps.girocomercial.models import Giro


class PersonaJuridica(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    razon_social = models.CharField(max_length=300, blank=True)
    rut = models.CharField(max_length=25, unique=True)
    giro = models.ForeignKey(Giro, on_delete=models.DO_NOTHING)
    direccion = models.CharField('dirección', max_length=300)
    telefono = models.CharField('teléfono', max_length=30)
    contacto = models.CharField(max_length=500, blank=True, default='')
    url = models.URLField('página web', blank=True, default='')

    class Meta:
        verbose_name = "Persona Jurídica"
        verbose_name_plural = "Personas Jurídicas"

    def __str__(self):
        return '{} {}'.format(self.rut, self.nombre)


class Proveedor(models.Model):
    persona_juridica = models.ForeignKey(
        PersonaJuridica,
        on_delete=models.CASCADE,
        related_name='como_proveedor',
    )

    class Meta:
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return str(self.persona_juridica)

    @property
    def nombre(self):
        return self.persona_juridica.nombre


class Cliente(models.Model):
    persona_juridica = models.ForeignKey(
        PersonaJuridica,
        on_delete=models.CASCADE,
        related_name='como_cliente',
    )

    def __str__(self):
        return str(self.persona_juridica)

    @property
    def nombre(self):
        return self.persona_juridica.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=1000, blank=True)
    precio_compra = models.FloatField()
    precio_venta = models.FloatField()

    def __str__(self):
        return self.nombre


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = "tipo de documento"
        verbose_name_plural = "tipos de documento"

    def __str__(self):
        return self.nombre


class Documento(models.Model):
    tipo_documento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.DO_NOTHING,
    )
    numero = models.IntegerField('número')
    neto = models.FloatField()
    iva = models.FloatField()

    class Meta:
        abstract = True

    @property
    def total(self):
        return int(self.neto + self.iva)

    def __str__(self):
        return '{} {} por {}'.format(
            str(self.tipo_documento),
            self.numero,
            self.total,
        )


class DetalleDocumento(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    cantidad = models.PositiveIntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    precio_unidad = models.FloatField()

    class Meta:
        verbose_name = 'detalle de documento'
        verbose_name_plural = 'detalles de documentos'

    def __str__(self):
        return '{} unidades de {} a ${} c/u'\
            .format(self.cantidad, self.producto, self.precio_unidad)

    @property
    def total(self):
        return self.cantidad * self.precio_unidad

class DocumentoVenta(Documento):
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    detalle = GenericRelation(DetalleDocumento)

    class Meta:
        unique_together = 'tipo_documento', 'numero'
        verbose_name = "documento de venta"
        verbose_name_plural = "documentos de venta"

    def __str__(self):
        return '{} a {}'.format(
            super(DocumentoVenta, self).__str__(),
            self.cliente.nombre,
        )


class DocumentoProveedor(Documento):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.DO_NOTHING)
    detalle = GenericRelation(DetalleDocumento)

    class Meta:
        unique_together = 'tipo_documento', 'proveedor', 'numero'
        verbose_name = "documento de proveedor"
        verbose_name_plural = "documentos de proveedor"

    def __str__(self):
        return '{} de {}'.format(
            super(DocumentoProveedor, self).__str__(),
            self.proveedor.nombre,
        )
