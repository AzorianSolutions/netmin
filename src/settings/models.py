from django.db import models


class ServicePackage(models.Model):
    label = models.CharField(max_length=50)
    technologies = models.CharField(max_length=255)
    type = models.CharField(max_length=20)
    downstream = models.FloatField()
    upstream = models.FloatField()


class EquipmentConfiguration(models.Model):
    label = models.CharField(max_length=100)
    frequency_band = models.CharField(max_length=20)
    internal_gain = models.SmallIntegerField()
    external_gain = models.SmallIntegerField()
    beamwidth = models.SmallIntegerField()
    downtilt = models.SmallIntegerField()

    FREQUENCY_BANDS: list = ['900 MHz', '2 GHz', '3 GHz', '5 GHz', '6 GHz', '11 GHz', '18 GHz', '24 GHz', '60 GHz',
                             '80 GHz']
