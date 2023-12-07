from chatbot import chatbot
from flask import Flask, render_template, request
from services.LocationService import LocationService

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))

# Ensure default locations are in the database
LocationService.ensure_default_locations_in_db()

if __name__ == "__main__":
    app.run()