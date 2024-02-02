import os

# Set keys, ready to be imported as local variables
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
WEATHER_DATA_EXPIRATION_DAYS = os.environ.get('WEATHER_DATA_EXPIRATION_DAYS')

#!TODO: Add validation for the environment variables

# Convert WEATHER_DATA_EXPIRATION_DAYS to an int
WEATHER_DATA_EXPIRATION_DAYS = int(WEATHER_DATA_EXPIRATION_DAYS) if WEATHER_DATA_EXPIRATION_DAYS else None

# Locations required for the assignment. Location data will be loaded into the database when app is first run
DEFAULT_LOCATIONS = [
    "Lake District National Park",
    "Corfe Castle",
    "The Cotswolds",
    "Cambridge",
    "Bristol",
    "Oxford",
    "Norwich",
    "Stonehenge",
    "Watergate Bay",
    "Birmingham"
]