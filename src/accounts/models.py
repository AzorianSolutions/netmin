from django.db import models


class Account(models.Model):
    org_name = models.CharField(max_length=30, null=True)
    primary_contact_name = models.CharField(max_length=50)
    primary_contact_phone1 = models.IntegerField()
    primary_contact_phone2 = models.IntegerField(null=True)
    secondary_contact_name = models.CharField(max_length=50, null=True)
    secondary_contact_phone1 = models.IntegerField(null=True)
    secondary_contact_phone2 = models.IntegerField(null=True)
    notes = models.TextField()


class AccountLocation(models.Model):
    account_id = models.IntegerField()
    label = models.CharField(max_length=100)
    type = models.CharField(max_length=30)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, null=True)
    address_city = models.CharField(max_length=50)
    address_state = models.CharField(max_length=2)
    address_postal_code = models.CharField(max_length=50)
    address_country = models.CharField(max_length=2)

    TYPES: dict = {
        'commercial': 'Commercial',
        'residential': 'Residential',
    }


class AccountEquipment(models.Model):
    account_id = models.IntegerField()
    location_id = models.IntegerField()
    label = models.CharField(max_length=100)
    type = models.CharField(max_length=30)
    mac_address = models.CharField(max_length=12)
    serial_number = models.CharField(max_length=30, null=True)

    TYPES: dict = {
        'bridge': 'Bridge',
        'router': 'Router',
        'switch': 'Switch',
    }


class AccountEquipmentPackage(models.Model):
    account_id = models.IntegerField()
    equipment_id = models.IntegerField()
    package_id = models.IntegerField()
    status = models.CharField(max_length=30)
    lease_time = models.BigIntegerField(null=True)
    ipv4_address = models.GenericIPAddressField(null=True)
    ipv4_pool = models.CharField(max_length=50, null=True)
    ipv6_prefix = models.GenericIPAddressField(null=True)
    ipv6_pool = models.CharField(max_length=50, null=True)
    routes = models.TextField(null=True)
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)

    STATUSES: dict = {
        'active': 'Active',
        'canceled': 'Canceled',
        'paused': 'Paused',
        'pending': 'Pending',
        'delinquent': 'Delinquent',
    }
