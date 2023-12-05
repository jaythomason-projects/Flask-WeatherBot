import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set keys, ready to be imported as local variables
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

# Variable that controls how many days to keep weather data in the database
WEATHER_DATA_EXPIRATION_DAYS = 1