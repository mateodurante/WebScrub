from django.conf.urls import url
from . import views

urlpatterns = [
            url(r'^$', views.index, name='asn_index'),
            url(r'^store$', views.store, name='asn_store'),
            url(r'^create$', views.create, name='asn_create'),
            url(r'^([0-9]+)$', views.show, name='asn_show'),
            url(r'^([0-9]+)/edit$', views.edit, name='asn_edit'),
            url(r'^([0-9]+)/delete$', views.delete, name='asn_delete'),
]
