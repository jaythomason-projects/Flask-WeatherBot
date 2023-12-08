import requests
from datetime import datetime, timedelta
import dateparser

# Found that the dateparser library was not able to parse dates that contained certain words, so created this decorator to remove them
def remove_bad_words_from_date(func):
    def wrapper(date_string):
        words_to_remove = ['next', 'this']
        for word in words_to_remove:
            date_string = date_string.replace(word, '')
        return func(date_string)
    return wrapper

@remove_bad_words_from_date
def get_date_from_string(date_string):
    parsed_date = dateparser.parse(date_string, settings={'PREFER_DATES_FROM': 'future'})
    if parsed_date:
        parsed_date = parsed_date.strftime('%d-%m-%Y')
        return parsed_date
    else:
        return None
    
def make_request(url):
    response = requests.get(url).json()
    return response

def console_log(message, log_type):
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    log_types = {
        'INFO': f"[INFO][{current_time}]: {message}",
        'DEBUG': f"[DEBUG][{current_time}]: {message}",
        'WARNING': f"[WARNING][{current_time}]: {message}\n",
        'ERROR': f"[ERROR][{current_time}]: {message}\n",
        'SUCCESS': f"[SUCCESS][{current_time}]: {message}\n"
    }
    print(log_types.get(log_type, f"\n[INFO][{current_time}]: {message}"))