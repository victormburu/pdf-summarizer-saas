import pyrebase
import os
#from pyrebase.pyrebase import Firebase
from dotenv import load_dotenv

load_dotenv()

firebaseconfig = {
    "apiKey": ("AIzaSyCLWkdQZHNf4c-a7jTj8vT1fhdiyGcFudo"),
    "authDomain": os.getenv("authDomain"),
    "databaseURL": os.getenv("databaseURL"),
    "projectId": os.getenv("projectID"),
    "storageBucket": os.getenv("storageBucket"),
    "messageSenderId": os.getenv("messageSenderID"),
    "appId": os.getenv("appID"),
    "measurementId": os.getenv("measurementID")
}

# DEBUG: Print one env value to confirm loading
#rint("✅ apiKey from ENV:", os.getenv("apiKey"))

firebase = pyrebase.initialize_app(firebaseconfig)
auth = firebase.auth()