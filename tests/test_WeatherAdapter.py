import unittest
from chatbot import chatbot
from chatterbot.conversation import Statement
from logic_adapters.WeatherAdapter import WeatherAdapter

class TestWeatherAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = WeatherAdapter(chatbot)

    def test_can_process(self):
        # Test with weather keyword
        statement = Statement("What's the weather like today?")
        self.assertTrue(self.adapter.can_process(statement))

        # Test with non-weather keyword
        statement = Statement("What's your favorite color?")
        self.assertFalse(self.adapter.can_process(statement))

    def test_process_no_location(self):
        statement = Statement("What's the weather like today?")
        response = self.adapter.process(statement)
        self.assertEqual(response.text, "You didn't specify a location! Tell me where you want the weather for.")

    def test_process_multiple_locations(self):
        statement = Statement("What's the weather in London and Australia on Tuesday?")
        response = self.adapter.process(statement)
        self.assertEqual(response.text, "You specified more than one location! I can only give you the weather for one location at a time.")

    def test_process_multiple_dates(self):
        statement = Statement("What's the weather in London on Tuesday and Wednesday?")
        response = self.adapter.process(statement)
        self.assertEqual(response.text, "You specified more than one date! I can only give you the weather for one date at a time.")

    def test_process_country_as_location(self):
        statement = Statement("What's the weather in the UK on Tuesday?")
        response = self.adapter.process(statement)
        self.assertEqual(response.text, "I couldn't find the location 'UK' anywhere. Sorry!")

    def test_process_remove_bad_words_from_date(self):
        # Certain words were causing the dateparser to fail, eg. 'this'. Created a decorator to remove them
        statement = Statement("What is the weather going to be like in London this Friday?")
        response = self.adapter.process(statement)
        self.assertIn("Here's the weather for London on", response.text)

    def test_process_out_of_forecast_range(self):
        statement = Statement("What is the weather going to be like in London in three weeks?")
        response = self.adapter.process(statement)
        self.assertEqual("You specified a date that's more than 7 days from today! I can only get weather data for the next week.", response.text)

    def test_process_successful_response(self):
        statement = Statement("What's the weather in London on Tuesday?")
        response = self.adapter.process(statement)
        self.assertIn("Here's the weather for London on", response.text)

if __name__ == '__main__':
    unittest.main()