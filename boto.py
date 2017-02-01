"""
This is the template server side for ChatBot
"""
from datetime import datetime
from bottle import route, run, template, static_file, request
import json
import random
import requests


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
    JOKE_WORDS = ["joke","tell"]
    for word in words:
        if word in GREETING_WORDS:
            return greeting(words, user_message)
        elif word in JOKE_WORDS:
            return jokes(words, user_message)
        elif word in QUESTION_WORDS or user_message.endswith("?") or "calculate" in user_message or "weather" in user_message:
            return question(words, user_message)
        else:
            return "I'm sorry, I don't understand", "confused"

def greeting(words, user_message):
    variations = ["im","i'm","name is"]
    for word in variations:
        if word in user_message:
            name = " "+user_message.split(word + " ",1)[1].capitalize() +", "
            break
        else:
            name = ""
    return "Hi,"+name+"how can I help you?", "waiting"


def jokes(words,user_message):
    joke_list = ["What is a programmer?...A person who fixed a problem you didn't know you had and in a way that you don't understand.",
                 "What is an algorithm?...It's a word used by programmers when they do not want to explain what they did.",
                 "What is hardware?...It's the part of the computer that you can kick!",
                 "What is the object-oriented way to become wealthy?...Inheritance",
                 "What is a programmer's favorite hangout spot?...Foo Bar",
                 "Why did the programmer quit his job?... Because he didn't get arrays"]
    joke = random.choice(joke_list)
    return joke , "laughing"

def question(words, user_message):
    math_operations = ["+","-","/","*","plus","minus","divided by","multiplied by"]
    WEATHER_WORDS = ["temperature", "weather", "forecast"]
    #TODO: add more options to the list
    options = ["about the time","to solve math problems", "about the weather"]
    if "weather in" in user_message:
        weather = requests.get("http://api.openweathermap.org/data/2.5/weather?APPID=de595487072c551664a7a2fecdb43b95&q="+user_message[11:]+"&cnt=10&mode=json&units=metric")
        weather_today = json.loads(weather.content)
        return "Today will be "+weather_today["weather"][0]["description"]+" with a temperature of "+str(weather_today["main"]["temp"])+" in "+weather_today["name"], "giggling"
    if "calculate" in user_message:
        for operator in math_operations:
            if operator in user_message:
                #TODO: only working for addition, make work for other operators
                result = eval(user_message[10:])
                print(result)
                return "The answer is: "+str(result), "dancing"
            else:
                return "I don't know how to calculate that, I'm sorry", "crying"

    if "what" in user_message:
        if "should i ask" in user_message:
            option = random.choice(options)
            return "Ask me "+option, "dancing"
        elif "time" in user_message:
            #TODO:get rid of miliseconds
            continuation = "the time is "+str(datetime.time(datetime.now()))
        elif any(word in user_message for word in WEATHER_WORDS):
            return "I'd be happy to get that for you. Please say: 'Weather in [name of city]'", "takeoff"
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
