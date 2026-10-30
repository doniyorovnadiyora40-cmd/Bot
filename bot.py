import json
import telebot
from config import TOKEN

bot = telebot.TeleBot(token=TOKEN)

Fayl = "todo.json"

def load():
    try:
        with open ("todo.json","r",encoding="utf-8") as fayl:
            return json.load(fayl)
    except:
        return {}

lists = load()

def save():
    with open(Fayl,"w",encoding="utf-8") as fayl:
        json.dump(lists,fayl,ensure_ascii=False,indent=4)
def tasks(chat_id):
    chat_id = str(chat_id)
    if chat_id not in lists:
        lists[chat_id] = []
    return lists[chat_id]
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message,"Salom! Men Ustudy botman.\nListni ko'rish uchun /help ni bosing!")
@bot.message_handler(commands=["help"])
def help(message):
    bot.reply_to(message,"""ToDo bot!\n/add - Vazifa qo'shish\n/list - Vazifalarni ko'rish\n/done 0 - Vazifani bajarish\n/del 0 - Vazifani o'chirish\n/stat - Statistika\n/clear - Hamma vazifani o'chirish""")
@bot.message_handler(commands=["add"])
def add(message):
    response = bot.reply_to(message, "Vazifa nomini yozing: ")
    bot.register_next_step_handler(response,add_finish)
def add_finish(message):
    text = message.text.replace("/add","",1).strip()
    if text == "":
        bot.reply_to(message,"Format: /add")
        return
    task = tasks(message.chat.id)
    task.append({
        "vazifa": text,
        "bajarildi": False
        })
    save()
    bot.reply_to(message,f"Vazifa qo'shildi: {text}")
@bot.message_handler(commands=["list"])
def list_tasks(message):
    task = tasks(message.chat.id)
    if len(task) == 0:
        bot.reply_to(message,"Vazifalar yo'q! /add bilan qo'shing!")
        return
    line = [f"#{i} {v}" for i, v in enumerate(task)]
    bot.reply_to(message,"\n".join(line))
@bot.message_handler(commands=["done"])
def done_finish(message):
    try:
        order, number = message.text.split()
        index = int(number)
        task = tasks(message.chat.id)
        if index >= 0 and index < len(task):
            task[index]["completed"] = True
            save()
            bot.reply_to(message, "Vazifa bajarildi!")
        else:
            bot.reply_to(message, "Bunday vazifa yo'q.")
    except ValueError:
        bot.reply_to(message, "Format: /done 0")
@bot.message_handler(commands=["del"])
def delete_task(message):
    try:
        order, number = message.text.split()
        task = tasks(message.chat.id)
        index = int(number)
        if index >= 0 and index < len(task):
            task.pop(index)
            save()
            bot.reply_to(message,f"#{index} o'chirildi!")
        else:
            bot.reply_to(message,"Vazifa topilmadi!")
    except:
        bot.reply_to(message,"Format: /del 0")
@bot.message_handler(commands=["stat"])
def statistics(message):
    task = tasks(message.chat.id)
    total = len(task)
    completed = 0
    for i in task:
        if i["Bajarildi"]:
            completed += 1
    bot.reply_to(message,f"Jami: {total}\nBajarilgan: {completed}\nBajarilmagan: {total - completed}")
@bot.message_handler(commands=["clear"])
def clear_tasks(message):
    response = bot.reply_to(message,"Hamma vazifani o'chirmoqchimisiz? ha/yoq")
    bot.register_next_step_handler(response,clear_tasks_finish)
def clear_tasks_finish(message):
    if message.text:
        answer = message.text.lower().strip()
    else:
        answer = ""
    if answer == "Ha" or answer == "ha" or answer == "HA":
        lists[str(message.chat.id)] = []
        save()
        bot.reply_to(message,"Hamma vazifalar o'chirildi!")
    elif answer == "yoq" or answer == "Yoq" or answer == "YOQ":
        bot.reply_to(message,"Bekor qilindi!")
    else:
        bot.reply_to(message,"Ha/yoq kiriting!")
@bot.message_handler(func=lambda message: True)
def unknown_message(message):
    bot.reply_to(message,"Tushunmadim. /help orqali todo botni ko'ring!")

print("Bot ishga tushdi!")
bot.infinity_polling()
