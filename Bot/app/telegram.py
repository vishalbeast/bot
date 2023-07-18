import requests
import json

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bots/api{self.token}/"

    def send_message(self, chat_id, text):
        url = self.api_url + "sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text
        }
        response = requests.post(url, json=data)
        return response.json()

    def send_keyboard(self, chat_id, text, buttons):
        url = self.api_url + "sendMessage"
        keyboard = {
            "keyboard": buttons,
            "one_time_keyboard": True
        }
        data = {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": json.dumps(keyboard)
        }
        response = requests.post(url, json=data)
        return response.json()

    @staticmethod
    def parse_webhook_data(request_body):
        update = json.loads(request_body)
        return update

    @staticmethod
    def parse_callback_query(request_body):
        callback_query = json.loads(request_body)
        return callback_query

