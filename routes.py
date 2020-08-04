from flask import request, render_template
from flask_assistant import Assistant, ask, tell

from core.dialog.manager import DialogManger
from app import app

manager = DialogManger()

assist = Assistant(app, route='/webhook')


@assist.action('greating')
def greet_and_start():
    speech = "Hey! Are you male or female?"
    return ask(speech)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("chat1.html")
    elif request.method == "POST":
        rawAudio = request.get_data()
        try:
            return manager.process_message(rawAudio)
        except Exception as err:
            print(err)
            return "Something went wrong"
        resp = manager.engine.predict_speech(rawAudio)
        print('Yay, got Wit.ai response: ' + str(resp))
        return "success"
