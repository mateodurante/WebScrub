from django.shortcuts import render
# from .forms import ScrubbingForm
from .models import PeerMessage
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
        PeerMessage(**flatten_dict(data)).save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

