import telebot, os, time
from bot_handlers import setup_handlers

# Initialize the bot with your token
bot = telebot.TeleBot(os.environ.get('BOT_ID'))

# Setup bot handlers
setup_handlers(bot)

# Start polling
while True:
    try:
        bot.infinity_polling(interval=0.1, timeout=10)
    except Exception as e:
        # Log the exception here
        print(f"Error encountered: {e}. Restarting polling...")
        time.sleep(1)

