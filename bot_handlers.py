import telebot, os, base64, io
import json, requests
from telebot import types
from db_utils import register_user, get_user_quota, decrease_quota
from llm_utils import chat_ai, voice_ai, reset_ai, texttovoice
from pydub import AudioSegment

def decode_base64_to_bytes(base64_string):
    return base64.b64decode(base64_string)

def convert_bytes_io_to_base64(audio_bytes_io):
    audio_bytes_io.seek(0)
    audio_base64 = base64.b64encode(audio_bytes_io.read()).decode()
    return f"data:audio/oga;base64,{audio_base64}"

def setup_handlers(bot: telebot.TeleBot):

    def create_menu():
        menu = types.ReplyKeyboardMarkup(row_width=2)
        items = [
            types.KeyboardButton('/balance'), 
            types.KeyboardButton('/deposit'),
            types.KeyboardButton('/reset'),
            types.KeyboardButton('/about')
        ]
        menu.add(*items)
        return menu

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        user_id = message.from_user.id
        username = message.from_user.username
        name = message.from_user.first_name

        response = register_user(user_id, username, name)
        # bot.send_message(message.chat.id, os.environ.get('START').format(username=name), reply_markup=create_menu())
        voice_response = texttovoice(os.environ.get('START').format(username=name))
        with open('audio.mp3','wb') as f:
            f.write(decode_base64_to_bytes(voice_response.split(',')[1]))
        
        # Use pydub to convert the MP3 file to the OGG format
        sound = AudioSegment.from_mp3("audio.mp3")
        sound.export("voice_message_replay.oga", format="oga")

        # Send the transcribed text back to the user as a voice
        voice = open("voice_message_replay.oga", "rb")
        bot.send_voice(message.chat.id, voice)
        voice.close()
        bot.send_message(message.chat.id, os.environ.get('START').format(username=name), reply_markup=create_menu())
        os.remove("voice_message_replay.oga")
        os.remove("audio.mp3")

    @bot.message_handler(commands=['reset'])
    def handle_balance(message):
        res = reset_ai(message.chat.id)
        bot.send_message(message.chat.id, os.environ.get('RESET'), reply_markup=create_menu())

    @bot.message_handler(commands=['about'])
    def handle_balance(message):
        bot.send_message(message.chat.id, os.environ.get('ABOUT'), reply_markup=create_menu())

    @bot.message_handler(commands=['balance'])
    def handle_balance(message):
        user_id = message.from_user.id
        quota = get_user_quota(user_id)

        if quota is not None:
            bot.send_message(message.chat.id, os.environ.get('BALANCE').format(quota=quota), reply_markup=create_menu())
        else:
            bot.send_message(message.chat.id, "You are not registered yet. Please use /start to register.", reply_markup=create_menu())
 
    @bot.message_handler(commands=['deposit'])
    def handle_deposit(message):
        markup = types.InlineKeyboardMarkup()
        user_id = message.from_user.id
        amounts = [1, 5, 10, 50]
        for amount in amounts:
            button = types.InlineKeyboardButton(f"${amount} for {amount*3} chats", callback_data=f"deposit_{amount}_{user_id}")
            markup.add(button)
        
        bot.send_message(message.chat.id, "🔹 Choose an amount to deposit:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('deposit_'))
    def handle_query(call):
        amount = int(call.data.split('_')[1])
        # TODO: Integrate PayPal here and send the payment link

        bot.answer_callback_query(call.id)
        telegram_id = call.data.split('_')[2]
        bot_id = os.environ.get('BOT_USERNAME')

        base_url = os.environ.get('PAYPAL_URL')
        payment_url = f"{base_url}/?telegram_id={telegram_id}&amount={amount}&bot_id={bot_id}"
        bot.send_message(call.message.chat.id, f"You chose to deposit ${amount} for {amount*3} chats. Please visit {payment_url}")
    
    @bot.message_handler(content_types=["voice"])
    def handle_voice(message):
        user_id = message.from_user.id
        new_quota = decrease_quota(user_id)
        
        if new_quota is None:
            bot.reply_to(message, "You have no remaining coins. Please top up. /deposit")
        else:
            file_info = bot.get_file(message.voice.file_id)
            print(file_info)
            file = requests.get("https://api.telegram.org/file/bot{0}/{1}".format(os.environ.get('BOT_ID'), file_info.file_path))
            buffer = io.BytesIO()
            for chunk in file.iter_content(chunk_size=1024):
                if chunk:
                    buffer.write(chunk)
            
            audio_file = convert_bytes_io_to_base64(buffer)

            bot.send_chat_action(message.chat.id, "record_voice", 25)

            voice_ai_data = voice_ai(audio_file, message.chat.id)

            bot.send_chat_action(message.chat.id, "upload_voice", 25)
            
            with open('audio.mp3','wb') as f:
                f.write(decode_base64_to_bytes(voice_ai_data[0]['data']['voice'].split(',')[1]))
            
            # Use pydub to convert the MP3 file to the OGG format
            sound = AudioSegment.from_mp3("audio.mp3")
            sound.export("voice_message_replay.oga", format="oga")

            # Send the transcribed text back to the user as a voice
            voice = open("voice_message_replay.oga", "rb")
            bot.send_voice(message.chat.id, voice)
            voice.close()
            bot.send_message(message.chat.id, voice_ai_data[0]['data']['text'])
            os.remove("voice_message_replay.oga")
            os.remove("audio.mp3")
    
    @bot.message_handler(func=lambda message: True)
    def handle_all_messages(message):
        user_id = message.from_user.id
        new_quota = decrease_quota(user_id)

        if new_quota is not None:
            bot.send_chat_action(message.chat.id, "record_voice", 25)
            
            chat_reply = chat_ai(message.text, message.chat.id)['data']
            voice_response = texttovoice(chat_reply)

            bot.send_chat_action(message.chat.id, "upload_voice", 25)

            with open('audio.mp3','wb') as f:
                f.write(decode_base64_to_bytes(voice_response.split(',')[1]))
            
            # Use pydub to convert the MP3 file to the OGG format
            sound = AudioSegment.from_mp3("audio.mp3")
            sound.export("voice_message_replay.oga", format="oga")

            # Send the transcribed text back to the user as a voice
            voice = open("voice_message_replay.oga", "rb")
            bot.send_voice(message.chat.id, voice)
            voice.close()
            bot.send_message(message.chat.id, chat_reply)
            os.remove("voice_message_replay.oga")
            os.remove("audio.mp3")
        else:
            bot.reply_to(message, "You have no remaining coins. Please top up. /deposit")
