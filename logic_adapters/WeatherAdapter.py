from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from spacy import load
from services.LocationService import LocationService
from services.WeatherService import WeatherService
from utils import *
import config

# Logic adapter for processing weather-related queries
class WeatherAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.nlp = load('en_core_web_sm')

    def can_process(self, statement, additional_response_selection_parameters=None): # additional_response_selection_parameters is a required parameter
        console_log(f"Checking if WeatherAdapter can process statement: '{statement.text}'", "INFO")

        # Check if the statement contains any tokens that are in the weather_keywords list
        weather_keywords = ['weather', 'temperature', 'forecast', 'rain', 'sun', 'cloud', 'wind', 'humidity']
        tokenised_statement = self.nlp(statement.text)
        matching_tokens = [token.text for token in tokenised_statement if token.text in weather_keywords]

        # If there are any weather_keywords in the statement, process with the WeatherAdapter
        if matching_tokens:
            for token in matching_tokens:
                console_log(f"Token matching WeatherAdapter keywords: '{token}'", "DEBUG")
            return True
        else:
            return False
            
    def process(self, statement, additional_response_selection_parameters=None): # additional_response_selection_parameters is a required parameter
        console_log(f"Processing statement with WeatherAdapter: '{statement.text}'", "INFO")

        # Extract locations and dates from the statement
        tokenised_statement = self.nlp(statement.text)
        locations = [ent.text for ent in tokenised_statement.ents if ent.label_ == 'GPE' or ent.text in config.DEFAULT_LOCATIONS]
        dates = [ent.text for ent in tokenised_statement.ents if ent.label_ == 'DATE']
        console_log(f"Found locations and dates: {locations}, {dates}", "DEBUG")

        # Convert dates to standard format
        converted_dates = [get_date_from_string(date) for date in dates]
        console_log(f"Converted dates: {converted_dates}", "DEBUG")

        # Use location, date and weather data to create a response
        response = self.create_response(locations, converted_dates)
        console_log(f"Response from WeatherAdapter: '{response['message']}'", response['status'])
        
        # Return the response as a Statement object
        response_statement = Statement(response['message'])
        response_statement.confidence = response['confidence']
        return response_statement
            
    def get_temperature_tips(self, temperature):
        if temperature < 0:
            return "Brace yourself, it's going to be freezing!. Don't forget your warm woolies."
        elif temperature < 10:
            return "Looks rather chilly! A snug jacket would be a good idea."
        elif temperature > 30:
            return "Phew, it's a scorcher! Be sure to wear plenty of sunscreen and stay hydrated."
        else:
            return ""

    def get_weather_description_tips(self, description):
        weather_descriptions = {
            "rain": "Don't forget your brolly, it's going to be a drizzly day!",
            "thunderstorm": "Storms will be on the horizon. Stay indoors if you can.",
            "snow": "Better pack your snow boots, you're going to need them.",
            "light rain": "Expect a sprinkle of rain, maybe pack a lightweight waterproof layer.",
            "mist": "There's a bit of mist around! Remember to drive carefully if you're on the road.",
            "smoke": "Smoky conditions predicted. Motorists, please exercise caution.",
            "haze": "Weather's looking hazy. Drive safely, folks!",
            "dust": "Expect some dust clouds today. Consider wearing face protection if you're going out.",
            "fog": "Foggy day ahead! Take extra caution, particularly if you're driving.",
            "sand": "Sandy conditions are expected. Safe travels if you're on the road.",
            "ash": "Ashfall expected. Be careful, especially while driving.",
            "squall": "Get your windbreakers out, squalls are anticipated!",
            "tornado": "Potential extreme weather alert! Always heed the advice of local authorities."
        }
        # Check if the description contains any of the weather_descriptions keys - for example, 'light rain' contains 'rain'
        for key in weather_descriptions:
            if key in description:
                return weather_descriptions[key]
        return ""

    def get_wind_tips(self, wind_speed):
        if wind_speed < 10:
            return ""
        elif wind_speed < 20:
            return "Expect to feel the wind in your hair. It's going to be a bit breezy!"
        elif wind_speed < 30:
            return "It's going to be quite breezy out there. Secure your hat!"
        else:
            return "Hold onto your hats, extreme winds expected! Please follow local advisories."
    
    def validate_message(func):
        def wrapper(self, locations, dates):
            if not locations:
                return {
                    'status': "WARNING",
                    'message': "You didn't specify a location! Tell me where you want the weather for.",
                    'confidence': 0.30
                }
            elif not dates or dates[0] is None:
                return {
                    'status': "WARNING",
                    'message': "You didn't specify a date! Tell me when you want the weather for.",
                    'confidence': 0.30
                }            
            elif len(locations) > 1:
                return {
                    'status': "WARNING",
                    'message': "You specified more than one location! I can only give you the weather for one location at a time.",
                    'confidence': 0.70
                }
            elif len(dates) > 1:
                return {
                    'status': "WARNING",
                    'message': "You specified more than one date! I can only give you the weather for one date at a time.",
                    'confidence': 0.70
                }
            # If the date is greater than 7 days from today, return a warning
            elif dates[0] > get_date_from_string('7 days'):
                return {
                    'status': "WARNING",
                    'message': "You specified a date that's more than 7 days from today! I can only get weather data for the next week.",
                    'confidence': 0.70
                }
            else:
                return func(self, locations, dates)
        return wrapper
    
    def fetch_data_for_processing(func):
        def wrapper(self, locations, dates):
            # Fetch location data from database or APIs
            location_data = LocationService.fetch_location_data(locations[0])
            
            if location_data is None:
                return {
                    'status': 'WARNING',
                    'message': f"I couldn't find the location '{locations[0]}' anywhere. Sorry!",
                    'confidence': 0.25
                }
            
            # Get the forecast data for the location and date from database or APIs
            forecast_data = WeatherService.fetch_forecast_data(location_data, dates[0])

            if forecast_data is None:
                return {
                    'status': 'WARNING',
                    'message': f"I couldn't find the weather for '{locations[0]}' on '{dates[0]}'. I can only retrieve weather data for the next 7 days.",
                    'confidence': 0.40
                }
            
            return func(self, location_data, forecast_data)
        return wrapper
    
    @validate_message
    @fetch_data_for_processing
    def create_response(self, location_data, forecast_data):
        location = location_data.name
        date = forecast_data.date

        # Make readable copies of the forecast data
        readable_forecast_data = forecast_data.get_readable_weather_data()
        description = readable_forecast_data['description']
        temperature = readable_forecast_data['temperature']
        humidity = readable_forecast_data['humidity']
        wind_speed = readable_forecast_data['wind_speed']
        wind_direction = readable_forecast_data['wind_direction']

        # Craft the chatbot response
        greeting = f"Here's the weather for {location} on {date}:"
        forecast_details = f"It'll be {description} with a temperature of {temperature}. Be ready for humidity of {humidity}, and {wind_speed} winds from the {wind_direction}."
        weather_tips = [
            self.get_temperature_tips(forecast_data.temperature),
            self.get_weather_description_tips(description),
            self.get_wind_tips(forecast_data.wind_speed)
        ]

        # Combine the weather tips
        weather_tips = ' '.join(weather_tips)

        # Combine the response message
        response_message = ' '.join([greeting, forecast_details, weather_tips])
        return {
            'status': 'SUCCESS',
            'message': response_message,
            'confidence': 1.1
        }