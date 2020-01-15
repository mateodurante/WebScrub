from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='announce_index'),
    #url(r'^create$',views.create, name='create'),
]
