from django.db import models
from django import forms
import ipaddress
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete 
from django.dispatch import receiver
from apicli.views import query


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

    def validate_port(ranges):
        # =1024  >1024  >1024&<3500
        valids = ['=', '>']
        min_port = max_port = ''
        values = ranges.split()
        for value in values:
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

    id = models.AutoField(primary_key=True)
    src_net = models.CharField(max_length=18, validators=[
                               validate_srcnet], blank=True, null=True)
    dst_net = models.CharField(max_length=18, validators=[validate_dstnet])
    src_port = models.CharField(
        max_length=255, blank=True, null=True, validators=[validate_port])
    dst_port = models.CharField(
        max_length=255, blank=True, null=True, validators=[validate_port])
    t_proto = MultiSelectField(choices=DISPLAY_CHOICES)
    policy = models.CharField(max_length=15, choices=POLICY_CHOICES)
    rate_limit = models.IntegerField('', blank=True, null=True)
    announce = models.ForeignKey('announceBGP.AnnounceBGP', on_delete=models.CASCADE)

    @staticmethod
    def command(src_net, dst_net, src_port, dst_port, t_proto, policy, rate_limit, withdraw=False):
        """
        Returns the flowspec command: Proceses the received parameters to generate a valid FlowSpec command.
        """
        action = 'withdraw' if withdraw else 'announce'

        t_protocol = f"[{' '.join(t_proto)}]"

        if policy == 'rate-limit':
            if not rate_limit:
                rate_limit = '9600'
            policy += f" {rate_limit}"

        sp = dp = ''
        if src_port:
            sp = f"source-port [{src_port}]; "
        if dst_port:
            dp = f"destination-port [{dst_port}]; "

        command = f"{action} flow route {{ match {{ source {src_net}; destination {dst_net}; {dp} {sp} protocol {t_protocol}; }} then {{ {policy}; }} }}"

        return command

    def as_command(self, withdraw=False):
        """
        Returns the flowspec command: Proceses the received parameters to generate a valid FlowSpec command.
        """

        return self.command(self.src_net, self.dst_net, self.src_port, self.dst_port, self.t_proto, self.policy, self.rate_limit, withdraw=withdraw)

# @receiver(pre_delete, sender=FlowSpec)
# def delete_repo(sender, instance, **kwargs):
#     query(instance.as_command(withdraw=True))

    def delete_gracefull(self):
        query(self.as_command(withdraw=True))
        return self.delete()
