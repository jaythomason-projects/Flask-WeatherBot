# Meet Flask-WeatherBot
WeatherBot. You were born to do one thing, and one thing only. Tell people the weather. And you'll do it well. You're a simple bot, but you're a good bot. You're WeatherBot.

[Click here to see a live demo of Flask-WeatherBot](https://weatherbot.jaythomasonprojects.com/)

## Why Do I Exist?
This project was created for the final assessment of my graduate certificate in Programming & Development. Here is the scenario:

> A travel blogger has been commissioned by the (fictional) travel website Go Travel! to explore England and to post regular updates on their trip. In preparation for this blog series, the owners of the website have worked with a developer to create a Flask API framework prototype. This will integrate with their site and return weather data for each specific location on the blogger’s itinerary. They are in the process of testing the prototype, which uses an API to connect to OpenWeatherLinks to an external site. and then returns weather data based on the location entered into a user form. 

This app is built using Flask for the front-end and Python and Chatterbot for the back-end. It is capable of handling various location-based weather queries. Additionally, it uses a database to store weather and location data, reducing the need for excessive API calls.

## Quick Start
If you want to run your own Flask-WeatherBot in Docker, follow these steps:

1. Make sure you have Docker installed on your machine.
2. Create an .env file with the necessary API keys and configuration. Here is an example of what your .env file should look like:
    
    ```yaml
    GOOGLE_API_KEY=<your_google_api_key>
    OPENWEATHER_API_KEY=<your_openweather_api_key>
    WEATHER_DATA_EXPIRATION_DAYS=1
    ```
    
3. Run the following command, replacing `<path/to/file>` with the path to your .env file:
    
    ```bash
    docker run -d -p 5000:5000 jaythomasonprojects/flask-weatherbot:latest —env-file <path/to/file>
    ```
    
4. That's it! The app will be exposed on port 5000. You can access it by navigating to port 5000 on the IP machine where the Docker container is running. (eg. `http://localhost:5000`)

## Usage
- ChatterBot is a rule-based chatbot, which means that messages sent to the chatbot are processed in a very systematic way. The more direct your question, the more likely you are to receive an appropriate response. Eg. ‘What is the weather like in Melbourne this Sunday?’ or ‘What is the weather like in New York in 2 days?’
- Weatherbot only understands your most recent mssage 😢 You won't be able to ask follow-up questions about previous statements or make corrections. If your question was misinterpreted, try re-typing the full question.

## Credits
### UI:
- Primary chat interface (HTML and CSS) from [studygyann](https://github.com/studygyaan/tutorials/flask/flask-chatbot-chatterbot)

### Graphics:
- For icons: [iconmonstr](https://iconmonstr.com/loading-10-svg/)
- For animations: [Animate.css](https://animate.style/)
- For default styling: [water.css](https://watercss.kognise.dev/)
