import os, requests
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def send_telegram_message(message):
    """
    Send a message to a Telegram chat.
    
    Args:
        token (str): The bot token for the Telegram Bot API.
        chat_id (str): The chat ID where the message will be sent.
        message (str): The message to send.
    """

    TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to send message: {response.text}")
    
    return "Message sent successfully."

def receive_telegram_message(after_timestamp):
    
    TOKEN = os.getenv("BOT_TOKEN")
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(url).json()

    if not response["result"]:
        return []

    new_messages = []
    for update in response["result"]:
        if "message" in update:
            message = update["message"]
            if message["date"] > after_timestamp:
                new_messages.append({
                    "text": message["text"],
                    "date": datetime.fromtimestamp(message["date"]).strftime("%Y-%m-%d %H:%M")
                })

    return new_messages