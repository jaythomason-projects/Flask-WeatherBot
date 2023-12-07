from peewee import DoesNotExist
from fuzzywuzzy import process
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
    def get_best_location_match(location_name, response):
        if len(response['results']) == 1:
            return response['results'][0]
        else:
            response_names = [result['formatted_address'] for result in response['results']]
            best_match = process.extractOne(location_name, response_names)
            for result in response['results']: #? Is there a better way to do this?
                if result['formatted_address'] == best_match[0]:
                    return result

    @staticmethod
    def is_valid_location(response):
        address_components = response['address_components']

        # If there's less than two address components, it's likely a country.
        if len(address_components) < 2:
            return False
        
        # If the first address component is a country or province, it's likely the user asked about a country or state.
        elif 'country' in address_components[0]['types'] or 'administrative_area_level_1' in address_components[0]['types']:
            return False
        
        else:
            return True
        
    @staticmethod
    def extract_location_data(location_data):
        province = None
        country = None

        for component in location_data['address_components']:
            if 'administrative_area_level_1' in component['types']:
                province = component['long_name']
            elif 'country' in component['types']:
                country = component['long_name']

        return {
            'name': location_data['address_components'][0]['long_name'],
            'province': province,
            'country': country,
            'latitude': location_data['geometry']['location']['lat'],
            'longitude': location_data['geometry']['location']['lng']
        }

    @staticmethod
    def get_location_from_api(location_name):
        url = LocationService.GOOGLE_MAPS_API_URL.format(location_name, LocationService.GOOGLE_KEY)
        response = make_request(url)
        
        if response['status'] != 'OK':
            console_log(f"Error fetching location data for '{location_name}'. API response: {response['status']}", "ERROR")
            return None
        else:
            location = LocationService.get_best_location_match(location_name, response)

            if location and LocationService.is_valid_location(location):
                return LocationService.extract_location_data(location)
            else:
                console_log(f"'{location_name}' is not a valid location (eg. a country).", "ERROR")
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
        
    @staticmethod
    def ensure_default_locations_in_db():
        for location_name in config.DEFAULT_LOCATIONS:
            location = LocationService.get_location_from_db(location_name)
            if not location:
                location_data = LocationService.get_location_from_api(location_name)
                if not location_data:
                    console_log(f"Could not fetch location data for '{location_name}'. Skipping...", "WARNING")
                    continue
                else:
                    LocationService.add_location_to_db(location_data)
                    console_log(f"Added location '{location_name}' to database.", "INFO")
            else:
                console_log(f"Location '{location_name}' already in database. Skipping...", "INFO")