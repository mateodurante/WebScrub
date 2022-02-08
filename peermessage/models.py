from django.db import models
import datetime

class ConvertingDateTimeField(models.DateTimeField):

    def get_prep_value(self, value):
        if type(value) == float:
            return datetime.datetime.utcfromtimestamp(value)
        return value

class PeerMessage(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    time = ConvertingDateTimeField()
    counter = models.IntegerField()
    type = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    neighbor_address_local = models.CharField(max_length=255)
    neighbor_address_peer = models.CharField(max_length=255)
    neighbor_asn_local = models.CharField(max_length=255)
    neighbor_asn_peer = models.CharField(max_length=255)
    neighbor_direction = models.CharField(max_length=255)
    neighbor_state = models.CharField(max_length=255)
    raw = models.TextField()

    def __str__(self):
        return self.name


    def getLastState(address_peer):
        return PeerMessage.objects.filter(neighbor_address_peer=address_peer, type='state').order_by('-time')[0]

