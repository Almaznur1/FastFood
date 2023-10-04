from django.db import models
from .fetch_coordinates import fetch_coordinates


class MapPoint(models.Model):
    address = models.CharField(
        'адрес',
        max_length=200
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

    def save(self, *args, **kwargs):
        (lon, lat) = fetch_coordinates(self.address)
        self.lat = lat
        self.lon = lon
        super(MapPoint, self).save(*args, **kwargs)
