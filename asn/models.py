from django.db import models
from scrubbing.models import Scrubbing
from django.contrib.auth.models import User


class ASN(models.Model):
    id = models.AutoField(primary_key=True)
    asn = models.CharField(max_length=10)
    scrubbing = models.ManyToManyField(Scrubbing, related_name="asns")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.asn
