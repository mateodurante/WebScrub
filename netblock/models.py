from django.db import models
from django.contrib.auth.models import User
from asn.models import ASN


class Netblock(models.Model):
    network = models.CharField(max_length=15)
    mask = models.IntegerField()
    #owner = models.ManyToManyField(User)
    asn = models.ForeignKey(ASN, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}/{1}".format(self.network, self.mask)
