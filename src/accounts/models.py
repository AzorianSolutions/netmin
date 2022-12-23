from django.db import models


class Account(models.Model):
    org_name = models.CharField(max_length=30)
    primary_contact_name = models.CharField(max_length=50)
    primary_contact_phone1 = models.IntegerField()
    primary_contact_phone2 = models.IntegerField()
    secondary_contact_name = models.CharField(max_length=50)
    secondary_contact_phone1 = models.IntegerField()
    secondary_contact_phone2 = models.IntegerField()
    notes = models.TextField()


class AccountLocation(models.Model):
    account_id = models.IntegerField()
    label = models.CharField(max_length=50)
    type = models.CharField(max_length=30)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100)
    address_city = models.CharField(max_length=50)
    address_state = models.CharField(max_length=2)
    address_postal_code = models.CharField(max_length=50)
    address_country = models.CharField(max_length=2)


class AccountEquipment(models.Model):
    account_id = models.IntegerField()
    location_id = models.IntegerField()
    configuration_id = models.IntegerField()
    type = models.CharField(max_length=30)
    mac_address = models.CharField(max_length=12)
    serial_number = models.CharField(max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.SmallIntegerField()
    azimuth = models.SmallIntegerField()
    downtilt = models.SmallIntegerField()


class AccountEquipmentPackage(models.Model):
    account_id = models.IntegerField()
    equipment_id = models.IntegerField()
    package_id = models.IntegerField()
    status = models.CharField(max_length=30)
    lease_time = models.BigIntegerField()
    ipv4_address = models.GenericIPAddressField()
    ipv4_pool = models.CharField(max_length=50)
    ipv6_prefix = models.GenericIPAddressField()
    ipv6_pool = models.CharField(max_length=50)
    routes = models.TextField()
    ppp_username = models.CharField(max_length=50)
    ppp_password = models.CharField(max_length=50)