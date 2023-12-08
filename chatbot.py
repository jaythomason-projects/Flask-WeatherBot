from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import spacy
from utils import *

BEST_MATCH = 'chatterbot.logic.BestMatch'
WEATHER_LOGIC = 'logic_adapters.WeatherAdapter.WeatherAdapter'
TRAINING_FILES = [
    'training_data/weather_questions.txt', 
    'training_data/personal_questions.txt'
    ]  # Additional training files can be added here

def download_model(model_name):
    try:
        spacy.load(model_name)
        console_log(f"{model_name} is already downloaded.", "INFO")
    except OSError:
        console_log(f"{model_name} is not downloaded. Downloading now...", "INFO")
        spacy.cli.download(model_name)
        console_log(f"{model_name} downloaded successfully.", "INFO")

# Download language models
download_model("en_core_web_sm")
download_model("en")

# Initialise chatbot
chatbot = ChatBot(
    'WeatherBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': WEATHER_LOGIC
        },
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': "I am sorry, I don't understand. I am still learning.",
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database.sqlite3'
)

# Train chatbot with the training files
trainer_list = ListTrainer(chatbot)

for file in TRAINING_FILES:
    with open(file, 'r') as f:
        console_log(f"Training with {file}...", "INFO")
        training_data = f.read().splitlines()
        trainer_list.train(training_data)

# Training with corpus
# https://chatterbot.readthedocs.io/en/stable/training.html
trainer_corpus = ChatterBotCorpusTrainer(chatbot)

# Just the most basic training corpus - faster for testing
trainer_corpus.train(
    'chatterbot.corpus.english.greetings',
    'chatterbot.corpus.english.conversations',
    'chatterbot.corpus.english.botprofile'
)

# For the full training corpus, uncomment the line below
# trainer_corpus.train('chatterbot.corpus.english')