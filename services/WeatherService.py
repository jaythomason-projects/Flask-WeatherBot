from peewee import DoesNotExist
from models import Forecast
import config
from utils import *

class WeatherService:
    OPENWEATHER_KEY = config.OPENWEATHER_API_KEY
    WEATHER_DATA_EXPIRATION_DAYS = config.WEATHER_DATA_EXPIRATION_DAYS
    WEATHER_DATA_EXPIRY = datetime.datetime.now() - datetime.timedelta(days=WEATHER_DATA_EXPIRATION_DAYS)
    OPEN_WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&units=metric&appid={}'

    @staticmethod
    def get_forecast_from_db(location, date):
        try:
            forecast = Forecast.get(Forecast.location_id == location, Forecast.date == date)
            return forecast
        except DoesNotExist:
            return None

    @staticmethod
    def check_if_forecast_is_stale(forecast):
        if forecast.created_at < WeatherService.WEATHER_DATA_EXPIRY:
            return True
        else:
            return False
        
    @staticmethod
    def delete_stale_forecast(location):
        Forecast.delete().where(Forecast.id == location.id).execute()

    @staticmethod
    def get_forecast_from_api(lat, lng):
        url = WeatherService.OPEN_WEATHER_API_URL.format(lat, lng, WeatherService.OPENWEATHER_KEY)
        response = make_request(url)

        if 'daily' in response:
            forecasts = []
            for day in response['daily']:
                forecasts.append({
                    'date': datetime.datetime.fromtimestamp(day['dt']).strftime('%d-%m-%Y'),
                    'icon': day['weather'][0]['icon'],
                    'description': day['weather'][0]['description'],
                    'temperature': day['temp']['day'],
                    'humidity': day['humidity'],
                    'wind_speed': day['wind_speed'],
                    'wind_direction': day['wind_deg']
                })
            return forecasts
        else:
            console_log(f"Error fetching forecast data for '{lat}, {lng}'. API response: {response['message']}", "ERROR")
            return None
    
    @staticmethod
    def add_forecast_to_db(location, weather_data):
        forecast = Forecast.create(
            location_id=location.id,
            date=weather_data['date'],
            icon=weather_data['icon'],
            description=weather_data['description'],
            temperature=weather_data['temperature'],
            humidity=weather_data['humidity'],
            wind_speed=weather_data['wind_speed'],
            wind_direction=weather_data['wind_direction']
        )
        return forecast

    @staticmethod
    def fetch_forecast_data(location, date):
        # Check if the forecast is already in the database
        forecast_from_db = WeatherService.get_forecast_from_db(location.id, date)
        if forecast_from_db:
            if WeatherService.check_if_forecast_is_stale(forecast_from_db):
                console_log(f"Stale forecast for '{location.name}' on '{date}' found in database. Deleting...", "INFO")
                WeatherService.delete_stale_forecast(location)
            else:
                console_log(f"Recent forecast for '{location.name}' on '{date}' found in database.", "INFO")
                return forecast_from_db

        # Fetch forecast from the API
        console_log(f"Recent forecast for '{location.name}' on '{date}' not found in database. Fetching from API...", "INFO")
        weather_data_from_api = WeatherService.get_forecast_from_api(location.latitude, location.longitude)

        # If API call is successful, add the location data to the database
        forecast_for_requested_date = None
        if weather_data_from_api:
            for daily_forecast in weather_data_from_api:
                console_log(f"Adding forecast for '{location.name}' on '{daily_forecast['date']}' to database...", "INFO")
                forecast = WeatherService.add_forecast_to_db(location, daily_forecast)
                # Check if the forecast is for the requested date. If yes, set it
                if forecast.date == date:
                    forecast_for_requested_date = forecast

        if forecast_for_requested_date:
            console_log(f"Successfully fetched forecast for '{location.name}' on '{date}' from API.", "INFO")
            return forecast_for_requested_date
        else:
            return None