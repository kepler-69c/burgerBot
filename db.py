import firebase_admin
from firebase_admin import credentials, firestore
import secrets

# Initialize Firebase (only ONCE)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def generate_token() -> str:
    return secrets.token_hex(8)  # 16-character secure random token


def add_email(address, sending="always") -> str:
    """
    add email to firestore db. if email already exists, it will be overwritten. returns token of the email record
    """
    token = generate_token()
    db.collection("emails").document(address).set(
        {"sending": sending, "token": token}
    )
    return token


def get_emails() -> dict:
    """
    get all emails with token && setting from firestore db
    """
    emails_ref = db.collection("emails")
    docs = emails_ref.stream()
    return {doc.id: doc.to_dict() for doc in docs}


def update_email_setting(address, new_sending, provided_token) -> bool:
    """
    update email sending setting for an existing email. Return True if successful
    """
    doc_ref = db.collection("emails").document(address)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        stored_token = data.get("token")
        if stored_token == provided_token:
            doc_ref.update({"sending": new_sending})
            return True
    return False


def delete_email(address, provided_token) -> bool:
    """
    delete email record from firestore db. Return True if successful
    """
    doc_ref = db.collection("emails").document(address)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        if data.get("token") == provided_token:
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
