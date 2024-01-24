import requests, os

bot_id = os.environ.get('BOT_ID')

def send_chat(message_id, chat):
    base_url = f"https://api.telegram.org/bot{bot_id}/sendMessage"
    payload = {
        "chat_id": message_id,
        "text": chat
    }
    requests.post(base_url, data=payload)

