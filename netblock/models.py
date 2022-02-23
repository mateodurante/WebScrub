from django.db import models
from django.contrib.auth.models import User
from asn.models import ASN
import ipaddress


class Netblock(models.Model):
    id = models.AutoField(primary_key=True)
    network = models.CharField(max_length=15)
    mask = models.IntegerField()
    #owner = models.ManyToManyField(User)
    asn = models.ForeignKey(ASN, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}/{1}".format(self.network, self.mask)

    def findByIP(ip):
        ip = ip.split('/')[0]
        for netblock in Netblock.objects.all():
            if ipaddress.ip_address(ip) in ipaddress.ip_network(f'{netblock.network}/{netblock.mask}'):
                return netblock
