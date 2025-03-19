# Project polaris aka meme bot
import telebot
import random
import schedule
import time
from threading import Thread
import os

TOKEN = '7640406495:AAHBgK2GvWQYjdGt8f_7gGxRMrwrtgec7oY'
bot = telebot.TeleBot(TOKEN)

#шлях до папки з мемами
UPLOAD_FOLDER = r"c:\memes/"
if not os.path.exists(UPLOAD_FOLDER):  # перевірка на існування папки
    os.makedirs(UPLOAD_FOLDER)

# список мемів
memes = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "7.jpg", "8.jpg", "9.jpg", "10.jpg", "11.jpg", "12.jpg", "13.jpg", "14.jpg", "15.jpg", "16.jpg", "17.jpg", "18.jpg", "19.jpg", "20.jpg"]

# список текстових жартів
jokes = [
    "Чому програмісти не люблять ходити в ліс? Бо там є баги!",
    "Як програміст робить какао? Програма: \"for i in range(3): milk, sugar, cocoa; mix; pour into cup\".",
    "Я не лінуюсь, я просто знаходжу ефективніші способи нічого не робити.",
    "Якщо ви не можете знайти проблему, то, ймовірно, ви і є проблема.",
    "Стоять наркоман та його друг, один показує пальцем на курку і каже -Братан це куриця? а інший йому відповідає -Нє це хаваєця. ",
    "Скільки важить один кілограм металу? Залежить від того, як ви його важите.",
]

# змінна для мема дня
meme_of_the_day = ""

@bot.message_handler(content_types=['photo'])
def recieve_meme(message):
    try:
        # дістаємо інформацію про надісланий мем
        file_info = bot.get_file(message.photo[-1].file_id)
        # завантажуємо мем
        downloaded_file = bot.download_file(file_info.file_path)
        # зберігаємо мем на комп'ютері під унікальним іменем
        file_name = str(len(memes) + 1) + "jpg"
        with open(UPLOAD_FOLDER + file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        # додаємо назву мема в список memes
        memes.append(file_name)
        bot.reply_to(message, "Мем отримано і збережено")
    except Exception as e:
        bot.reply_to(message, "Сталася помилка при завантаженні мема: " + str(e))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Я мемний бот. Напишіть /meme для отримання мемів, /joke для отримання жартів або /help для детальнішої інформації.")

# Команда для отримання мема дня
@bot.message_handler(commands=['meme_of_the_day'])
def send_meme_of_the_day(message):
    try:
        if meme_of_the_day:
            with open(UPLOAD_FOLDER + meme_of_the_day, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.reply_to(message, "Мем дня ще не обрано, спробуйте пізніше.")
    except Exception as e:
        bot.reply_to(message, "Сталася помилка при надсиланні мема дня: " + str(e))


@bot.message_handler(commands=['meme'])
def send_random_meme(message):
    try:
        if memes:
            meme = random.choice(memes)
            with open(UPLOAD_FOLDER + meme, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.reply_to(message, "Мемів поки немає")
    except Exception as e:
        bot.reply_to(message, "Сталася помилка при надсиланні мема: " + str(e))

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
    Привіт! Ось доступні команди:
    
    /start - Початок роботи з ботом.
    /meme - Отримати випадковий мем.
    /joke - Отримати випадковий жарт.
    /meme_of_the_day - Отримати мем дня.
    
    Надішліть жарт, щоб додати його до списку.
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['joke'])
def send_random_joke(message):
    try:
        if jokes:
            joke = random.choice(jokes)
            bot.send_message(message.chat.id, joke)
        else:
            bot.reply_to(message, "Жартів поки немає")
    except Exception as e:
        bot.reply_to(message, "Сталася помилка при надсиланні жарту: " + str(e))

# Додаємо новий жарт до списку
@bot.message_handler(func=lambda message: True)
def add_joke(message):
    try:
        joke = message.text
        if joke not in jokes:  # перевірка, щоб не додавати однакові жарти
            jokes.append(joke)
            bot.reply_to(message, "Жарт успішно додано!")
        else:
            bot.reply_to(message, "Цей жарт уже є в списку.")
    except Exception as e:
        bot.reply_to(message, "Сталася помилка при додаванні жарту: " + str(e))

# Функція для вибору мема дня
def choose_meme_of_the_day():
    global meme_of_the_day
    meme_of_the_day = random.choice(memes)

# Створення планувальника для вибору мема дня
def job():
    try:
        choose_meme_of_the_day()
        print(f"Мем дня обрано: {meme_of_the_day}")
    except Exception as e:
        print(f"Помилка при виборі мема дня: {str(e)}")

# Функція для запуску планувальника
def run_scheduler():
    schedule.every().day.at("09:00").do(job)  # вибір мема дня о 9:00
    while True:
        schedule.run_pending()
        time.sleep(1)

# Стартуємо планувальник у окремому потоці
Thread(target=run_scheduler).start()

bot.polling()