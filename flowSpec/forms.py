from django.forms import ModelForm, TextInput
from .models import FlowSpec
from netblock.models import Netblock

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

"""
Campos adicionales de FlowSpec:
#proto_number = forms.CharField(label='Número de protocolo', widget=forms.TextInput(attrs={'placeholder': 'Ingrese datos'}))
#icmp_type= forms.CharField(label='Tipo ICMP', widget=forms.TextInput(attrs={'placeholder': 'Ingrese datos'}))
#icmp_code= forms.CharField(label='Código ICMP', widget=forms.TextInput(attrs={'placeholder': 'Ingrese datos'}))
#tcp_flags= forms.CharField(label='Flags TCP', widget=forms.TextInput(attrs={'placeholder': 'Ingrese datos'}))
#packet_lenght= forms.CharField(label='Long. de paquete', widget=forms.TextInput(attrs={'placeholder': 'Ingrese datos'}))
#dscp= forms.CharField(label='DSCP', widget=forms.TextInput(attrs={'placeholder': 'Ingrese datos'}))
#fragment= forms.CharField(label='Fragmento', widget=forms.TextInput(attrs={'placeholder': 'Ingrese datos'}))
"""

from django.utils.translation import ugettext_lazy as _
from announceBGP.models import AnnounceBGP


class FlowSpecForm(ModelForm):
    class Meta:
        model = FlowSpec
        fields = ['announce', 'src_net', 'dst_net', 'src_port',
                  'dst_port', 't_proto', 'policy', 'rate_limit']
        labels = {
            "announce": "Bloques de redes anunciados",
            "src_net": "Dirección de red de origen",
            "dst_net": "Dirección de red de destino",
            "src_port": "Puerto de origen",
            "dst_port": "Puerto de destino",
            "t_proto": "Protocolo",
            "policy": "Política de filtro",
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        net_id = kwargs.pop('net_id')
        super(FlowSpecForm, self).__init__(*args, **kwargs)
        asn = Netblock.objects.get(id=net_id).asn
        self.fields['announce'].queryset = asn.netblock_set.get(
            id=net_id).announcebgp_set

        """
        #Para aplicar CSS a los campos
        widgets = {
            'announce': namedWidget('PSPID'),
            # No encuentro como modificar el nombre html del campo anounce
        }
        """
