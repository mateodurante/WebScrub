from django.forms import ModelForm
from .models import ASN


class ASNForm(ModelForm):
    class Meta:
        model = ASN
        fields = ['asn', 'gre_ip', 'scrubbing', 'owner']
        labels = {
            "asn": "Número de sistema autónomo",
            "gre_ip": "Dirección IP de terminador GRE",
            "scrubbing": "Scrubbings centers asociados",
            "owner": "Administrador de sistema autónomo",
        }
