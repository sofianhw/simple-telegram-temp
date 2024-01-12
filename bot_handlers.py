import telebot, os
from telebot import types
from db_utils import register_user, get_user_quota, decrease_quota

def setup_handlers(bot: telebot.TeleBot):

    def create_menu():
        menu = types.ReplyKeyboardMarkup(row_width=2)
        items = [types.KeyboardButton('/balance'), types.KeyboardButton('/deposit')]
        menu.add(*items)
        return menu

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        user_id = message.from_user.id
        username = message.from_user.username
        name = message.from_user.first_name

        response = register_user(user_id, username, name)
        bot.send_message(message.chat.id, f"Welcome, {name}! {response}", reply_markup=create_menu())

    @bot.message_handler(commands=['balance'])
    def handle_balance(message):
        user_id = message.from_user.id
        quota = get_user_quota(user_id)

        if quota is not None:
            bot.send_message(message.chat.id, f"Your current quota is: {quota}", reply_markup=create_menu())
        else:
            bot.send_message(message.chat.id, "You are not registered yet. Please use /start to register.", reply_markup=create_menu())
 
    @bot.message_handler(commands=['deposit'])
    def handle_deposit(message):
        markup = types.InlineKeyboardMarkup()
        user_id = message.from_user.id
        amounts = [1, 5, 10, 50]
        for amount in amounts:
            button = types.InlineKeyboardButton(f"${amount}", callback_data=f"deposit_{amount}_{user_id}")
            markup.add(button)
        
        bot.send_message(message.chat.id, "Choose an amount to deposit:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('deposit_'))
    def handle_query(call):
        amount = int(call.data.split('_')[1])
        # TODO: Integrate PayPal here and send the payment link

        bot.answer_callback_query(call.id)
        telegram_id = call.data.split('_')[2]
        bot_id = 'dibayarbayarinbot'

        base_url = os.environ.get('PAYPAL_URL')
        payment_url = f"{base_url}/?telegram_id={telegram_id}&amount={amount}&bot_id={bot_id}"
        bot.send_message(call.message.chat.id, f"You chose to deposit ${amount}. Please visit {payment_url}")
    
    @bot.message_handler(func=lambda message: True)
    def handle_all_messages(message):
        user_id = message.from_user.id
        new_quota = decrease_quota(user_id)

        if new_quota is not None:
            bot.reply_to(message, f"Ok, your remaining quota is: {new_quota}")
        else:
            bot.reply_to(message, "You have no remaining quota. Please top up. /deposit")
