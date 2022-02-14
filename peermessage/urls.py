from django.conf.urls import url
from . import views


urlpatterns = [
            url(r'^$', views.index, name='peermessage_index'),
            url(r'^add$', views.add, name='peermessage_add'),
            url(r'^nodestatus$', views.nodestatus, name='peermessage_nodestatus'),
            url(r'^shownodestatus$', views.shownodestatus, name='peermessage_shownodestatus'),
            url(r'^shownodeifacestatus$', views.shownodeifacestatus, name='peermessage_shownodeifacestatus'),
            url(r'^shownodeifacestatusdata$', views.shownodeifacestatusdata, name='peermessage_shownodeifacestatusdata'),
]
