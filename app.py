import os
import sys
from datetime import datetime
import threading
import requests
from flask import Flask, request, json

app = Flask(__name__)
users = {}
colours = ["blue","red","black","yellow", "green", "purple","turqoise", "navy"]
swears = ["cspost", "php"]

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "<h1>Copyright The BuddyBot Team 2017<h1>", 200


# Function to get to entities (get_intent)
# return intent (as value) & other stuff (seperate json)
# set_remind, {duration: {...}, reminder: {...}, ...}
#
#
#
#
#


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    #sender = data.get()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    msg = messaging_event["message"]
                    timestamp = messaging_event["timestamp"]
                    message_text = messaging_event["message"]["text"]


                    try:
                        if sender_id not in users:
                            users[sender_id] = {
                                "info": {},
                                "events": {}
                            }
                        intent, entities = get_intent(msg["nlp"]["entities"])
                        log(entities) # Loggging the entities
                        if intent == "bot_name":
                            # Fred
                            log("This was called - bn")
                        elif intent == "get_user":
                            # Fred
                            log("This was called - gu")
                        elif intent == "set_user":
                            # Fred
                            log("This was called-su")
                        elif intent == "set_remind":
                            if "every" in message_text:
                                recurring = True
                            else:
                                recurring = False
                            set_remind(sender_id, entities, timestamp, recurring)
                        elif intent == "instructions":
                            #instructions(sender_id)
                            log("Instruct")
                        elif intent == "get_remind":
                            log("This was called -gr")
                        elif intent == "stop":
                            stop_reminder(sender_id, entities)
                        else:
                            log("Missing Intent :/")

                    except KeyError:
                        pass

    return "ok", 200


def stop_reminder(sender_id, entities):
    reminder_value = entities["reminder"]["value"]
    events = users[sender_id]["events"]

    for event in events:
        log(sender_id, event)
    log(sender_id, reminder_value)
    try:
        events[reminder_value]["thread_event"].set()
        log(events[reminder_value]["thread_event"].is_set())
        send_message(sender_id, "I would stop reminding you to {}".format(reminder_value))
    except KeyError:
        send_message(sender_id, reminder_value + " does not exist")


def set_remind(sender_id, entities, timestamp, recurring):
    duration_seconds = entities["duration"]["normalized"]["value"]
    input_unit = entities["duration"]["unit"]
    input_value = entities["duration"]["value"]
    if input_value > 1:
        input_unit += "s"

    duration_input = str(input_value) + " " + input_unit
    log(duration_input)
    reminder_value = entities["reminder"]["value"]
    end_time = timestamp + duration_seconds
    if recurring:
        recurring_string = " every "
    else:
        recurring_string = " in "


    users[sender_id]["events"][reminder_value] = {
        "duration": duration_seconds,
        "init_time": timestamp,
        "end_time": end_time,
        "thread_event": threading.Event()
    }

    fschedule(users[sender_id]["events"][reminder_value]["thread_event"] ,sender_id, reminder_value, duration_seconds, recurring)
    send_message(sender_id, ("I will remind you to " + reminder_value + recurring_string + duration_input))


def get_intent(nlp):
    intent = ""
    entities = {}

    try:
        for key in nlp:
            if key == "intent":
                intent = nlp[key][0]["value"]
                log(intent)
            else:
                entities[key] = nlp[key][0]
    except KeyError:
        pass

    return intent, entities



def fschedule(f_stop, sender_id, reminder_value, time, recurring):
    if not f_stop.is_set():
        send_message(sender_id, "I'm reminding you to {}.".format(reminder_value))
        # call f() again in X seconds
        if recurring:
            users[sender_id]["events"][reminder_value]["end_time"] += time
            threading.Timer(time, fschedule, [f_stop, sender_id, reminder_value, time, recurring]).start()
        else:
            remind_once(sender_id, reminder_value, time)
            users[sender_id]["events"][reminder_value]["thread_event"].set()
    else:
        users[sender_id]["events"][reminder_value] = {}

def remind_once(sender_id, reminder_value, time):
    timer = threading.Timer(time, send_message, [sender_id, ("I'm reminding you to {}.".format(reminder_value))])
    timer.start()


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
