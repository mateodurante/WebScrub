from django.forms import ModelForm
from .models import Scrubbing


class ScrubbingForm(ModelForm):
    class Meta:
        model = Scrubbing
        fields = ['name', 'address']
        labels = {
            "name": "Nombre",
            "address": "Dirección IP"
        }
