from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.apps, name='index '),
    re_path(r'^setasn$', views.set_asn, name='set_asn'),
]
