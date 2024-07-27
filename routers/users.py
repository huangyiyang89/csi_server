from fastapi import APIRouter, HTTPException,Depends
from sqlmodel import Session, select,SQLModel
from database import get_session
from models.eventtype import EventType
from models.user import User

router = APIRouter()

class LoginRequest(SQLModel):
    username: str
    password: str

@router.post("/login")
async def login(*,request: LoginRequest,session: Session = Depends(get_session)):
    """
    登录接口
    """
    user = session.exec(select(User).where(User.name == request.username)).first()
    if user.password == request.password:
        return {"message": "登录成功"}
    else:
        raise HTTPException(status_code=401, detail="用户名或密码错误")