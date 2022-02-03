from django.forms import ModelForm
from .models import AnnounceBGP
import ipaddress

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

    def clean_netblock(self):
        cleaned_data = self.clean()
        bnetblock = cleaned_data.get('netblock')
        try:
            netblock = ipaddress.ip_network(bnetblock)
        except ValueError:
            self.add_error('netblock', "Netblock no es válido")
            # return False

        return bnetblock
    
    def clean_block(self):
        cleaned_data = self.clean()
        netblock = ipaddress.ip_network(cleaned_data.get('netblock'))
        bblock = cleaned_data.get('block')
        gre_ip = ipaddress.ip_address(cleaned_data.get('netblock').asn.gre_ip)
        try:
            block = ipaddress.ip_network(bblock)
            # con python3.7 esta la funcion subnet_of()
            if not block in netblock.subnets(new_prefix=block.prefixlen): # if is subnet_of
                self.add_error('block', "El bloque de red no se encuentra dentro del bloque seleccionado")

            # verificar que la IP del terminador GRE del usuario no este dentro del bloque publicado
            # TODO agregar estas validaciones al modelo
            if gre_ip in block:
                self.add_error('block', f"La IP del terminador GRE del AS ({gre_ip}) esta dentro del bloque de red a anunciar")
        except ValueError:
            self.add_error('block', "El bloque de red no es válido")
            # return False


        return bblock