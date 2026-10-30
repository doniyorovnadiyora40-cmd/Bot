import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
royxat = {}      #chat_id - key values ["task1","task2"]

def royxat(message):
    return royxat.setdefault(message.chat.id, [])   # yo'q bo'lsa bo'sh ro'yxat yaratadi

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message, "📝 ToDo bot\n/add matn — qo'shish\n/list — ro'yxat\n/done 0 — bajarildi\n/del 0 — o'chirish")

@bot.message_handler(commands=['add'])
def add(message):
    # matn = message.text.replace("/add", "", 1).strip()     # "/add Dars qilish" → "Dars qilish"
    # if matn == "":
    #     bot.reply_to(message, "Format: /add Dars qilish")
    #     return
    # r = royxat(message)
    # r.append("[ ] " + matn)
    # bot.reply_to(message, f"✅ #{len(r) - 1} qo'shildi: {matn}")   # oxirgi element raqami
    task = message.text.replace("/add","",1)
    if not task:
        bot.send_message(message.chat.id,"Format: /add Dars qilish")
        return
    tasks = royxat.get(message.chat.id,[])
    tasks.append(f"[ ] {task}")
    royxat[message.chat.id] = tasks
    bot.send_message(message.chat.id,f"{len(task) - 1}#qo'shildi: {task}")

@bot.message_handler(commands=['list'])
def royxatni_korsat(message):
    r = royxat(message)
    if len(r) == 0:
        bot.reply_to(message, "Ro'yxat bo'sh. /add bilan qo'shing")
        return
    qatorlar = [f"#{i} {v}" for i, v in enumerate(r)]   # "#0 [ ] Dars qilish"
    bot.reply_to(message, "\n".join(qatorlar))
# def list_(message):
#     tasks = royxat.get(message.chat.id,[])
#     if not tasks:
#         bot.send_message(message.chat.id,"/add orqali task qo'shing")
#         return
#     t = ""
#     for i,v in enumerate(tasks):
#         t = t.join(f"#{i} {v}\n")
#     bot.send_message(message.chat.id, t)
@bot.message_handler(commands=['done', 'del'])
def done_del(message):
    try:
        buyruq, raqam = message.text.split()       # "/done 0"
        idx = int(raqam)
        r = royxat.get(message.chat.id,[])
        if buyruq == "/done":
            r[idx] = r[idx].replace("[ ]", "[x]", 1)       # "[ ] Dars" → "[x] Dars"
            bot.reply_to(message, "✔️ Bajarildi")

        else:
            del r[idx]
            bot.reply_to(message, f"🗑 #{idx} o'chirildi")
    except (ValueError, IndexError):                # "x" son emas / #99 yo'q
        bot.reply_to(message, "Format: /done 0  yoki  /del 0")

@bot.message_handler(func=lambda m: True)
def universal(message):
    bot.send_message(message.chat.id, "Tushunmadim 🤔 /help")

bot.infinity_polling()