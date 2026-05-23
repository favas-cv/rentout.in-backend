import firebase_admin
 
from firebase_admin import credentials

cred = credentials.Certificate(
    'config/firebase/rentout-in-8b207-firebase-adminsdk-fbsvc-13aeff4512.json'
) 

firebase_admin.initialize_app(cred)

