import telebot
from time import sleep
import requests
import database as data
token = '6335870150:AAG26JRjEaZacUrzlwTayYQXaBKMuU-t-Ac'
bot = telebot.TeleBot(token)
my_id = '6094444931'
parrot = False


#tiktok api
url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"
headers = {
	"X-RapidAPI-Key": "986202cc54mshf3e91f00bf51e4ap1dcfb5jsn9a1fc2650736",
	"X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
}

@bot.message_handler(content_types=['photo'])
def photo_id(message):
    bot.send_message(message.chat.id, message.photo[0].file_id)

# hi bye
def hello(message):
    word = "привет"
    return word in message.text.lower()
def bye(message):
    word = 'пока'
    return word in message.text.lower()


# hi
@bot.message_handler(content_types=['text'], func=hello)
def say_hello(message):
    bot.send_message(message.chat.id, f'Здаров, брат! Теперь {message.from_user.first_name} мой лучший друг!')


# bye
@bot.message_handler(content_types=['text'], func=bye)
def say_bye(message):
    bot.send_message(message.chat.id, 'Бывай!')




# commands
# start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здаров, брат, чё как поживаешь, расскажи чё-нибудь')
    data.new_user(message)

# stop
@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.chat.id, 'Заряд батареи кончился, ботецкий откисает')
    iroglifs = ('///', '\\\\\\', '|||', '.', '..', '...')
    for i in iroglifs:
        bot.send_message(message.chat.id, i)
        sleep(0.1)
    sleep(0.4)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAECd6hlfXoWMDN-7i0sI6WLXDYDgTTGlQACMBoAAg-jeUrvQYdTvbPRPTME')
    bot.stop_bot()


# parrot command
@bot.message_handler(commands=['parrot'])
def test(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('✅ Включить')
    btn2 = telebot.types.KeyboardButton('❌ Отключить')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text='Режим попугая - бот будет повторять за тобой, если ты вводишь обычный текст.', reply_markup=markup)


# tiktok saver
@bot.message_handler(commands=['tiktok'])
def tt_saver(message):
    bot.send_message(message.chat.id, 'Скинь сылочку на видоскик😜:')


# link validator
def is_tt(message):
    if 'tiktok.com/' in message.text:
        return True


# input link
@bot.message_handler(content_types=['text'], func=is_tt)
def tt_saver2(message):
    querystring = {"url": message.text, "hd": "1"}
    response = requests.get(url, headers=headers, params=querystring)
    try:
        bot.send_message(message.chat.id, 'Держи🤑')
        sleep(0.5)
        bot.send_video(message.chat.id, response.json()['data']['play'])
        data.video_load(message, response.json(), True)
    except KeyError:
        bot.send_message(message.chat.id, 'Нее, не катит, кидай рабочую ссылку, шлак мне не нужен')
        print('Голимая ссылка')
        data.video_load(message, response.json(), False)



# parrot
# enable
@bot.message_handler(func=lambda message: message.text == '✅ Включить')
def enable_parrot(message):
    global parrot
    parrot = True
    bot.send_message(message.chat.id, 'Пернатый подключён 🦜', reply_markup=telebot.types.ReplyKeyboardRemove())


# disable
@bot.message_handler(func=lambda message: message.text == '❌ Отключить')
def disable_parrot(message):
    global parrot
    parrot = False
    bot.send_message(message.chat.id, 'Пернатый отключён 🦜', reply_markup=telebot.types.ReplyKeyboardRemove())




# text
@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.first_name != 'Бибан')
def spy(message):
    bot.send_message(my_id, f'Текст: {message.text}\nОтправитель: {message.from_user.first_name}\nID чата отправителя: {message.chat.id}\n\n')
def repeat_message(message):
    if parrot:
        bot.send_message(message.chat.id, message.text)




# sticker spy
@bot.message_handler(content_types=['sticker'])
def sticker(message):
    bot.send_sticker(my_id, message.sticker.file_id)
    if parrot:
        bot.send_sticker(message.chat.id, message.sticker.file_id)




bot.polling(none_stop=True)
