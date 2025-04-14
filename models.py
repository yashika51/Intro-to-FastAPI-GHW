from pydantic import BaseModel


# Request model for answer submission
class Answer(BaseModel):
    username: str
    answer: str


# Response model for /trivia
class Trivia(BaseModel):
    id: int
    question: str
    points: int
