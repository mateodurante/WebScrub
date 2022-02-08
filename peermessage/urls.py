from django.conf.urls import url
from . import views


urlpatterns = [
            url(r'^$', views.index, name='peermessage_index'),
            url(r'^add$', views.add, name='peermessage_add'),
]
