from django.conf.urls import url
from . import views

urlpatterns = [
            url(r'^$', views.index, name='netblock_index'),
            url(r'^store$', views.store, name='netblock_store'),
            url(r'^create$', views.create, name='netblock_create'),
            url(r'^([0-9]+)$', views.show, name='netblock_show'),
            url(r'^([0-9]+)/edit$', views.edit, name='netblock_edit'),
            url(r'^([0-9]+)/delete$', views.delete, name='netblock_delete'),
]
