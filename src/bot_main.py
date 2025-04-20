from config import *
import telebot
import os
import pyautogui

bot = telebot.TeleBot(bot_token)
#{"task_id": 1, "notification_date": "2023-10-01 14:00", "status": "pending", "description": "Complete project report"}
#Статусы задач:
#D - Done - выполнена - ✅
#P - In Process - в процессе - 🔄
#F - Frozen - заморожена - ❄️
#A - Archived - архивирована - 📦

# Словарь для отображения статусов
STATUS_DISPLAY = {
    'D': '✅ Выполнена',
    'P': '🔄 В процессе',
    'F': '❄️ Заморожена',
    'A': '📦 В архиве'
}

tasks = [
    {"task_id": 1, "notification_date": "2023-10-01 14:00", "status": "P", "description": "Тестовая задача"},
]

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
        return  # Ignore messages from non-owners
    
    if message.text == "Спящий режим":
        bot.send_message(message.chat.id, "Компьютер переведен в спящий режим, бот отключен")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif message.text == "Подтвердить игру":
        bot.send_message(message.chat.id, "Игра подтверждена!")
        # Эмуляция нажатия ЛКМ в центре экрана
        screen_width, screen_height = pyautogui.size()
        pyautogui.click(x=screen_width // 2, y=(screen_height // 2) - 40)

    

bot.infinity_polling()