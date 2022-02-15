from django.contrib import admin
from announceBGP.models import AnnounceBGP

@admin.action(description='Eliminar objetos seleccionados')
def delete_model(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete_gracefull()

class AnnounceBGPAdmin(admin.ModelAdmin):
    actions = [delete_model]

admin.site.register(AnnounceBGP, AnnounceBGPAdmin)
