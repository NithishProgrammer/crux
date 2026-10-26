from fastapi import FastAPI, Depends, HTTPException, status, Request
import httpx
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, sessionmaker 
from database import UserModel , SessionLocal, engine
from schemas import UserCreate, UserResponse
from security import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Default Vite port
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5500/" ,
    "http://127.0.0.1:5500/src/ed.html"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userid: str = payload.get("userid")
        if userid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(UserModel).filter(UserModel.userid == userid).first()
    if user is None:
        raise credentials_exception
    return user

@app.get("/")
def themain():
    return {"Message" : "Welcome to Amdox API, You can Visit the Docs of the API for" , "Developer" : "Nithish (Group 1) (2month intern)"}
    
@app.post("/register/", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.userid == user_data.userid).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(user_data.password)
    new_user = UserModel(
        userid=user_data.userid,
        username=user_data.username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.userid == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"userid": user.userid})
    return {"access_token": access_token, "token_type": "bearer", "user": {"userid": user.userid, "username": user.username}}
