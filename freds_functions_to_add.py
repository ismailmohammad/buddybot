# These functionality for the intents listed were created by Frederic but unfortunately
# was not able to be added for the demo. But nonetheless we will not let hard work go
# to waste. Shall add them in ASAP and train AI to recognize intents better.
# Sent Saturday November 4th, 2017 11:57 PM

#Buddy Bot

def bot_name(id):
    send_message(id, "Hi my name is Buddy Bot, BB for short.\nIt's a pleasure to meet you 😀")
    log("bot name has been given")


def get_user(id):
    name = users[id]["info"]["name"]
    if name is "":
        send_message(id, "I don't think you introducted yourself to me yet. My name is BB, what is yours?")
    else:
        send_message(id, "Your name is {}".format(name)
    log("user name has been given")


def instructions(id):
    str = ""
    list_form = """\t "{}" - {}\n"""
    info = {
        "What is yur name?": "Gives you BB's name",
        "What is my name?": "BB remembers! BB would give you your name"
        "My name is ___": "BB would remember your name for next time",
        "Remind me to ___ every ___ ___": "Tell BB to remind you some for some kind of interval, and BB would be sure to let you know!",
        "Stop reminding me to ___": "Made a mistake? Let BB know and BB would stop reminding you",
        "When do I ___", "BB would give you information on when your next reminder is"
    }
    send_message(id, "Buddy Bot is your companion who helps remind you to do activities to develop better life habits and improve both physical & mental health through conversation. Here are some examples of my features:")
    for i in info:
        str += list_form.format(i, info[i])
    send_message(id, str)
    send_message(id, "Find out more about me and my creators at https://bibambot.net.")
    log("instructions have been sent")


def set_user(id, items):
    name = items["contact"][0]["value"]
    users[id]["info"]["name"] = name
    send_message(id, "I will remember that. Nice to meet you {}".format(name))
    log("user has been set")
