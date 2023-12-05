from peewee import DoesNotExist
from models import Location
import config
from utils import *

class LocationService:
    GOOGLE_KEY = config.GOOGLE_API_KEY
    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'

    @staticmethod
    def get_location_from_db(location_name):
        try:
            location = Location.get(Location.name == location_name)
            return location
        except DoesNotExist:
            return None

    @staticmethod
    def get_location_from_api(location_name):
        url = LocationService.GOOGLE_MAPS_API_URL.format(location_name, LocationService.GOOGLE_KEY)
        response = make_request(url)
        
        if response['status'] == 'OK':
            # Check address_components for locality, which indicates a city or suburb
            for component in response['results'][0]['address_components']:
                if 'locality' in component['types']:
                    return {
                        'name': component['long_name'],
                        'province': response['results'][0]['address_components'][1]['long_name'],
                        'country': response['results'][0]['address_components'][2]['long_name'],
                        'latitude': response['results'][0]['geometry']['location']['lat'],
                        'longitude': response['results'][0]['geometry']['location']['lng']
                    }
        else:
            console_log(f"Error fetching location data for '{location_name}'. API response: {response['status']}", "ERROR")
            return None

    @staticmethod
    def add_location_to_db(location_data):
        location = Location.create(
            name=location_data['name'],
            province=location_data['province'],
            country=location_data['country'],
            latitude=location_data['latitude'],
            longitude=location_data['longitude']
        )
        return location

    @staticmethod
    def fetch_location_data(location_name):
        # First, check if the location is already in the database
        location_from_db = LocationService.get_location_from_db(location_name)
        if location_from_db:
            console_log(f"Location '{location_name}' found in database.", "INFO")
            return location_from_db

        # Second, if the location is not in the database, fetch it from the API
        console_log(f"Location '{location_name}' not found in database. Fetching from API...", "INFO")
        location_from_api = LocationService.get_location_from_api(location_name)

        # If API call is successful, add the location data to the database and return it
        if location_from_api:
            console_log(f"Location '{location_name}' found in API. Adding to database and returning...", "INFO")
            return LocationService.add_location_to_db(location_from_api)
        else:
            return None