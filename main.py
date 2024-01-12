import telebot, os
from bot_handlers import setup_handlers

# Initialize the bot with your token
bot = telebot.TeleBot(os.environ.get('BOT_ID'))

# Setup bot handlers
setup_handlers(bot)

# Start polling
bot.polling(none_stop=True)

