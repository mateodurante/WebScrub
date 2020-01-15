from django.conf.urls import url
from . import views

urlpatterns = [
            url(r'^$',views.index, name='flis_index'),
            url(r'^Withdraw/$',views.withdraw, name='Withdraw'),

]
