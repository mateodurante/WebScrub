from django.db import models
from netblock.models import Netblock
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import ipaddress
from django.db.models.signals import pre_delete 
from django.dispatch import receiver
from apicli.views import query
from flowSpec.models import FlowSpec


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

    @staticmethod
    def check_asn(user, asn_id):
        """
        Returns boolean: checks if user has a specific asn by asn_id
        """
        return user.asn_set.filter(id=asn_id).exists()

    @staticmethod
    def command(net, asn_list=[], withdraw=False):
        """
        Returns announce command: Builds a string with the correct announce sintax.
        This method is externally used.
        """
        action = 'withdraw' if withdraw else 'announce'
        path = f"as-path [{' '.join(asn_list)}]" if asn_list else ""
        return f"{action} route {net} {path} next-hop self"

    def as_command(self, withdraw=False):
        """
        Returns announce command: Builds a string with the correct announce sintax.
        """
        return self.command(self.block, asn_list=[self.netblock.asn.asn], withdraw=withdraw)

@receiver(pre_delete, sender=AnnounceBGP)
def delete_repo(sender, instance, **kwargs):
    for flow in instance.flowspec_set.all():
        flow.delete()
    query(instance.as_command(withdraw=True))
