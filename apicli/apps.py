from django.apps import AppConfig


class ApicliConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apicli'
    verbose_name = "Clear BGP and FlowSpec and apply saved announces in DB"

    def ready(self):
        from .views import query_clear_adj_rib, query
        from announceBGP.models import AnnounceBGP
        from flowSpec.models import FlowSpec

        print('Ready:', self.name)
        print('Iniciando proceso de limpieza de BGP y FlowSpec...')
        
        # ok = False
        # while not ok:
        #     try:
        #         # Clear BGP
        #         print('Intentando conectar con API para limpiar BGP...')
        #         ok = query_clear_adj_rib()
        #     except Exception as e:
        #         # raise e
        #         print('Error:', e)
        #     time.sleep(1)
        query_clear_adj_rib()

        print('Limpieza de BGP completada. Enviando announces de DB...')
        announces = AnnounceBGP.objects.all()
        for announce in announces:
            query(announce.as_command())
        flows = FlowSpec.objects.all()
        for flow in flows:
            query(flow.as_command())
        print('Envio de announces completado.')
            