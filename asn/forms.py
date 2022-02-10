from django.forms import ModelForm
from .models import ASN


class ASNForm(ModelForm):
    class Meta:
        model = ASN
        fields = ['asn', 'scrubbing', 'owner']
        labels = {
            "asn": "Número de sistema autónomo",
            "scrubbing": "Scrubbings centers asociados",
            "owner": "Administrador de sistema autónomo",
        }
