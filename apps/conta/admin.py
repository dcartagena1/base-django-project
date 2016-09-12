from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from apps.conta.models import PersonaJuridica
from apps.conta.models import Proveedor
from apps.conta.models import Cliente
from apps.conta.models import Producto
from apps.conta.models import TipoDocumento
from apps.conta.models import DetalleDocumento
from apps.conta.models import DocumentoVenta
from apps.conta.models import DocumentoProveedor


class DetalleDocumentoInlineAdmin(GenericTabularInline):
    model = DetalleDocumento
    extra = 1


class DocumentoAdmin(admin.ModelAdmin):
    inlines = [DetalleDocumentoInlineAdmin]


# Register your models here.
admin.site.register(PersonaJuridica)
admin.site.register(Proveedor)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(TipoDocumento)
admin.site.register(DocumentoVenta, DocumentoAdmin)
admin.site.register(DocumentoProveedor, DocumentoAdmin)
