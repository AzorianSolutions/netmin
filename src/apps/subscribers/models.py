from django.db import models
from apps.settings.models import ServicePackage


class Subscriber(models.Model):
    org_name = models.CharField(max_length=50, null=True)
    primary_contact_name = models.CharField(max_length=50)
    primary_contact_phone1 = models.CharField(max_length=20)
    primary_contact_phone2 = models.CharField(max_length=20, null=True)
    secondary_contact_name = models.CharField(max_length=50, null=True)
    secondary_contact_phone1 = models.CharField(max_length=20, null=True)
    secondary_contact_phone2 = models.CharField(max_length=20, null=True)
    notes = models.TextField(null=True)

    @property
    def label(self):
        return self.org_name if self.org_name is not None and len(str(self.org_name)) else self.primary_contact_name


class SubscriberLocation(models.Model):
    label = models.CharField(max_length=100)
    type = models.CharField(max_length=30)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, null=True)
    address_city = models.CharField(max_length=50)
    address_state = models.CharField(max_length=2)
    address_postal_code = models.CharField(max_length=50)
    address_country = models.CharField(max_length=2)

    # Relationships
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)

    TYPES: dict = {
        'commercial': 'Commercial',
        'residential': 'Residential',
    }


class SubscriberEquipment(models.Model):
    label = models.CharField(max_length=100)
    type = models.CharField(max_length=30)
    mac_address = models.CharField(max_length=12)
    serial_number = models.CharField(max_length=30, null=True)

    # Relationships
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    location = models.ForeignKey(SubscriberLocation, on_delete=models.CASCADE)

    TYPES: dict = {
        'bridge': 'Bridge',
        'router': 'Router',
        'switch': 'Switch',
    }


class SubscriberSubscription(models.Model):
    status = models.CharField(max_length=30)
    lease_time = models.BigIntegerField(null=True)
    ipv4_address = models.GenericIPAddressField(null=True)
    ipv4_netmask = models.SmallIntegerField(null=True, default=24)
    ipv4_pool = models.CharField(max_length=50, null=True, default='pppoe')
    ipv6_prefix = models.GenericIPAddressField(null=True)
    ipv6_pool = models.CharField(max_length=50, null=True)
    routes = models.TextField(null=True)
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)

    # Relationships
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    equipment = models.ForeignKey(SubscriberEquipment, on_delete=models.CASCADE)
    package = models.ForeignKey(ServicePackage, on_delete=models.CASCADE)

    STATUSES: dict = {
        'active': 'Active',
        'canceled': 'Canceled',
        'paused': 'Paused',
        'pending': 'Pending',
        'delinquent': 'Delinquent',
    }

    @property
    def ipv4_static(self):
        if self.ipv4_address is not None and len(str(self.ipv4_address)):
            return self.ipv4_address

        if self.ipv4_pool is not None and len(str(self.ipv4_pool)):
            return self.ipv4_pool

        return 'None'

    @property
    def ipv6_static(self):
        if self.ipv6_prefix is not None and len(str(self.ipv6_prefix)):
            return self.ipv6_prefix

        if self.ipv6_pool is not None and len(str(self.ipv6_pool)):
            return self.ipv6_pool

        return 'None'
