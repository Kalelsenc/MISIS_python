import telebot;
import urllib.request
bot = telebot.TeleBot('ни ни');
storage={}

@bot.message_handler(commands=['start'])
def start_message(message):
    start_menu = telebot.types.ReplyKeyboardMarkup(True, True)
    start_menu.row('Доступность сайта МИСиС', 'Анализ текста', 'Бот калькулятор')
    bot.send_message(message.chat.id, 'Привет, выбери пункт меню', reply_markup=start_menu)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'доступность сайта мисис':
        if urllib.request.urlopen("https://misis.ru/").getcode()==200:
            bot.send_message(message.chat.id, 'Сайт МИСиС в норме')
            start_message(message)
        else:
            bot.send_message(message.chat.id, 'Сайт МИСиС не в норме')
            start_message(message)
    elif message.text.lower() == 'анализ текста':
        msg=bot.send_message(message.chat.id, 'Наберите свой текст ниже:')
        bot.register_next_step_handler(msg, analis)
    elif message.text.lower()=='бот калькулятор':
        operators_menu = telebot.types.ReplyKeyboardMarkup(True, True)
        operators_menu.row('+', '-', '*','/')
        msg=bot.send_message(message.chat.id,'Введите знак:',reply_markup=operators_menu)
        bot.register_next_step_handler(msg, mOperator)
    else:
        bot.reply_to(message, 'Фигню ты написал')
        start_message(message)
        

def analis(message):
    import collections
    import re

    count=collections.Counter()
    poem=str(message.text.lower())
    poem=re.sub(r'[^\w\s]','',poem)
    for word in poem.split():
        count[word]+=1

    max=0
    maxlen=0

    for i in count:
        if len(i)>maxlen:
            maxleni=i
            maxlen=len(i)
    
        if count[i]>max:
            maxi=i
            max=count[i]

    for i in count:
        bot.send_message(message.chat.id, f"Слово: {i} встречается {count[i]}")

    bot.send_message(message.chat.id,'Наиболее часто встречающееся слово: '+maxi+", оно встречается в стихотворении: "+str(max)+" раз(a)")
    bot.send_message(message.chat.id,'Cамое длинное слово: '+maxleni+", с количеством символов: "+str(maxlen))
    start_message(message)

def init_storage(user_id):
  storage[user_id] = dict(operator=None, first_number=None, second_number=None)

def store_number(user_id, key, value):
  storage[user_id][key] = dict(value=value)

def get_number(user_id, key):
  return storage[user_id][key].get('value')


def mOperator(message):
    init_storage(message.from_user.id)
    if message.text=='+' or message.text=='-' or message.text=='/' or message.text=='*':
        operator = message.text
        store_number(message.from_user.id, "operator", operator)
        bot.reply_to(message,"Введи первое число: ")
        bot.register_next_step_handler(message, firstNum)
    

def firstNum(message):
    first_number = message.text

    if not first_number.isdigit():
        msg = bot.reply_to(message, 'Вводи только целые числа!')
        bot.register_next_step_handler(message, firstNum)
        return

    store_number(message.from_user.id, "first_number", first_number)
    bot.reply_to(message, "Введи второе число: ")
    bot.register_next_step_handler(message, secNum)

def secNum(message):
    second_number = message.text

    if not second_number.isdigit():
        msg = bot.reply_to(message, 'Вводи только целые числа!')
        bot.register_next_step_handler(message, secNum)
        return

    store_number(message.from_user.id, "second_number", second_number)

    number_1 = get_number(message.from_user.id, "first_number")
    number_2 = get_number(message.from_user.id, "second_number")
    operator = get_number(message.from_user.id, "operator")

    if operator=='+':
        result = int(number_1) + int(number_2)
        bot.reply_to(message, f"Ответ: {result}")
    elif operator=='*':
        result = int(number_1) * int(number_2)
        bot.reply_to(message, f"Ответ: {result}")
    elif operator=='-':
        result = int(number_1) - int(number_2)
        bot.reply_to(message, f"Ответ: {result}")
    elif operator=='/':
        if int(number_2)!=0:
            result = int(number_1) / int(number_2)
            bot.reply_to(message, f"Ответ: {result}")
        else:
            bot.reply_to(message, 'Фигню ты написал')
    start_message(message)


bot.polling(none_stop=True, interval=0)
