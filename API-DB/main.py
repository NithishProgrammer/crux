from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from AI import analyze_problem_and_solution

from database import Problems, UserModel, SessionLocal, init_db
from schemas import ProblemCreate, UserCreate, UserResponse , ProblemResponse , AIEvaluator
from security import (
    verify_password,
    get_password_hash,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # The server still starts if PostgreSQL is down, so "/" and "/docs" always load
    try:
        init_db()
        print("Database connected, tables ready.")
    except Exception as e:
        print(f"WARNING: could not connect to the database: {e}")
    yield


app = FastAPI(lifespan=lifespan)

# Origins are scheme + host + port only: no trailing slash, no path
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
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



@app.get("/")
def themain():
    return {
        "Message": "Welcome to CRUX - Find what's the problem",
        "Developer": "COGNIHUB"
    }


@app.post("/register/", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(UserModel).filter(UserModel.userid == user_data.userid).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = UserModel(
        userid=user_data.userid,
        username=user_data.username,
        password= get_password_hash(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/user/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.userid == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.userid})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/problems/")
def create_problem(problem_data: ProblemCreate, db: Session = Depends(get_db)):
    new_problem = Problems(
        userid=problem_data.userid,
        problem_ID=problem_data.problem_ID,
        problem=problem_data.problem,
        sector=problem_data.sector
    )
    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)
    return new_problem


@app.get("/problems")
def get_problems(db: Session = Depends(get_db)):
    problems = db.query(Problems).all()
    return problems


@app.post("/AI/evaluate/")
def evaluate_problem_and_solution(evaluator_data: AIEvaluator):
    problem_statement = evaluator_data.problem
    solution = evaluator_data.soln
    return analyze_problem_and_solution(problem_statement, solution)
