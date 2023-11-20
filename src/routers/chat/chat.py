from fastapi import APIRouter
from pydantic import BaseModel
from src.routers.chat.chatService import get_answer, get_documents

import src.utils.openAI as openAI

router = APIRouter(prefix="/chat", tags=["Chat"])

class Question(BaseModel):
    question: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "Wer ist Jasmina?"
                }
            ]
        }
    }

@router.post("/question/", tags=["Chat"])
async def login(question: Question):
    return get_answer(question.question)

@router.post("/document/", tags=["Chat"])
async def login(question: Question):
    return get_documents(question.question)