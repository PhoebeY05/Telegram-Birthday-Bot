import telebot
from datetime import date

USER_ID = ""
BOT_TOKEN = "7062079662:AAFuS_0wxCpdXPqyolzXwHg25oRO6dpvVDA"
bot = telebot.TeleBot(BOT_TOKEN)

birthdays = []
today = date.today().strftime("%m%d") 

def Birthdays(calendar):
    event = False
    set = []
    bday = []
    for line in calendar.read().split("\n"):
        if line == "BEGIN:VEVENT":
            event = True
        elif line == "END:VEVENT":
            event = False
        if event:
            line = line.split(":")
            if line[0] == "DTSTART;VALUE=DATE":
                set.append(line[1][4:])
            elif line[0] == "SUMMARY":
                set.append(line[1])
        if not event:
            bday.append(set)
            set = []
    bday = [b for b in bday if b != []]
    return bday

@bot.message_handler(commands= ["start"])
def instructions(message): 
    global USER_ID
    USER_ID = message.chat.id
    bot.reply_to(message, "This bot reminds users to wish someone happy birthday based on their calendar.\n\nCOMMANDS: \nUse /cal to add a .ics file.\nUse /add to add a new birthday.\nUse /list to obtain a list of all birthdays (including newly added ones)")
    


@bot.message_handler(commands= ["add"])
def add_birthday(message): 
    reply = bot.reply_to(message, "Send a message in the format \"Birthday(MMDD), Name\"!")
    bot.register_next_step_handler(reply, new_birthday)



def new_birthday(message):
    msg = message.text.split(", ")
    birthdays.append(msg)
    if today == msg[0]:
        bot.send_message(USER_ID ,f"Wish {msg[1]} happy birthday!")

@bot.message_handler(commands= ["cal"])
def add_calendar(message):
    reply = bot.reply_to(message, "Send a .ics file!")
    bot.register_next_step_handler(reply, new_calendar) 
    
def new_calendar(message):
    global USER_ID
    USER_ID = message.chat.id
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    with open(file_name, 'r') as new_file:
        global birthdays
        birthdays = Birthdays(new_file)


@bot.message_handler(commands= ["list"])
def list_birthdays(message): 
    msg = ""
    if birthdays == []:
        msg = "Please add a calendar before using this command!"
    else:
        for bday in birthdays:
            msg += f"{bday[1]}: {bday[0][:2]}/{bday[0][2:]}\n"
    bot.reply_to(message, msg)


for birthday in birthdays:
    if today == birthday[0]:
        bot.send_message(USER_ID ,f"Wish {birthday[1]} Happy Birthday!")
bot.infinity_polling()