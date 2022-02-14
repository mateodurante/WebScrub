from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import json

# Create your views here.

def query(cmd):
    try:
        req = requests.post(f'{settings.HTTP_API_URL}/exabgpcli', data={'command': cmd})
        j = json.loads(req.text)
        j.update({'status_code': req.status_code, 'ok': j['stderr'] == ''})
        return j
    except requests.exceptions.RequestException:
        return {'error': 'Error connecting to ExaBGP'}

def query_show_neighbor_summary():
    peers = {}
    try:
        res = query('show neighbor summary')['stdout']
        lines = res.split('\n')
        for l in lines[1:]:
            if l:
                sl = l.split()
                peers[sl[0]] = {'peer': sl[0], 'as': sl[1], 'uptime': sl[2], 'state': sl[3], 'sent': sl[4], 'received': sl[5]}
    except Exception as e:
        # raise e
        print('Error:', e)
    return peers

def query_clear_adj_rib():
    ok = False
    try:
        ok = not query('clear adj-rib')['error']
    except Exception as e:
        # raise e
        print('Error:', e)
    return ok

def query_show_neighbor_extensive():
    peers = {}
    try:
        res = query('show neighbor extensive')['stdout']
        lines = res.split('\n')
        peer = None
        peer_lines = []
        for l in lines:
            if l.startswith('Neighbor'):
                if peer:
                    peers[peer] = '\n'.join(peer_lines)
                peer = l.split()[1]
                peer_lines = [l]
            else:
                # agregamos datos al peer
                peer_lines.append(l)
        if peer:
            peers[peer] = '\n'.join(peer_lines)
                
    except Exception as e:
        # raise e
        print('Error:', e)
    return peers

def query_show_neighbor_configuration():
    peers = {}
    try:
        res = query('show neighbor configuration')['stdout']
        lines = res.split('\n')
        peer = None
        peer_lines = []
        for l in lines:
            if l.startswith('neighbor'):
                if peer:
                    peers[peer] = '\n'.join(peer_lines)
                peer = l.split()[1]
                peer_lines = [l]
            else:
                # agregamos datos al peer
                peer_lines.append(l)
        if peer:
            peers[peer] = '\n'.join(peer_lines)
                
    except Exception as e:
        # raise e
        print('Error:', e)
    return peers

def query_show_neighbor_summary():
    peers = {}
    try:
        res = query('show neighbor summary')['stdout']
        lines = res.split('\n')
        for l in lines[1:]:
            if l:
                sl = l.split()
                peers[sl[0]] = {'peer': sl[0], 'as': sl[1], 'uptime': sl[2], 'state': sl[3], 'sent': sl[4], 'received': sl[5]}
    except Exception as e:
        # raise e
        print('Error:', e)
    return peers

def raw_show_neighbor_summary_of_peer(peer):
    try:
        res = query_show_neighbor_summary()[peer]
        data = ""
        for k, v in res.items():
            data += f"{k}: {v}\n"
        return data
    except Exception as e:
        raise e

def raw_show_neighbor_configuration_of_peer(peer):
    try:
        res = query_show_neighbor_configuration()
        return res[peer]
    except Exception as e:
        raise e

def raw_show_neighbor_extensive_of_peer(peer):
    try:
        res = query_show_neighbor_extensive()
        return res[peer]
    except Exception as e:
        raise e

# POST /apicli/run
@login_required
@permission_required('apicli.run', raise_exception=True)
@csrf_exempt
def run(request):
    if request.method == 'POST':
        cmd = request.POST['cmd']
        result = query(cmd)
        return JsonResponse({'result': result, 'cmd': cmd})
    elif request.method == 'GET':
        return render(request, 'apicli.html')


# POST /apicli/status
@login_required
@csrf_exempt
def status(request):
    if request.method == 'POST':
        qn = request.POST['qn']
        querys = {
            'Summary':'show neighbor summary', 
            'Configuration':'show neighbor configuration', 
            'Extensive':'show neighbor extensive',
            'Adj-RIB out':'show adj-rib out',
            'Adj-RIB in':'show adj-rib in',
            }
        if qn in querys.keys():
            result = query(querys[qn])
            return JsonResponse({'result': result, 'cmd': qn})
        else:
            return JsonResponse({'error': 'Unknown query'})
    elif request.method == 'GET':
        return render(request, 'apicli_status.html')

