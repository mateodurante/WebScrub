from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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
            f = FlowSpec.objects.get(id=c_id)
            f.delete_gracefull()
        

        for n_id in array_announces:
            a = AnnounceBGP.objects.get(id=n_id)
            a.delete_gracefull()

        return render(request, 'announceList.html', {'fdata': findFlows('all', request), 'adata': findAnnounces('all', request)})
    except Exception as e:
        messages.error(
            request, f"Ha ocurrido un error (COD 4). Vuelva a intentarlo. {e}")
        raise e

    return render(request, 'announceList.html')


def deleteFlow(request, f_id):
    fs = FlowSpec.objects.get(id=f_id)

    if fs.delete_gracefull():
        messages.success(request, "FlowSpec borrado exitosamente.")
    else:
        messages.error(
            request, "Ha ocurrido un error (COD 5). Vuelva a intentarlo.")

    return


def deleteAnnounce(request, n_id):
    a = AnnounceBGP.objects.get(id=n_id)

    if a.delete_gracefull():
        messages.success(request, "Anuncio de red borrado exitosamente.")
    else:
        messages.error(
            request, "Ha ocurrido un error (COD 6). Vuelva a intentarlo.")

    return


def findAnnounces(n_id, request):
    adata = {}
    user = request.user
    netblocks = [netblock for asn in user.asn_set.all()
                 for netblock in asn.netblock_set.all()]
    # Necesito los anuncios que me pertenecen solamente
    if n_id == 'all':
        for netblock in netblocks:
            announces = netblock.announcebgp_set.all()
            for a in announces:
                adata[a.id] = a.as_command()
    else:
        # No hay chequeo sobre si el anuncio es del usuario registrado
        a = AnnounceBGP.objects.get(id=n_id)
        return a.as_command()

    return adata


def findFlows(f_id, request):
    fdata = {}

    user = request.user
    netblocks = [netblock for asn in user.asn_set.all()
                 for netblock in asn.netblock_set.all()]

    if f_id == 'all':
        for netblock in netblocks:
            announces = netblock.announcebgp_set.all()
            for announce in announces:
                fs = announce.flowspec_set.all()
                for f in fs:
                    fdata[f.id] = f.as_command()
    else:
        # No hay chequeo sobre si el flowspec es del usuario registrado
        fs = FlowSpec.objects.get(id=f_id)
        command = fs.as_command()
        return command

    return fdata


@login_required
def index(request):
    return render(request, 'announceList.html', {'fdata': findFlows('all', request), 'adata': findAnnounces('all', request)})
