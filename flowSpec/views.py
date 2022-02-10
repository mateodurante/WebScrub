from django.shortcuts import render
from .forms import FlowSpecForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
import http.client
import json
import requests
import ipaddress
from django.conf import settings
from django.contrib import messages
from netblock.models import Netblock
from .models import FlowSpec

# Create your views here.


def process_form(request, form):
    """
    Returns a rendered page: Proceses the received form from the user.
    """

    src_net = form.cleaned_data['src_net']
    dst_net = form.cleaned_data['dst_net']
    src_port = form.cleaned_data['src_port']
    dst_port = form.cleaned_data['dst_port']
    t_proto = form.cleaned_data['t_proto']
    policy = form.cleaned_data['policy']
    rate_limit = form.cleaned_data['rate_limit']

    if not src_net:
        src_net = "0.0.0.0/0"

    command = FlowSpec.command(src_net, dst_net, src_port, dst_port, t_proto, policy, rate_limit)

    try:
        r = requests.post(settings.HTTP_API_URL, data={'command': command})
        if r.status_code == 200:
            sform = form.save()
            # To edit a field in a form
            if not form.cleaned_data['src_net']:
                sform.src_net = "0.0.0.0/0"
                sform.save()

            messages.success(request, "FlowSpec anunciado exitosamente.")
            return render(request, 'flow_result.html', {'command': command})
    except:
        messages.error(request, "Ha ocurrido un error. Vuelva a intentarlo.")

    return render(request, 'flowSpec.html', {'form': form})


def validate_announce(request, form):
    """
    Returns boolean: Checks if announced network is valid and belongs to the netblock
    """
    block = form.cleaned_data['dst_net']

    try:
        a = ipaddress.ip_network(block)
    except:
        messages.error(request, "Ha ocurrido un error. Vuelva a intentarlo.")
        return False

    b = ipaddress.ip_network(form.cleaned_data['announce'])

    a_len = a.prefixlen
    b_len = b.prefixlen

    return a_len >= b_len and a.supernet(a_len - b_len) == b


@login_required
def index(request):
    #asn_id = request.session['asn_id']
    #net_list = Netblock.objects.filter(asn_id=asn_id)
    asn_list = request.user.asn_set.all()
    asns = {}
    for asn in asn_list:
        asns[asn] = []
        for netblock in asn.netblock_set.all():
            asns[asn].append([netblock.id, netblock])
    return render(request, 'select_netblock.html', {'asns': asns})


def check_netblock(user, net_id):
    return net_id in [str(net.id) for asn in user.asn_set.all() for net in asn.netblock_set.all()]


@login_required
def create(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        net_id = request.session['net_id']
        form = FlowSpecForm(request.POST, net_id=net_id, request=request)

        # check whether it's valid:
        if form.is_valid():
            if validate_announce(request, form):
                return process_form(request, form)
            else:
                messages.error(
                    request, "Red de destino no pertenece al bloque del anuncio de red.")
                return render(request, 'flowSpec.html', {'form': form})

    else:
        net_id = request.GET['net_id']

        # Verificar que el asn sea parte de los asn que el usuario tiene (en POST tambien)
        if check_netblock(request.user, net_id):
            request.session['net_id'] = net_id
        else:
            return HttpResponse('El bloque de red no pertenece al usuario registrado')

        form = FlowSpecForm(net_id=net_id, request=request)

    return render(request, 'flowSpec.html', {'form': form})
