from django.conf.urls import url
from . import views

urlpatterns = [
            url(r'^run$', views.run, name='apicli_run'),
            url(r'^status$', views.status, name='apicli_status'),
]
