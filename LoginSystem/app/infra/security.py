import jwt
import bcrypt
import datetime

SECRETE_KEY = "onlytestkey"

def hash_password(password: str):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))
    return hashed.decode("utf-8")

def check_password(input_pw:str, pw:str):
    return bcrypt.checkpw(input_pw.encode("utf-8"),pw.encode("utf-8"))

def create_token(user_id:int, user_name:str):
    payload = {
        "id": user_id,
        "user_name": user_name,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=20)
    }
    return jwt.encode(payload, SECRETE_KEY, algorithm="HS256")

def get_payload(token: str):
    return jwt.decode(token, SECRETE_KEY, algorithms=["HS256"])