import requests
from flask import current_app


class GoogleMaps:

    @classmethod
    def get_latlong(cls, address):
        params = {
            'address': address,
            'key': current_app.config['GOOGLE']['maps_api_key'],
        }
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        info = requests.get(url, params=params).json()

        if info['results']:
            location = info['results'][0]['geometry']['location']
            info = {'lat': location['lat'], 'lng': location['lng']}
        else:
            info = {}
        return info
