"""WebScrub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path

# admin.autodiscover()
# admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    re_path(r'^', include('home.urls')),
    re_path(r'^announceBGP/', include('announceBGP.urls')),
    re_path(r'^flowSpec/', include('flowSpec.urls')),
    re_path(r'^announceList/', include('flist.urls')),
    re_path(r'^netblock/', include('netblock.urls')),
    re_path(r'^scrubbing/', include('scrubbing.urls')),
    re_path(r'^asn/', include('asn.urls')),
    re_path(r'^peermessage/', include('peermessage.urls')),
    re_path(r'^apicli/', include('apicli.urls')),
    # re_path(r'^auth/', include('django.contrib.auth.urls')),
    # re_path(r'^accounts/', include('allauth.urls')),
]
