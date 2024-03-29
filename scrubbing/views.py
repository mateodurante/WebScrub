from django.shortcuts import render
from .forms import ScrubbingForm
from .models import Scrubbing
from peermessage.models import PeerMessage
from apicli.views import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required


# GET /scrubbing
@login_required
def index(request):
    scrubbing_list = Scrubbing.objects.all()
    # states = { s.address: PeerMessage.getLastState(s.address) for s in scrubbing_list }
    states = query_show_neighbor_summary()
    # print(scrubbing_list, states)
    return render(request, 'scrubbing_index.html', {'scrubbings': scrubbing_list, 'states': states})


# GET /scrubbing/{id}
@login_required
def show(request, id):
    scrubbing = Scrubbing.objects.get(id=id)
    neighbor_summary = raw_show_neighbor_summary_of_peer(scrubbing.address)
    neighbor_extensive = raw_show_neighbor_extensive_of_peer(scrubbing.address)
    neighbor_configuration = raw_show_neighbor_configuration_of_peer(scrubbing.address)
    return render(request, 'scrubbing_show.html', {'scrubbing': scrubbing, 'neighbor_summary': neighbor_summary, 'neighbor_extensive': neighbor_extensive, 'neighbor_configuration': neighbor_configuration})


# GET /scrubbing/create
@login_required
@permission_required('scrubbing.add_scrubbing', raise_exception=True)
def create(request):
    form = ScrubbingForm()
    return render(request, 'scrubbing_create.html', {'form': form})


# POST /scrubbing/store
@login_required
@permission_required('scrubbing.add_scrubbing', raise_exception=True)
def store(request):
    if request.method == 'POST':
        form = ScrubbingForm(request.POST)
        if form.is_valid():
            if form.save():
                messages.success(
                    request, "Scrubbing center guardado exitosamente.")
            else:
                messages.error(
                    request, "Ha ocurrido un error y no se ha podido guardar el scrubbing center.")

        return render(request, 'scrubbing_create.html', {'form': form})


# GET /request/{id}/delete
@permission_required('scrubbing.delete_scrubbing', raise_exception=True)
@login_required
def delete(request, id):
    scrubbing = Scrubbing.objects.get(id=id)
    if scrubbing.delete():
        messages.success(request, "Scrubbing center eliminado correctamente.")
    else:
        messages.error(request, "Ha ocurrido un error. Vuelva a intentarlo.")

    return index(request)


# GET /scrubbing/{id}/edit
# POST /scrubbing/{id}/edit
@login_required
@permission_required('scrubbing.change_scrubbing', raise_exception=True)
def edit(request, id):
    scrubbing = Scrubbing.objects.get(id=id)
    if request.method == 'GET':
        form = ScrubbingForm(instance=scrubbing)
    elif request.method == 'POST':
        form = ScrubbingForm(request.POST, instance=scrubbing)
        if form.is_valid():
            if form.save():
                messages.success(
                    request, "Scrubbing center se ha actualizado correctamente.")
            else:
                messages.error(
                    request, "Ha ocurrido un error. No se ha podido actualizar. Vuelva a intentarlo.")

    return render(request, 'scrubbing_edit.html', {'form': form, 'scrub_id': id})
