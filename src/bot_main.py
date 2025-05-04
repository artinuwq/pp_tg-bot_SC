from config import *
import telebot
import os
import pyautogui
bot = telebot.TeleBot(bot_token)
TASKS_FILE_PATH = os.path.join(os.path.expanduser('~'), 'Desktop', 'tasks.txt') 

def load_tasks():
    try:
        with open(TASKS_FILE_PATH, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

def save_tasks():
    with open(TASKS_FILE_PATH, 'w', encoding='utf-8') as file:
        for task in tasks:
            file.write(f"{task}\n")

tasks = load_tasks()


@bot.message_handler(commands=['start'])
def Main(message):
    if str(message.from_user.id) != my_id:
        bot.send_message(message.chat.id, "Владелец не распознан")
        print(message.from_user.id)
        return # Бла бла бла защита от не владельца
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    sleep_button = telebot.types.KeyboardButton("Спящий режим")
    confirm_game_button = telebot.types.KeyboardButton("Подтвердить игру")
    add_task_button = telebot.types.KeyboardButton("Добавить задачу")
    all_tasks_button = telebot.types.KeyboardButton("Весь список")
    delete_task_button = telebot.types.KeyboardButton("Удалить задачу")
    markup.add(sleep_button, confirm_game_button)
    markup.add(add_task_button, delete_task_button, all_tasks_button)
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

    elif message.text == "Удалить задачу":
        if tasks:
            task_list = "\n".join(f"{i+1}. {task}" for i, task in enumerate(tasks))
            msg = bot.send_message(message.chat.id, f"Текущие задачи:\n{task_list}\n\nВведите номер задачи для удаления:")
            bot.register_next_step_handler(msg, delete_task)
        else:
            bot.send_message(message.chat.id, "Список задач пуст.")

def delete_task(message):
    try:
        task_num = int(message.text) - 1
        if 0 <= task_num < len(tasks):
            deleted_task = tasks.pop(task_num)
            save_tasks()
            bot.send_message(message.chat.id, f"Задача '{deleted_task}' удалена!")
        else:
            bot.send_message(message.chat.id, "Неверный номер задачи!")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовой номер задачи!")

def add_task(message):
    task = message.text
    tasks.append(str(message.text))
    save_tasks() 
    bot.send_message(message.chat.id, f"Задача '{task}' добавлена!")



bot.infinity_polling()