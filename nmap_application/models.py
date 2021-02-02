from django.db import models

# Source: Model field reference https://docs.djangoproject.com/en/3.1/ref/models/fields/#module-django.db.models.fields

class Host(models.Model):

    IP = models.GenericIPAddressField()

    mac_address = models.CharField(
        max_length=20,
        null=True
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
        max_length=255,
        null=True
    )

    product = models.CharField(
        max_length=255,
        null=True
    )

    extra_info = models.CharField(
        max_length=255,
        null=True
    )

    hostname = models.CharField(
        max_length=255,
        null=True
    )

    operative_system_type = models.CharField(
        max_length=255,
        null=True
    )

    method = models.CharField(
        max_length=255,
        null=True
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

    target = models.GenericIPAddressField()

    hosts = models.ManyToManyField(
        Host,
        related_name='host_history'
    )

    # Choices for field type
    QUICK = 'QS'
    FULL = 'FS'
    TYPE_CHOICES = [
        (QUICK, 'Quick scan'),
        (FULL, 'Full scan'),
    ]

    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=QUICK,
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the register was created"
    )

    updated_on = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the register was updated"
    )

    class Meta:
        ordering = ['-id']