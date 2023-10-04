import requests
from django.conf import settings

apikey = settings.GEOCODER_API_KEY


def fetch_coordinates(address):
    lon = None
    lat = None
    base_url = "https://geocode-maps.yandex.ru/1.x"
    try:
        response = requests.get(base_url, params={
            "geocode": address,
            "apikey": apikey,
            "format": "json",
        })
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return lon, lat

    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if found_places:
        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")

    return lon, lat
