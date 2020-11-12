from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
from flask_socketio import SocketIO, join_room, leave_room

from db import get_user
import pyrebase
import requests

import sys

requests.get('http://www.google.com')

from utilisateur import User

firebaseConfig = {
    "apiKey": "AIzaSyDGqgT6sWRZAUNQb21GudL06pkMhGF20sw",
    "authDomain": "attestation-e5fe9.firebaseapp.com",
    "databaseURL": "https://attestation-e5fe9.firebaseio.com",
    "projectId": "attestation-e5fe9",
    "storageBucket": "attestation-e5fe9.appspot.com",
    "messagingSenderId": "1034011984263",
    "appId": "1:1034011984263:web:e6e9adae72f09b1fa8d322",
    "measurementId": "G-YRBFHY1BXE"
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
database = firebase.database()
authenti = firebase.auth()
app = Flask(__name__)
app.secret_key = "sfdjkafnk"
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)

        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for('home'))
        else:
            message = 'Failed to login!'
    return render_template('login.html', message=message)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/sign/", methods=['GET', 'POST'])
def sign():
    return render_template('sign.html')


@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('postale')

    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])


@login_manager.user_loader
def load_user(username):
    return get_user(username)


@app.route('/inscription/', methods=['GET', 'POST'])
def inscription():
    email = request.form.get("email1")
    password = request.form.get("password1")
    print(request.form.get("email1"))
    print(request.form.get("password1"))
    user = authenti.create_user_with_email_and_password(email, password)
    data = {"nom": request.form.get("nom1"),
            "email": request.form.get("email1"),
            "prenom": request.form.get("prenom1"),
            "datena": request.form.get("datena1"),
            "lieuna": request.form.get("lieuna1"),
            "adresse": request.form.get("adress1"),
            "adresse2": request.form.get("adress2"),
            "ville": request.form.get("ville1"),
            "codepostale": request.form.get("postale1"),
            }
    database.child("users").push(data, user['idToken'])
    database.child("utilisateur").child(data["nom"]).set(data)
    return render_template('index.html')


@app.route('/authen/', methods=['GET', 'POST'])
def authentification():
    email = request.form.get("email1")
    password = request.form.get("password")
    user = authenti.sign_in_with_email_and_password(email, password)
    params = database.child("users").get()
    for person in params.each():

        if person.val()['email'] == email:
            print(person.val()['nom'])
            return render_template('chat.html',
                                   username=person.val()['nom'],
                                   prenom=person.val()['prenom'],
                                   datena=person.val()['datena'],
                                   lieuna=person.val()['lieuna'],
                                   adress1=person.val()['adresse'],
                                   adress2=person.val()['adresse2'],
                                   postale=person.val()['codepostale'],
                                   ville=person.val()['ville']
                                   )


@app.route('/test/')
def test():
    params = firebase.authenti().current_user
    print(params)


if __name__ == '__main__':
    socketio.run(app, debug=True)
