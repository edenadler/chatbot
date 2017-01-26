"""
This is the template server side for ChatBot
"""
from datetime import datetime
from bottle import route, run, template, static_file, request
import json


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return_message = split_message(user_message)
    return json.dumps(boto_response(return_message))

def boto_response(return_message):
    return {"animation": return_message[1], "msg": return_message[0]}

def split_message(user_message):
    user_message = user_message.lower()
    words = user_message.lower().split()
    return interpret_words(words, user_message)

def interpret_words(words, user_message):
    GREETING_WORDS = ["hello", "hi", "hey", "yo", "heya", "shalom"]
    QUESTION_WORDS = ["who","what","where","when","why","how"]
    for word in words:
        if word in GREETING_WORDS:
            return greeting(words, user_message)
        elif word in QUESTION_WORDS or user_message.endswith("?") or "calculate" in user_message:
            return question(words, user_message)
        else:
            return "I'm sorry, I don't understand", "confused"

def greeting(words, user_message):
    variations = ["im","i'm","name is"]
    for word in variations:
        if word in user_message:
            name = " "+user_message.split(word + " ",1)[1].capitalize() +", "
        else:
            name = ""
    return "Hi,"+name+"how can I help you?", "waiting"


def question(words, user_message):
    math_operations = ["+","-","/","*","plus","minus","divided by","multiplied by"]
    if "calculate" in user_message:
        for operator in math_operations:
            if operator in user_message:
                # index = user_message.index(operator)
                result = eval(user_message[10:])
                print(result)
                return "The answer is: "+str(result), "dancing"
            else:
                return "I don't know how to calculate that, I'm sorry", "crying"

    if "what" in user_message:
        print("what")
        if "time" in user_message:
            #TODO:get rid of miliseconds
            continuation = "the time is "+str(datetime.time(datetime.now()))
        elif any(operator in math_operations for operator in user_message):
            continuation = 'if you want me to calculate it for you, say: "Calculate" followed by the thing you want me to calculate. For example: Calculate 4+4'
        else:
            return "I'm sorry, I don't understand", "confused"
    else:
        return "I'm sorry, I don't understand", "confused"

    return "Great question, "+continuation, "ok"


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
