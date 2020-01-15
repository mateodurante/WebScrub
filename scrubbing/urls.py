from django.conf.urls import url
from . import views

urlpatterns = [
            url(r'^$', views.index, name='scrubbing_index'),
            url(r'^store$', views.store, name='scrubbing_store'),
            url(r'^create$', views.create, name='scrubbing_create'),
            url(r'^([0-9]+)$', views.show, name='scrubbing_show'),
            url(r'^([0-9]+)/edit$', views.edit, name='scrubbing_edit'),
            url(r'^([0-9]+)/delete$', views.delete, name='scrubbing_delete'),
]
