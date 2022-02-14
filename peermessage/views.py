from django.shortcuts import render
# from .forms import ScrubbingForm
from .models import PeerMessage, PeerStatus, PeerIfaceStatus
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json 


# GET /peermessage
@login_required
def index(request):
    peermessage_list = PeerMessage.objects.all()
    return render(request, 'peermessage_index.html', {'peermessages': peermessage_list})


# GET /peermessage/{id}
@login_required
def show(request, id):
    peermessage = PeerMessage.objects.get(id=id)
    return render(request, 'peermessage_show.html', {'peermessage': peermessage})

def flatten_dict(dd, separator='_', prefix=''):
    return { prefix + separator + k if prefix else k : v
             for kk, vv in dd.items()
             for k, v in flatten_dict(vv, separator, kk).items()
             } if isinstance(dd, dict) else { prefix : dd }

# POST /peermessage/add
# @login_required
# TODO: agregar permisos con api_key
# @permission_required('peermessage.add_peermessage', raise_exception=True)
@csrf_exempt
def add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # PeerMessage(**flatten_dict(data)).save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# POST /peermessage/nodestatus
@csrf_exempt
def nodestatus(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        address = get_client_ip(request)
        for d in data['cmds']:
            try:
                to_save = flatten_dict(d)
                to_save.update({'address': address})
                PeerStatus.objects.update_or_create(
                    address=to_save['address'], cmd=to_save['cmd'],
                    defaults=to_save,
                )
            except Exception as e:
                print(f'Error al guardar PeerStatus {to_save}')
                raise e

        for d in data['ifaces']:
            try:
                d.update({'address': address})
                d['data'] = json.dumps(d['data'])
                to_save = flatten_dict(d)
                PeerIfaceStatus.objects.update_or_create(
                    address=to_save['address'], name=to_save['name'],
                    defaults=to_save,
                )
            except Exception as e:
                print(f'Error al guardar PeerIfaceStatus {to_save}')
                raise e
                
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


# GET /peermessage/shownodestatus
@login_required
def shownodestatus(request):
    if request.method == 'GET':
        status = PeerStatus.getAllStatus()
        return render(request, 'nodestatus_index.html', {'nodes': status})
    # return html error


# GET /peermessage/shownodeifacestatus
@login_required
def shownodeifacestatus(request):
    if request.method == 'GET':
        status = PeerIfaceStatus.getAllStatus()
        return render(request, 'nodeifacestatus_index2.html', {'nodes': status})
    # return html error

# GET /peermessage/shownodeifacestatusdata
@login_required
def shownodeifacestatusdata(request):
    if request.method == 'GET':
        status = PeerIfaceStatus.getAllStatusValues()
        return JsonResponse({'nodes': status})
    # return html error

    

