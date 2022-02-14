from django.contrib import admin
from .models import PeerMessage, PeerStatus, PeerIfaceStatus

admin.site.register(PeerMessage)
admin.site.register(PeerStatus)
admin.site.register(PeerIfaceStatus)
