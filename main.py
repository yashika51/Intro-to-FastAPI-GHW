from fastapi import FastAPI, HTTPException
from models import Answer
from models import Trivia
from typing import List
import json

app = FastAPI()

# Load trivia questions from a JSON file
with open("questions.json") as f:
    questions = json.load(f)

# In-memory scoreboard
scoreboard = {}


@app.get("/trivia", response_model=List[Trivia])
def get_trivia():
    trivia_list = []

    for q in questions:
        trivia = Trivia(
            id=q["id"],
            question=q["question"],
            points=q["points"]
        )
        trivia_list.append(trivia)

    return trivia_list


@app.post("/trivia/answer/{question_id}")
def answer_question(question_id: int, answer: Answer):
    # Find the question with the given ID
    question = None
    for q in questions:
        if q["id"] == question_id:
            question = q
            break

    # If question not found, return error
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check if the answer is correct (case-insensitive)
    if answer.answer.lower().strip() == question["answer"].lower().strip():
        is_correct = True
        points = question["points"]
        scoreboard[answer.username] = scoreboard.get(answer.username, 0) + points
    else:
        is_correct = False
        scoreboard.setdefault(answer.username, 0)

    return {
        "correct": is_correct,
        "score": scoreboard[answer.username]
    }


@app.get("/trivia/leaderboard")
def get_leaderboard():
    # Convert scoreboard dictionary to a list of dicts
    leaderboard = []
    for username, score in scoreboard.items():
        leaderboard.append({"username": username, "score": score})

    # Sort the list by score (highest first)
    leaderboard.sort(key=lambda entry: entry["score"], reverse=True)

    return leaderboard
