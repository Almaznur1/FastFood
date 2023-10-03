from django import template
from geopy import distance

register = template.Library()


@register.filter
def get_object_by_id(queryset, id):
    try:
        return queryset.get(id=id)
    except queryset.model.DoesNotExist:
        return None


@register.simple_tag
def fetch_distance(order, restaurant):
    return distance.distance(
        (order.lat, order.lon),
        (restaurant.lat, restaurant.lon)
    ).km
