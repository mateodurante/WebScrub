from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.


def check_asn(request, asn_id):
    return request.user.asn_set.filter(id=asn_id).exists()


@login_required
def index(request):
    return render(request, 'home/index.html')


@login_required
def apps(request):
    # return HttpResponse(status=201)
    return render(request, 'home/apps_home.html')


def set_asn(request):
    print(request)
    print(dir(request))
    if request.method == 'POST':
        asn_id = request.POST['asn_id']
        if check_asn(request, asn_id):
            request.session['asn_id'] = asn_id
            return apps(request)
        else:
            return HttpResponse('El asn no pertenece al usuario registrado')
    else:
        # Si el usuario no tiene asn, entonces lo redirigo al inicio (no podrá anunciar ni nada relacionado con manejo de redes)
        username = 'sarasa'
        asn_query = request.user.asn_set
        if asn_query.count() > 0:
            asn_list = request.user.asn_set.all
            return render(request, 'home/select_asn.html', {'asn_list': asn_list})
        else:
            return redirect("/")
