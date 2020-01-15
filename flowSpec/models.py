from django.db import models
from django import forms
import ipaddress
from announceBGP.models import AnnounceBGP
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


DISPLAY_CHOICES = (
    ("UDP", "UDP"),
    ("TCP", "TCP"),
    ("ICMP", "ICMP")
)


POLICY_CHOICES = (
    ("accept", "Accept"),
    ("discard", "Discard"),
    ("rate-limit", "Rate limit")
)


class FlowSpec(models.Model):

    def validate_port(value):
        valids = ['=', '>']
        min_port = max_port = ''
        if value[0] in valids:
            for i in range(1, len(value)-1):
                if value[i] == "&" and value[i+1] == "<":
                    max_port = value[i+2:len(value)]
                    break
                else:
                    min_port += value[i]
            try:
                valid_int = int(min_port)
            except ValueError:
                raise ValidationError(
                    _('Formato de puerto no válido.'),
                )
            if max_port:
                try:
                    valid_int = int(max_port)
                except ValueError:
                    raise ValidationError(
                        _('Formato de puerto no válido.'),
                    )
        else:
            raise ValidationError(
                _('Formato de puerto no válido.'),
            )

    def validate_srcnet(value):
        # Si esta vacio
        if not value:
            return
        elif value == '0.0.0.0/0':
            return
        try:
            ip = ipaddress.ip_network(value)
        except:
            raise ValidationError(
                _('Bloque de red ingresado no es válido.'),
            )
        if ip.is_private:
            raise ValidationError(
                _('Bloque de red ingresado no pertenece a un bloque público.'),
                params={'value': value},
            )

    def validate_dstnet(value):
        try:
            ip = ipaddress.ip_network(value)
            mask = int(value.split("/")[1])
        except:
            raise ValidationError(
                _('Bloque de red ingresado no es válido.'),
                params={'value': value},
            )
        if ip.is_private:
            raise ValidationError(
                _('Bloque de red ingresado no pertenece a un bloque público.'),
                params={'value': value},
            )
        if mask < 16:
            raise ValidationError(
                _('Máscara para red destino no es válida.'),
                params={'value': value},
            )

    src_net = models.CharField(max_length=18, validators=[
                               validate_srcnet], blank=True, null=True)
    dst_net = models.CharField(max_length=18, validators=[validate_dstnet])
    src_port = models.CharField(
        max_length=13, blank=True, null=True, validators=[validate_port])
    dst_port = models.CharField(
        max_length=13, blank=True, null=True, validators=[validate_port])
    t_proto = MultiSelectField(choices=DISPLAY_CHOICES)
    policy = models.CharField(max_length=15, choices=POLICY_CHOICES)
    rate_limit = models.IntegerField('', blank=True, null=True)
    announce = models.ForeignKey(AnnounceBGP, on_delete=models.CASCADE)
