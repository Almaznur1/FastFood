from django import template
from geopy import distance
from datetime import date, timedelta
from addresses.models import MapPoint
from addresses.fetch_coordinates import fetch_coordinates

register = template.Library()


def update_coordinates(point):
    (lon, lat) = fetch_coordinates(point.address)
    point.lat = lat
    point.lon = lon
    point.save()


@register.filter
def get_object_by_id(queryset, id):
    try:
        return queryset.get(id=id)
    except queryset.model.DoesNotExist:
        return None


@register.simple_tag
def fetch_distance(*points):
    coordinates = []
    for point in points:
        point, created = MapPoint.objects.get_or_create(address=point.address)
        if (point.coordinates_update_date + timedelta(days=1)) < date.today():
            update_coordinates(point)
        coordinates.append((point.lat, point.lon))

        if None in (point.lat, point.lon):
            return 'N/a'

    return round(distance.distance(*coordinates).km, 3)
