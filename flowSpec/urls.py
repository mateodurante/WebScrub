from django.conf.urls import url
from . import views

urlpatterns = [
            url(r'^$',views.index, name='flowspec_index'),
            url(r'^create$',views.create, name='flowspec_create'),

]
