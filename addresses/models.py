from django.db import models


class Address(models.Model):
    address = models.CharField(
        'адрес',
        max_length=200,
        unique=True
    )
    lat = models.FloatField(
        'Широта',
        null=True,
        blank=True
    )
    lon = models.FloatField(
        'Долгота',
        null=True,
        blank=True
    )
    coordinates_update_date = models.DateField(
        'дата последнего обновления координат',
        auto_now=True
    )

    class Meta:
        verbose_name = 'локация'
        verbose_name_plural = 'локации'

    def __str__(self):
        return self.address
