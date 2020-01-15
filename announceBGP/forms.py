from django.forms import ModelForm
from .models import AnnounceBGP

"""
class AnnounceForm(forms.Form):
    ip = forms.CharField(label='Bloque IP', widget=forms.TextInput(attrs={'placeholder': 'Ingrese un bloque IP'}))

    def clean(self):
        cleaned_data = super(AnnounceForm, self).clean()
        data = cleaned_data.get('ip')
        try:
            #ip = ipaddress.ip_address(data)
            net = ipaddress.ip_network(data)

            #TODO: Faltaria verificar si el bloque que publica le pertenece efectivamente a dicho AS.
            if net.is_private :
                self.add_error('ip', 'Es un bloque de red privado')
        except ValueError:
            self.add_error('ip', 'No es un bloque valido')
        return data

    def is_global(self, ip):
        return not (ip.is_link_local or ip.is_loopback or ip.is_multicast or ip.is_private or ip.is_reserved or ip.is_unspecified)
"""


class AnnounceForm(ModelForm):
    class Meta:
        model = AnnounceBGP
        fields = ['netblock', 'block']
        labels = {
            "netblock": "Dirección de de red",
            "block": "Bloque de red a anunciar",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        asn_list = user.asn_set.all()
        asns = {}
        for asn in asn_list:
            asns[asn] = []
            for netblock in asn.netblock_set.all():
                asns[asn].append([netblock.id, netblock])
        super(AnnounceForm, self).__init__(*args, **kwargs)
        self.fields['netblock'].widget.choices = asns.items()
