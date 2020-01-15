from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
import http.client
import json
import requests
from django.conf import settings
from bson.objectid import ObjectId
import time
from flowSpec.views import generate_command
from announceBGP.views import generate_announce
from announceBGP.models import AnnounceBGP
from flowSpec.models import FlowSpec
from django.contrib import messages


# Sends flow withdraw command
@login_required
def withdraw(request):

    if request.method == 'POST':
        array_flows = request.POST.getlist('flows_id')
        array_announces = request.POST.getlist('net_id')
    else:
        messages.error(
            request, "Ha ocurrido un error (COD 1). Vuelva a intentarlo.")

    try:
        for c_id in array_flows:
            flow = findFlows(c_id, request)
            r = requests.post(settings.HTTP_API_URL, data={
                              'command': str(flow).replace("announce", "withdraw")})
            if r.status_code == 200:
                deleteFlow(request, c_id)
            else:
                messages.error(
                    request, "Ha ocurrido un error (COD 2). Vuelva a intentarlo.")

        for n_id in array_announces:
            announce = findAnnounces(n_id, request)
            r = requests.post(settings.HTTP_API_URL, data={
                              'command': str(announce).replace("announce", "withdraw")})
            if r.status_code == 200:
                deleteAnnounce(request, n_id)
            else:
                messages.error(
                    request, "Ha ocurrido un error (COD 3). Vuelva a intentarlo.")

        return render(request, 'announceList.html', {'fdata': findFlows('all', request), 'adata': findAnnounces('all', request)})
    except:
        messages.error(
            request, "Ha ocurrido un error (COD 4). Vuelva a intentarlo.")

    return render(request, 'announceList.html')


def deleteFlow(request, f_id):
    fs = FlowSpec.objects.get(id=f_id)

    if fs.delete():
        messages.success(request, "FlowSpec borrado exitosamente.")
    else:
        messages.error(
            request, "Ha ocurrido un error (COD 5). Vuelva a intentarlo.")

    return


def deleteAnnounce(request, n_id):
    a = AnnounceBGP.objects.get(id=n_id)

    if a.delete():
        messages.success(request, "Anuncio de red borrado exitosamente.")
    else:
        messages.error(
            request, "Ha ocurrido un error (COD 6). Vuelva a intentarlo.")

    return


def findAnnounces(n_id, request):
    adata = {}
    user = request.user
    #asn_id = request.session['asn_id']
    #netblocks = user.asn_set.get(id=asn_id).netblock_set
    netblocks = [netblock for asn in user.asn_set.all()
                 for netblock in asn.netblock_set.all()]
    # Necesito los anuncios que me pertenecen solamente
    if n_id == 'all':
        for netblock in netblocks:
            announces = netblock.announcebgp_set.all()
            for a in announces:
                adata[a.id] = generate_announce(a.block)
    else:
        # No hay chequeo sobre si el anuncio es del usuario registrado
        net = AnnounceBGP.objects.get(id=n_id)
        return generate_announce(net)

    return adata


def findFlows(f_id, request):
    fdata = {}

    user = request.user
    #asn_id = request.session['asn_id']
    #netblocks = user.asn_set.get(id=asn_id).netblock_set
    netblocks = [netblock for asn in user.asn_set.all()
                 for netblock in asn.netblock_set.all()]

    if f_id == 'all':
        for netblock in netblocks:
            announces = netblock.announcebgp_set.all()
            for announce in announces:
                #fs = FlowSpec.objects.all()
                fs = announce.flowspec_set.all()
                for f in fs:
                    command = generate_command(
                        f.src_net, f.dst_net, f.src_port, f.dst_port, f.t_proto, f.policy, f.rate_limit)
                    fdata[f.id] = command
    else:
        # No hay chequeo sobre si el flowspec es del usuario registrado
        fs = FlowSpec.objects.get(id=f_id)
        command = generate_command(
            fs.src_net, fs.dst_net, fs.src_port, fs.dst_port, fs.t_proto, fs.policy, fs.rate_limit)
        return command

    return fdata


@login_required
def index(request):
    return render(request, 'announceList.html', {'fdata': findFlows('all', request), 'adata': findAnnounces('all', request)})
