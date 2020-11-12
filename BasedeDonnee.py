import pyrebase


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

def inscription() :
    email = User.inputemail4
    password = User.inputpassword4

    user = firebase.auth.create_user_with_email_and_password(email, password)
    inscription()