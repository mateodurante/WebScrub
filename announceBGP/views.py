from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from netblock.models import Netblock
from django.conf import settings
from django.db import models
from django.contrib import messages
from .forms import AnnounceForm
from .models import AnnounceBGP
import ipaddress
import requests


def process_parameter(request, form):
    """
    Returns rendered page: Proceses the form parameters of a BGP announce.
    """

    net = form.cleaned_data['block']
    net_id = form.cleaned_data['netblock'].id
    asn = Netblock.objects.get(id=net_id).asn.asn

    command = AnnounceBGP.command(net, asn_list=[asn])

    try:
        req = requests.post(settings.HTTP_API_URL, data={'command': command})

        if req.status_code == 200:
            # Stores in the DB
            form.save()
            messages.success(request, "Bloque de red anunciado exitosamente.")
            return render(request, 'announceBGP.html', {'form': form})
        else:
            messages.success(request, f"El ScrubCentral respondio un mensaje inesperado. {req.text}")
            return render(request, 'announceBGP.html', {'form': form})
    except requests.exceptions.RequestException:
        messages.error(
            request, "Ha ocurrido un error en la comunicacion con la API del ScrubCentral.")

    return render(request, 'announceBGP.html', {'form': form})


def validate_announce(request, form):
    """
    Returns boolean: Checks if announced network is valid and belongs to the netblock
    """
    block = form.cleaned_data['block']

    try:
        address_a = ipaddress.ip_network(block)
    except ValueError:
        messages.error(
            request, "Ha ocurrido un error. El bloque no es valido.")
        return False

    address_b = ipaddress.ip_network(form.cleaned_data['netblock'])

    a_len = address_a.prefixlen
    b_len = address_b.prefixlen

    return a_len >= b_len and address_a.supernet(a_len - b_len) == address_b


@login_required
def index(request):
    """
    Shows index page
    """
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AnnounceForm(request.POST, user=request.user)
        # check whether it's valid:
        if form.is_valid():
            if validate_announce(request, form):
                return process_parameter(request, form)
            else:
                messages.error(request, "Bloque de red anunciado no pertenece \
                    al bloque de red seleccionado.")
                return render(request, 'announceBGP.html', {'form': form})

    else:
        form = AnnounceForm(user=request.user)

    return render(request, 'announceBGP.html', {'form': form})
