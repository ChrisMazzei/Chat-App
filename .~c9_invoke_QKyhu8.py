# app.py
from os.path import join, dirname
from dotenv import load_dotenv
from random import randint
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
import editdistance

onlineUsers = []
userIdNum = -1

ADDRESSES_RECEIVED_CHANNEL = 'addresses received'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

#sql_user = os.environ['SQL_USER']
#sql_pwd = os.environ['SQL_PASSWORD']
#dbuser = os.environ['USER']

database_uri = os.environ['DATABASE_URL']
#'postgresql://{}:{}@localhost/postgres'.format(sql_user, sql_pwd)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()
print("sessions = " + str(db.session))
db.session.commit()

def emit_all_addresses(channel):
    # TODO - Content.jsx is looking for a key call for all addresses
    all_addresses = [db_address.message for db_address in db.session.query(models.Chatlog).all()]
    #print("printing below")
    #print(all_addresses)
    
    socketio.emit(channel, {
        'allAddresses': all_addresses
    })

@socketio.on('connect')
def on_connect():
    userIdNum = randint(0, 100000)
    username = "user" + str(userIdNum)
    
    print('user' + str(userIdNum) + ' connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    })
    emit_usernames('username', username)
    emit_all_addresses(ADDRESSES_RECEIVED_CHANNEL)
    
def emit_usernames(channel, username):
    #all_usernames = [db_username.username for db_username in db.session.query(models.Chatlog).all()]
    socketio.emit(channel, {
        'allNames' : username
    })

@socketio.on('disconnect')
def on_disconnect():
    print('user' + str(userIdNum) + ' disconnected!')
    print ('Someone disconnected!')

@socketio.on('new address input')
def on_new_address(data):
    print("Got an event for new address input with data:", data)
    if data["message"] == "!! about":
        db.session.add(models.Chatlog(bot.get(data["message"])))
        db.session.commit();
    else
        db.session.add(models.Chatlog(data["message"]));
    db.session.commit();
    
    """
    dist = 999999
    correctWord = ""
    
    print("-----------------")
    print(str(db.session.query(models.Usps).all()))
    print("-----------------")
    all_addresses = [db_address.name for db_address in db.session.query(models.Usps).all()]
    for a in all_addresses:
        tmpDist = editdistance.eval(a, data["name"])
        if tmpDist < dist:
            dist = tmpDist
            correctWord = a

    if data["name"] not in all_addresses and dist > 2:
        
        
        print("Added " + data["name"] + " to the list! Your List is" +
        " now: " + str(all_addresses))
    elif dist <= 2 and dist > 0:
        print("'" + correctWord + "'" + " is already in the list, and I assume" +
        " you spelled it the British way when you tried to add '" + data["name"] + "'")
    else:
        print(data["name"] + " is already in the list")
    """
    emit_all_addresses(ADDRESSES_RECEIVED_CHANNEL)

@app.route('/')
def index():
    emit_all_addresses(ADDRESSES_RECEIVED_CHANNEL)

    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
