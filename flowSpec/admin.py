from django.contrib import admin
from flowSpec.models import FlowSpec

@admin.action(description='Eliminar objetos seleccionados')
def delete_model(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete_gracefull()

class FlowSpecAdmin(admin.ModelAdmin):
    actions = [delete_model]

admin.site.register(FlowSpec, FlowSpecAdmin)
