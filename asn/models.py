from django.db import models
from scrubbing.models import Scrubbing
from django.contrib.auth.models import User


class ASN(models.Model):
    id = models.AutoField(primary_key=True)
    asn = models.CharField(max_length=10)
    gre_ip = models.CharField(max_length=15)
    scrubbing = models.ManyToManyField(Scrubbing)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.asn
