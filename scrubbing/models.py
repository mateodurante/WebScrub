from django.db import models


class Scrubbing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=15)
    gre_ip = models.CharField(max_length=15)

    def __str__(self):
        return self.name
