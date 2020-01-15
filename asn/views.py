from django.shortcuts import render
from .forms import ASNForm
from .models import ASN
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def index(request):
    if request.user.is_superuser:
        asn_list = ASN.objects.all()
    else:
        asn_list = request.user.asn_set.all()
    return render(request, 'asn_index.html', {'asn': asn_list})


@login_required
def show(request, id):
    asn = ASN.objects.get(id=id)
    netblocks = asn.netblock_set.all
    return render(request, 'asn_show.html', {'asn': asn, 'netblocks': netblocks})


@login_required
@permission_required('asn.add_asn', raise_exception=True)
def create(request):
    form = ASNForm()
    return render(request, 'asn_create.html', {'form': form})


@login_required
@permission_required('asn.add_asn', raise_exception=True)
def store(request):
    if request.method == 'POST':
        form = ASNForm(request.POST)
        if form.is_valid():
            asn = form.save()
            if asn:
                messages.success(request, "ASN guardado exitosamente.")
            else:
                messages.error(
                    request, "Ha ocurrido un error y no se ha podido guardar el ASN.")

        return render(request, 'asn_create.html', {'form': form})


@login_required
@permission_required('asn.delete_asn', raise_exception=True)
def delete(request, id):
    asn = ASN.objects.get(id=id)
    if asn.delete():
        messages.success(request, "ASN borrado exitosamente.")
    else:
        messages.error(request, "Ha ocurrido un error. Vuelva a intentarlo.")

    return index(request)


@login_required
@permission_required('asn.change_asn', raise_exception=True)
def edit(request, id):
    asn = ASN.objects.get(id=id)
    if request.method == 'GET':
        form = ASNForm(instance=asn)
    elif request.method == 'POST':
        form = ASNForm(request.POST, instance=asn)
        if form.is_valid():
            if form.save():
                messages.success(request, "ASN actualizado exitosamente.")
            else:
                messages.error(
                    request, "Ha ocurrido un error. No se ha podido actualizar. Vuelva a intentarlo.")

    return render(request, 'asn_edit.html', {'form': form, 'asn_id': id})
