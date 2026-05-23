import os

import firebase_admin

from firebase_admin import credentials

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

FIREBASE_CREDENTIALS_PATH = os.path.join(
    BASE_DIR,
    "rentout-in-8b207-firebase-adminsdk-fbsvc-13aeff4512.json"
)

if not firebase_admin._apps:

    cred = credentials.Certificate(
        FIREBASE_CREDENTIALS_PATH
    )

    firebase_admin.initialize_app(cred)

    print("Firebase initialized successfully")