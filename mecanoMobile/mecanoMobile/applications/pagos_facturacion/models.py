from django.db import models

from applications.usuarios.models import Cliente


# Create your models here.
class PagosFacturacion(models.Model):
    METODOS_PAGO = (
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('transferencia', 'Transferencia Bancaria'),
        ('efectivo', 'Efectivo'),
        # ... añadir otros métodos según sea necesario
    )
    ESTADOS_PAGO = (
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
    )

    usuario = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pagos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=15, choices=ESTADOS_PAGO, default='pendiente')
    comision = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=15, choices=METODOS_PAGO, default='tarjeta')

    # ... otros campos que desees añadir

    def __str__(self):
        return f"Pago {self.id} por Usuario {self.usuario.user.username}"
