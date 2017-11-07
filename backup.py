if message_text == "hello":
    send_message(sender_id, "Hello! Nice to meet you as well!")
    send_message(sender_id, "What is your favourite colour?")
elif message_text == "goodbye":
    send_message(sender_id, "Roger that! See you next time")
elif message_text in colours:
    message_string = "I like " + message_text + " too!"
    send_message(sender_id, message_string)
elif "remind me to" in message_text:
    # remind me to xxxx
    action_to_remind = message_text.split('every')[0].split("remind me to ")[1]
    time_amount = reminder.split(' every ')[1].split()[0]
    time_unit = reminder.split(' every ')[1].split()[1]

    if "minute" in time_unit:
        time_amount = int(time_amount) * 60
    elif "hour" in time_unit:
        time_amount = int(time_amount) * 3600
    elif "day" in time_unit:
        time_amount = int(time_amount) * 86400


    users[sender_id]["event"] = threading.Event()
    users[sender_id]["time"] = int(stuff[2])
    log(users[sender_id]["event"])
    log(users[sender_id]["time"])
    fschedule(users[sender_id]["event"], sender_id)
elif message_text == "stop":
    users[sender_id]["event"].set()
    users[sender_id]["time"] = 0
else:
    send_message(sender_id, "I'm sorry, I could not understand your request. Please try again.")
except KeyError:
pass

try:
sticker_text = messaging_event["message"]["sticker_id"]
if sticker_text == 369239263222822:
    send_message(sender_id, "I Like you too!")
except KeyError:
passs




TAKEN FROM app.py 4:33 AM:
    '''
    users[sender_id]["events"] = {entities["reminder"]["value"]: {}}
    users[sender_id]["events"][reminder_value] = {
        "duration": entities["duration"]["normalized"]["value"],
        "init_time": timestamp,
        "end_time": end_time,
        "thread_event": threading.Event()
    }
    '''
