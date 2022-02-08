from django.db import models
from netblock.models import Netblock
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import ipaddress


class AnnounceBGP(models.Model):

    def validate_net(value):
        try:
            ip = ipaddress.ip_network(value)
            mask = int(value.split("/")[1])
        except:
            raise ValidationError(
                _('Bloque de red ingresado no es válido.'),
            )
        if ip.is_private:
            raise ValidationError(
                _('Bloque de red ingresado no pertenece a un bloque público.'),
                params={'value': value},
            )
        if mask < 16 or mask > 26:
            raise ValidationError(
                _('Mascara de red no válida (debe ser mayor que /15 y menor a /27)'),
            )

    # Fields
    id = models.AutoField(primary_key=True)
    netblock = models.ForeignKey(Netblock, on_delete=models.CASCADE)
    block = models.CharField(max_length=18, validators=[validate_net])

    def __str__(self):
        return self.block
