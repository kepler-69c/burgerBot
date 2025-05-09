import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import secrets
import base64
import json
import os

# load credentials from base64
# dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)
firebase_b64 = os.getenv("B64_FIREBASE_CREDENTIALS")
if not firebase_b64:
    raise RuntimeError("Missing B64_FIREBASE_CREDENTIALS env var")
firebase_json = json.loads(base64.b64decode(firebase_b64))
# alternatively (on local):
# firebase_json = "serviceAccountKey.json"

# Initialize Firebase (only ONCE)
cred = credentials.Certificate(firebase_json)
firebase_admin.initialize_app(cred)
db = firestore.client()


def generate_token() -> str:
    return secrets.token_hex(8)  # 16-character secure random token


def add_email(address, sending="always") -> str:
    """
    adds a new email only if it doesn't already exist.
    returns token of new/existing email
    """
    # search all existing emails
    emails_ref = db.collection("emails")
    docs = emails_ref.stream()
    for doc in docs:
        data = doc.to_dict()
        if data.get("email") == address:
            return doc.id

    # if not found, create new
    token = generate_token()
    db.collection("emails").document(token).set({"email": address, "sending": sending, "development": False})
    return token


def get_email(token) -> dict:
    doc_ref = db.collection("emails").document(token)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def get_emails() -> dict:
    """
    get all emails with token && setting from firestore db
    """
    emails_ref = db.collection("emails")
    docs = emails_ref.stream()
    return {doc.id: doc.to_dict() for doc in docs}


def update_settings(provided_token, new_sending) -> bool:
    """
    update email sending setting for an existing email. Return True if successful
    """
    doc_ref = db.collection("emails").document(provided_token)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update({"sending": new_sending})
        return True
    return False


def delete_email(provided_token) -> bool:
    """
    delete email record from firestore db. Return True if successful
    """
    doc_ref = db.collection("emails").document(provided_token)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.delete()
        return True
    return False


def get_token(address) -> str:
    """
    Fetch the token for a given email (for management/admin use only).
    """
    doc_ref = db.collection("emails").document(address)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("token")
    return None
