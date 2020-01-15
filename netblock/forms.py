from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Netblock


class NetblockForm(ModelForm):
    class Meta:
        model = Netblock
        fields = ['network', 'mask', 'asn']
        labels = {
            "network": "Dirección de red",
            "mask": "Máscara",
            "asn": "Número de sistema autónomo",
        }
