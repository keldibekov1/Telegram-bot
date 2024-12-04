import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = 'TOKEN'
CHAT_ID = '@'  # Kanal yoki guruh nomi yoki ID-si
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, "Assalomu alaykum! Iltimos, ismingizni kiriting:")

@bot.message_handler(func=lambda message: message.chat.id in user_data and 'name' not in user_data[message.chat.id])
def get_name(message):
    chat_id = message.chat.id
    user_data[chat_id]['name'] = message.text

    # Telefon raqamini olish uchun tugma
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = telebot.types.KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)
    markup.add(button)

    bot.send_message(chat_id, "Iltimos, telefon raqamingizni yuboring:", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def get_contact(message):
    chat_id = message.chat.id
    if message.contact is not None:
        user_data[chat_id]['phone'] = message.contact.phone_number
        bot.send_message(chat_id, "Endi murojaatingizni kiriting:", reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: message.chat.id in user_data and 'phone' in user_data[message.chat.id] and 'message' not in user_data[message.chat.id])
def get_message(message):
    chat_id = message.chat.id
    user_data[chat_id]['message'] = message.text

    # Ma'lumotlarni birlashtirish
    response = f"📝 *Yangi murojaat!* 📝\n\n"
    response += f"👤 *Ism:* {user_data[chat_id]['name']}\n"
    response += f"📞 *Telefon raqami:* {user_data[chat_id]['phone']}\n"
    response += f"✉️ *Murojaat:* {user_data[chat_id]['message']}\n"
    response += f"🆔 *Chat ID:* {chat_id}"  # Foydalanuvchining chat ID-si

    

    # Inline button yordamida profilga havola qo'shish
    inline_markup = InlineKeyboardMarkup()
    inline_button = InlineKeyboardButton(text="Foydalanuvchi profiliga o'tish", url=f"tg://user?id={chat_id}")
    inline_markup.add(inline_button)

    # Murojaatni kanalga yuborish
    bot.send_message(CHAT_ID, response, parse_mode='Markdown', reply_markup=inline_markup)  # Kanalga yuborish
    bot.send_message(chat_id, "Murojaatingiz qabul qilindi. Rahmat!")

bot.polling()
