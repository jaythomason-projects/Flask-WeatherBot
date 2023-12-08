## Meet Flask-WeatherBot - A Fairly Useless And Very Specific Robotic-Sounding Weather Thing

This is WeatherBot. Ask it the weather, and it will tell you the weather. You can also ask it questions about travelling in the UK, if you’d like. Sometimes it will answer, other times, it will spout nonsense.

This app is built using Flask for the front-end and Python and Chatterbot for the back-end. It is capable of handling various location-based weather queries. Additionally, it uses a database to store weather and location data, reducing the need for excessive API calls.

## Instructions
### Installation
1. You'll need to install Python 3.7. You can download the different versions of Python [here](https://www.python.org/downloads/).
2. Navigate to the project's root directory.
3. Create a virtual environment by running `python3 -m venv venv`
3. Activate the virtual environment by running `source ./venv/bin/activate`
4. To install the prerequisites, run `pip install -r requirements.txt`
5. The app uses two APIs: [OpenWeather](https://openweathermap.org/api) and [Google Geocode](https://developers.google.com/maps/documentation/geocoding/overview). You'll need to sign up for both and get your own API keys. Then, create a `.env` file in the root directory and add your API keys like this:

```
OPENWEATHER_API_KEY=your_api_key
GOOGLE_API_KEY=your_api_key
```

6. To run the app, navigate to the folder and run `flask run` in your terminal.
7. Go to `http://localhost:5000` in your browser.

### Tips
- Weatherbot only reads your most recent statement 😢 You won't be able to ask follow-up questions about previous statements or make corrections. If your question was misinterpreted, try re-typing the full question.

## Credits
### UI:
- Primary chat interface (HTML and CSS) from [studygyann](https://github.com/studygyaan/tutorials/flask/flask-chatbot-chatterbot)

### Graphics:
- For icons: [iconmonstr](https://iconmonstr.com/loading-10-svg/)
- For animations: [Animate.css](https://animate.style/)
- For default styling: [water.css](https://watercss.kognise.dev/)
