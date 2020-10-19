# app.py
from os.path import join, dirname
from dotenv import load_dotenv
from random import randint
from chatbot import Chatbot
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
import editdistance


ADDRESSES_RECEIVED_CHANNEL = 'messages received'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()

db.session.commit()

def emit_all_messages(channel):
    all_messages = [db_message.message for db_message in db.session.query(models.Chatlog).all()]
    
    socketio.emit(channel, {
        'allMessages': all_messages
    })
    
@socketio.on('connect')
def on_connect():
    print("A user has connected.")
    emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)

@socketio.on('disconnect')
def on_disconnect():
   print ("A user has disconnected.")

@socketio.on('new message input')
def on_new_message(data):
    # this is used to strip away the nickname infront of the chat message
    botcommand = data["message"].lstrip(":")
    
    chat = Chatbot(botcommand)
    if chat.checkcommand():
        db.session.add(models.Chatlog(chat.getcommand()));
        db.session.commit();
    else:
        db.session.add(models.Chatlog(data["nickname"] + ": " + data["message"]));
        db.session.commit();
    
    emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)

@app.route('/')
def index():
    emit_all_messages(ADDRESSES_RECEIVED_CHANNEL)

    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
