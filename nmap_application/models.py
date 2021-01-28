from django.db import models

# Source: Model field reference https://docs.djangoproject.com/en/3.1/ref/models/fields/#module-django.db.models.fields

class Host(models.Model):

    IP = models.CharField(
        max_length=20
    )

    mac_address = models.CharField(
        max_length=20
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the register was created"
    )

    updated_on = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the register was updated"
    )

class OperativeSystemMatch(models.Model):

    name = models.CharField(
        max_length=255
    )

    accuracy = models.PositiveSmallIntegerField()

    line = models.PositiveSmallIntegerField()

    host = models.ForeignKey(
        Host,
        on_delete=models.CASCADE,
        related_name='host_os_match'
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the register was created"
    )

    updated_on = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the register was updated"
    )

class OperativeSystemClass(models.Model):

    operative_system_match = models.OneToOneField(
        OperativeSystemMatch,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    type = models.CharField(
        max_length=255
    )

    vendor = models.CharField(
        max_length=255
    )

    operative_system_family = models.CharField(
        max_length=255
    )

    operative_system_generation = models.CharField(
        max_length=255
    )

    accuracy = models.PositiveSmallIntegerField()

    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the register was created"
    )

    updated_on = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the register was updated"
    )

class Port(models.Model):

    protocol = models.CharField(
        max_length=255
    )

    portid = models.PositiveSmallIntegerField()

    state = models.CharField(
        max_length=255
    )

    reason = models.CharField(
        max_length=255
    )

    reason_ttl = models.PositiveSmallIntegerField()

    host = models.ForeignKey(
        Host,
        on_delete=models.CASCADE,
        related_name='host_port'
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the register was created"
    )

    updated_on = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the register was updated"
    )

class PortService(models.Model):

    port = models.OneToOneField(
        Port,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    name = models.CharField(
        max_length=255
    )

    product = models.CharField(
        max_length=255
    )

    operative_system_type = models.CharField(
        max_length=255
    )

    method = models.CharField(
        max_length=255
    )

    conf = models.PositiveSmallIntegerField()

    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the register was created"
    )

    updated_on = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the register was updated"
    )

class ScannerHistory(models.Model):

    target = models.CharField(
        max_length=30,
        help_text="This field saves the IP, range of IPs or subnet mask that is scanned"
    )

    host = models.ManyToManyField(
        Host,
        related_name='host_history'
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the register was created"
    )

    updated_on = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the register was updated"
    )