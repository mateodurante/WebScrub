from django.shortcuts import render
from .forms import NetblockForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .forms import Netblock
from asn.models import ASN


def is_number(value):
    return value.isdigit()


@login_required
def index(request):
    """
            Si el usuario logueado es superusuario, tiene la capacidad de ver todos los bloques de red.
            Caso contrario, solo se listará sus bloques de red.
    """
    if request.user.is_superuser:
        netblock_list = Netblock.objects.all()
    else:
        asn_list = request.user.asn_set.all()
        netblock_list = []
        for asn in asn_list:
            for netblock in asn.netblock_set.all():
                netblock_list.append(netblock)
    return render(request, 'netblock_index.html', {'netblocks': netblock_list})


@login_required
def show(request, net_id):
    # TODO: Yo puedo consultar por datos de bloques no míos
    netblock = Netblock.objects.get(id=net_id)
    return render(request, 'netblock_show.html', {'netblock': netblock})


@login_required
@permission_required('netblock.add_netblock', raise_exception=True)
def create(request):
    form = NetblockForm()
    return render(request, 'netblock_create.html', {'form': form})


@login_required
@permission_required('netblock.add_netblock', raise_exception=True)
def store(request):
    if request.method == 'POST':
        form = NetblockForm(request.POST)
        if form.is_valid():
            netblock = form.save()
            if netblock:
                messages.success(
                    request, "Bloque de red guardado exitosamente.")
            else:
                messages.error(
                    request, "Ha ocurrido un error y no se ha podido guardar el bloque de red.")

        return render(request, 'netblock_create.html', {'form': form})


@login_required
@permission_required('netblock.delete_netblock', raise_exception=True)
def delete(request, net_id):
    netblock = Netblock.objects.get(id=net_id)
    if netblock.delete():
        messages.success(request, "Bloque de red borrado exitosamente.")
    else:
        messages.error(request, "Ha ocurrido un error. Vuelva a intentarlo.")

    return index(request)


@login_required
@permission_required('netblock.change_netblock', raise_exception=True)
def edit(request, net_id):
    netblock = Netblock.objects.get(id=net_id)
    if request.method == 'GET':
        form = NetblockForm(instance=netblock)
    elif request.method == 'POST':
        form = NetblockForm(request.POST, instance=netblock)
        if form.is_valid():
            if form.save():
                messages.success(
                    request, "Bloque de red actualizado exitosamente.")
            else:
                messages.error(
                    request, "Ha ocurrido un error. No se ha podido actualizar. Vuelva a intentarlo.")

    return render(request, 'netblock_edit.html', {'form': form, 'net_id': net_id})
