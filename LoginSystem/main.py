from fastapi import FastAPI,HTTPException,Depends,Header
from sqlalchemy.orm import Session
from app.infra.db import User
from app.infra.deps import get_db
from pydantic import BaseModel
from app.infra.security import hash_password,check_password,create_token,get_payload
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI(title="LoginSystem")
security = HTTPBearer()

class User_register_info(BaseModel):
    user_name: str
    user_password: str
    user_email: str
class User_info(BaseModel):
    user_name: str
    user_password: str


# 用户注册
@app.post("/register")
def Register(user: User_register_info, db: Session = Depends(get_db)):
    if db.query(User).filter(User.user_name == user.user_name).first():
        raise HTTPException(status_code=400, detail="用户已存在")      
    registed_user = User(
        user_name = user.user_name, 
        password = hash_password(user.user_password), 
        email = user.user_email)
    db.add(registed_user)
    db.commit()
    return {"msg":"注册成功"}

# 用户登录
@app.post("/login")
def Login(user: User_info, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(user.user_name==User.user_name).first()
    if (not db_user) or (not check_password(user.user_password, db_user.password)):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = create_token(db_user.id, db_user.user_name)
    return {"token": token}

@app.get("/whoami")
def whoami(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="不包含Token")
    try:
        token = credentials.credentials
        payload = get_payload(token)
        return {"msg":"验证通过","payload": payload}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Token无效或过期")
