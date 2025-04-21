from config import *
import telebot
import os
import pyautogui
from datetime import datetime
import threading
import time

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
        screen_width, screen_height = pyautogui.size()
        pyautogui.click(x=screen_width // 2, y=(screen_height // 2) - 40)

    elif message.text == "Добавить задачу":
        bot.send_message(message.chat.id, "Введите задачу в формате:\n<время уведомления в формате ДД.ММ.ГГГГ ЧЧ:ММ>\n<описание задачи>")
        def add_task_step(message):
            if str(message.from_user.id) != my_id:
                bot.send_message(message.chat.id, "Владелец не распознан")
                return  # Ignore messages from non-owners
            try:
                lines = message.text.split("\n")
                if len(lines) != 2:
                    bot.send_message(message.chat.id, "Неверный формат. Попробуйте снова.")
                    return

                notification_date = lines[0].strip()
                description = lines[1].strip()
                datetime.strptime(notification_date, "%d.%m.%Y %H:%M")
                new_task = {
                    "task_id": len(tasks) + 1,
                    "notification_date": notification_date,
                    "status": "P",
                    "description": description,
                }
                tasks.append(new_task)
                bot.send_message(message.chat.id, "Задача успешно добавлена!")
            except ValueError:
                bot.send_message(message.chat.id, "Неверный формат даты. Попробуйте снова.")
            except Exception as e:
                bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

        bot.register_next_step_handler(message, add_task_step)



    elif message.text == "Весь список":
        bot.send_message(message.chat.id, "Кнопка сдохла иди нахуй")
        if not tasks:
            bot.send_message(message.chat.id, "Список задач пуст.")
        else:
            task_list = "Список задач:\n"
            for task in tasks:
                task_list += f"{task['notification_date']} - {STATUS_DISPLAY.get(task['status'], 'Неизвестный статус')} - {task['description']}\n"
            bot.send_message(message.chat.id, task_list)

def task_notification():
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        for task in tasks:
            if task["notification_date"] == now and task["status"] == "P":
                bot.send_message(my_id, f"Напоминание о задаче:\n{task['description']}")
        time.sleep(60)  # Проверяем каждую минуту

notification_thread = threading.Thread(target=task_notification, daemon=True)
notification_thread.start()



bot.infinity_polling()