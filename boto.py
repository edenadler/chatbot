"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json

@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    GREETING_WORDS = ["hello", "hi", "hey", "yo", "heya", "shalom"]
    QUESTION_WORDS = ["who","what","where","when","why","how"]
    user_message = request.POST.get('msg')
    return_message = "I'm sorry, I don't understand"
    words = user_message.split()
    for word in words:
        if word.lower() in GREETING_WORDS:
            return_message = "Hi, how can I help you?"
            return json.dumps({"animation": "excited", "msg": return_message})
        elif word.lower() in QUESTION_WORDS or word[-1] == "?":
            return_message = "That's a great question."
            return json.dumps({"animation": "confused", "msg": return_message})
    return json.dumps({"animation": "confused", "msg": return_message})


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
