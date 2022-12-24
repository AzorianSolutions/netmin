from django.db import models


class ServicePackage(models.Model):
    label = models.CharField(max_length=100)
    technologies = models.CharField(max_length=255)
    type = models.CharField(max_length=20)
    downstream = models.FloatField()
    upstream = models.FloatField()

    TECHNOLOGIES: dict = {
        'optical': 'Optical',
        'lfwll': 'Licensed FWLL',
        'ufwll': 'Unlicensed FWLL',
    }

    TYPES: dict = {
        'any': 'Any',
        'commercial': 'Commercial',
        'residential': 'Residential',
    }
