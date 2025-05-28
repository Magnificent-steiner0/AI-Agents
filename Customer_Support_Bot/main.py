from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from chatbot.bot import ask_bot

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class QueryRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
def get_chat_page():
    return FileResponse("static/chat.html")

@app.post("/chat")
def chat(request: QueryRequest):
    response = ask_bot(request.query)
    return {"response": response}
