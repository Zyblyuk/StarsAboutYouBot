import telebot, requests
from telegram import ParseMode
from telebot import types
from bs4 import BeautifulSoup
from Token import token
from save_and_load import Users


bot = telebot.TeleBot(token)
isRunning_Other = False
List = Users("DataBase")


@bot.message_handler(commands=['help'])
def start(message):
    string = "Этот бот предназначен для определения ваших личных качеств. Для того чтобы начать, вы можете использовать команды /start и /anew. Если вы уже использовали эти команды, то вы можете пропустить этап заполнения полей, воспользовавшись командой /result, а также узнать вашу совместимость со второй половинкой с помощью команды /compatibility"
    bot.send_message(message.chat.id, string)


#collecting information about the user and moving them to the database
@bot.message_handler(commands=['start', 'anew'])
def start(message):
    global isRunning
    chat_id = message.chat.id
    text = message.text
    msg = bot.send_message(chat_id, 'Введите ваш год рождения:')
    bot.register_next_step_handler(msg, askYear)
    isRunning = True


def askYear(message):
    global List
    chat_id = message.chat.id
    text = message.text
    if not text.isdigit():
        msg = bot.send_message(chat_id, 'Год должен быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, askYear)
        return
    if int(text) < 1900 or int(text) > 2020:
        msg = bot.send_message(chat_id, 'Кажется мне, что ты врешь, введите ещё раз.')
        bot.register_next_step_handler(msg, askYear)
        return
    msg = bot.send_message(chat_id, 'Введите месяц: ')
    List.users.pop(chat_id, None)
    List.add(chat_id, text)
    bot.register_next_step_handler(msg, askMouns)


def askMouns(message):
    global List
    chat_id = message.chat.id
    text = message.text
    if not text.isdigit():
        msg = bot.send_message(chat_id, 'Месяц должен быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, askMouns)
        return
    if int(text) < 1 or int(text) > 12:
        msg = bot.send_message(chat_id, 'Кажется мне, что ты врешь, введите ещё раз.')
        bot.register_next_step_handler(msg, askMouns)
        return
    msg = bot.send_message(chat_id, 'Введите день рождения: ')
    List.add(chat_id, text)
    bot.register_next_step_handler(msg, askDay)


def askDay(message):
    global List
    chat_id = message.chat.id
    text = message.text
    if not text.isdigit():
        msg = bot.send_message(chat_id, 'Месяц должен быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, askDay)
        return
    if int(text) < 1 or int(text) > 31:
        msg = bot.send_message(chat_id, 'Кажется мне, что ты врешь, введите ещё раз.')
        bot.register_next_step_handler(msg, askDay)
        return
    msg = bot.send_message(chat_id, 'Введите Имя: ')
    List.add(chat_id, text)
    bot.register_next_step_handler(msg, askName)


def askName(message):
    global List
    chat_id = message.chat.id
    text = message.text
    msg = bot.send_message(chat_id, 'Введите Фамилию: ')
    List.add(chat_id, text)
    bot.register_next_step_handler(msg, askLast_Name)


def askLast_Name(message):
    global List
    chat_id = message.chat.id
    text = message.text
    List.add(chat_id, text)
    isRunning = False
    result(message)


@bot.message_handler(commands=['result'])
def result(message):
    global List
    URL = "https://my-calend.ru/kvadrat-pifagora/"
    if not message.chat.id in List.users:
        bot.send_message(message.chat.id, "Воспользуйтесь коммандой /start!")
        return
    arr = List.users[message.chat.id]
    for i in range(3):
        URL += str(arr[2 - i]) + "."
    character(message, URL)


def character(message, URL):
    global List
    keyboard = types.InlineKeyboardMarkup()
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    full_page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(full_page.content, 'lxml')
    p_el = soup.find("p")
    h3_el = soup.find("h3")
    temp = []
    t_List = {}
    nnn = ["Характер", "Здоровье", "Удача", "Энергетика", "Логика", "Чувство", "Познание", "Трудолюбие", "Память"]
    while p_el and h3_el:
        lst = h3_el.get_text().replace(',', '').split()
        if lst[0] in nnn:
            if lst[0] == 'Чувство':
                lst[0] = 'Доброта'
            temp.append(types.InlineKeyboardButton(lst[0], callback_data=lst[0]))
        t_List[lst[0]] = p_el.get_text()
        p_el = p_el.find_next_sibling("p")
        h3_el = h3_el.find_next_sibling("h3")
    List.temp_list.pop(message.chat.id, None)
    List.temp_list[message.chat.id] = t_List
    i = 0
    while i < len(temp):
        if i + 2 < len(temp):
            keyboard.add(temp[i], temp[i+1], temp[i+2])
        else:
            break
        i += 3
    bot.send_message(message.chat.id, "Выберете то, о чем вы хотите узнать", reply_markup=keyboard)


#collecting information about the second half of the user
@bot.message_handler(commands=['compatibility'])
def compatibility(message):
    global isRunning_Other, List
    chat_id = message.chat.id
    text = message.text
    if not chat_id in List.users:
        start(message)
    msg = bot.send_message(chat_id, 'Введите год рождения вашей второй половинки:')
    bot.register_next_step_handler(msg, askYear_Other)
    isRunning_Other = True


def askYear_Other(message):
    global List
    chat_id = message.chat.id
    text = message.text
    if not text.isdigit():
        msg = bot.send_message(chat_id, 'Год должен быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, askYear_Other)
        return
    if int(text) < 1900 or int(text) > 2020:
        msg = bot.send_message(chat_id, 'Кажется мне, что ты врешь, введите ещё раз.')
        bot.register_next_step_handler(msg, askYear_Other)
        return
    msg = bot.send_message(chat_id, 'Введите месяц рождения вашей второй половинки: ')
    List.temp_users.pop(chat_id, None)
    List.temp_add(chat_id, text)
    bot.register_next_step_handler(msg, askMouns_Other)


def askMouns_Other(message):
    global List
    chat_id = message.chat.id
    text = message.text
    if not text.isdigit():
        msg = bot.send_message(chat_id, 'Месяц должен быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, askMouns_Other)
        return
    if int(text) < 1 or int(text) > 12:
        msg = bot.send_message(chat_id, 'Кажется мне, что ты врешь, введите ещё раз.')
        bot.register_next_step_handler(msg, askMouns_Other)
        return
    msg = bot.send_message(chat_id, 'Введите день рождения вашей второй половинки: ')
    List.temp_add(chat_id, text)
    bot.register_next_step_handler(msg, askDay_Other)


def askDay_Other(message):
    global List
    chat_id = message.chat.id
    text = message.text
    if not text.isdigit():
        msg = bot.send_message(chat_id, 'Месяц должен быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, askDay_Other)
        return
    if int(text) < 1 or int(text) > 31:
        msg = bot.send_message(chat_id, 'Кажется мне, что ты врешь, введите ещё раз.')
        bot.register_next_step_handler(msg, askDay_Other)
        return
    msg = bot.send_message(chat_id, 'Введите Имя второй половинки: ')
    List.temp_add(chat_id, text)
    bot.register_next_step_handler(msg, askName_Other)


def askName_Other(message):
    global List
    chat_id = message.chat.id
    text = message.text
    msg = bot.send_message(chat_id, 'Введите Фамилию второй половинки: ')
    List.temp_add(chat_id, text)
    bot.register_next_step_handler(msg, askLast_Name_Other)


def askLast_Name_Other(message):
    global List
    chat_id = message.chat.id
    text = message.text
    List.temp_add(chat_id, text)
    isRunning_Other = False
    result_Other(message)


def result_Other(message):
    global List
    URL = "https://my-calend.ru/sovmestimost-po-date-rozhdeniya/"
    arr = List.users[message.chat.id]
    for i in range(3):
        URL += str(arr[2 - i]) + "."
    URL += '/'
    arr = List.temp_users[message.chat.id]
    for i in range(3):
        URL += str(arr[2 - i]) + "."
    character_Other(message, URL)


def character_Other(message, URL):
    global List
    keyboard = types.InlineKeyboardMarkup()
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    full_page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(full_page.content, 'lxml')
    p_el = soup.find("p")
    h2_el = soup.find("h2")
    t_List = {}
    while p_el and h2_el:
        keyboard.add(types.InlineKeyboardButton(h2_el.get_text(), callback_data=h2_el.get_text()))
        t_List[h2_el.get_text()] = p_el.get_text()
        p_el = p_el.find_next_sibling("p")
        h2_el = h2_el.find_next_sibling("h2")
    List.temp_list.pop(message.chat.id, None)
    List.temp_list[message.chat.id] = t_List
    bot.send_message(message.chat.id, "Нажмите, чтобы узнать подробнее.", reply_markup=keyboard)


#button handling
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global List
    if call.message.chat.id in List.temp_list:
        string = "<b>"+call.data+"</b>" + ":\n<em>" + List.temp_list[call.message.chat.id][call.data] + "</em>"
        bot.send_message(call.message.chat.id, string, parse_mode = 'html')
    else:
        bot.send_message(call.message.chat.id, "Выполните комманду /result")


if __name__ == '__main__':
     bot.polling(none_stop=True)
