from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    userid: str
    username: str
    password: str


class UserResponse(BaseModel):
    # No password field here, so the hash is never sent back to the client
    userid: str
    username: str

    model_config = ConfigDict(from_attributes=True)


class ProblemCreate(BaseModel):
    userid: str
    problem_ID: int
    problem: str
    sector: str
    


class ProblemResponse(BaseModel):
    # No password field here, so the hash is never sent back to the client
    userid: str
    problem_ID: int
    problem: str
    sector: str

    model_config = ConfigDict(from_attributes=True)

class SolutionsCreate(BaseModel):
    userid: str
    problem_ID: int
    solution: str

class SolutionsResponse(BaseModel):
    userid: str
    problem_ID: int
    solution: str

class AIEvaluator(BaseModel):
    problem: str
    soln: str
    