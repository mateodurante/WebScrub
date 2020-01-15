from django.forms import ModelForm
from .models import Scrubbing


class ScrubbingForm(ModelForm):
    class Meta:
        model = Scrubbing
        fields = ['name', 'address', 'gre_ip']
        labels = {
            "name": "Nombre",
            "address": "Dirección IP",
            "gre_ip": "Dirección de terminador GRE",
        }
