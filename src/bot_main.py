from config import *
import telebot
import os
import pyautogui
bot = telebot.TeleBot(bot_token)

tasks = []

@bot.message_handler(commands=['start'])
def Main(message):
    if str(message.from_user.id) != my_id:
        bot.send_message(message.chat.id, "Владелец не распознан")
        print(message.from_user.id)
        return  # Ignore messages from non-owners
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    sleep_button = telebot.types.KeyboardButton("Спящий режим")
    confirm_game_button = telebot.types.KeyboardButton("Подтвердить игру")
    add_task_button = telebot.types.KeyboardButton("Добавить задачу")
    all_tasks_button = telebot.types.KeyboardButton("Весь список")
    markup.add(sleep_button, confirm_game_button)
    markup.add(add_task_button, all_tasks_button)
    bot.send_message(message.chat.id, f"Привет {message.from_user.first_name}\nСледующая строка, доступные действия:", reply_markup=markup)










@bot.message_handler()
def info(message):
    if str(message.from_user.id) != my_id:
        bot.send_message(message.chat.id, "Владелец не распознан")
        return  
    
    if message.text == "Спящий режим":
        bot.send_message(message.chat.id, "Компьютер переведен в спящий режим, бот отключен")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif message.text == "Подтвердить игру":
        bot.send_message(message.chat.id, "Игра подтверждена!")
        screen_width, screen_height = pyautogui.size()
        pyautogui.click(x=screen_width // 2, y=(screen_height // 2) - 40)

    elif message.text == "Весь список":
        if tasks:
            task_list = "\n".join(f"{i+1}. {task}" for i, task in enumerate(tasks))
            bot.send_message(message.chat.id, f"Список задач:\n{task_list}")
        else:
            bot.send_message(message.chat.id, "Список задач пуст.")

    elif message.text == "Добавить задачу":
        msg = bot.send_message(message.chat.id, "Введите задачу:")
        bot.register_next_step_handler(msg, add_task)
def add_task(message):
    task = message.text
    tasks.append(str(message.text))
    bot.send_message(message.chat.id, f"Задача '{task}' добавлена!")




bot.infinity_polling()