from peewee import *
import datetime

db = SqliteDatabase('weather.db')

class Location(Model):
    id = PrimaryKeyField()
    name = CharField(max_length=50)
    province = CharField(max_length=50)
    country = CharField(max_length=50)
    latitude = FloatField()
    longitude = FloatField()

    class Meta:
        database = db

class Forecast(Model):
    location_id = ForeignKeyField(Location, backref='weather')
    created_at = DateTimeField(default=datetime.datetime.now)
    date = DateTimeField() #? Will DateField work here?
    icon = CharField(max_length=10)
    description = CharField(max_length=100)
    temperature = FloatField()
    humidity = IntegerField()
    wind_speed = FloatField()
    wind_direction = IntegerField()

    class Meta:
        database = db

    def get_readable_weather_data(self):
        readable_weather_data = {
            'icon': self.icon,
            #'description': self.get_proper_case_description(),
            'description': self.description,
            'temperature': f"{round(self.temperature)}°C",
            'humidity': f"{self.humidity}%",
            'wind_speed': f"{self.wind_speed}km/s",
            'wind_direction': self.get_readable_wind_direction()
        }
        return readable_weather_data
    
    # def get_proper_case_description(self):
    #     return self.description.title()

    def get_readable_wind_direction(self):
        # I'm not smart enough to make this, someone else did it in Javascript:
        # https://stackoverflow.com/questions/48750528/get-direction-from-degrees
        
        # Define the direction names
        directions = ['north', 'north-east', 'east', 'south-east', 'south', 'south-west', 'west', 'north-west']

        # Convert degrees to an index
        index = round(self.wind_direction / 45) % 8
        
        # Return the direction name
        return directions[index]

db.connect()
db.create_tables([Location, Forecast])