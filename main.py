"""
FastAPI backend for Avinash Wagh's portfolio chatbot.

Run locally:
    uvicorn main:app --reload --port 8000

Endpoints:
    GET  /health              -> simple health check
    POST /api/chat            -> non-streaming answer, returns JSON
    POST /api/chat/stream     -> streaming answer (Server-Sent Events),
                                  for a "typing" effect in the frontend
"""

from pathlib import Path
import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from groq import Groq

from portfolio_data import PORTFOLIO, CONTACT_INFO

# ============================================================
# ENVIRONMENT
# ============================================================

# Looks for a .env file next to this file. Adjust the path if your
# .env lives elsewhere (e.g. parent.parent as in the original script).

# Find .env in week1/
env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(env_path)

my_api_key = os.getenv("Grok_key")

if not my_api_key:
    raise ValueError("API key not found")


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(api_key=my_api_key)

MODEL = "qwen/qwen3.8-27b"

# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(title="Avinash Wagh Portfolio Chatbot API")

# CORS: allow your frontend to call this API from the browser.
# Replace "*" with your actual frontend origin(s) in production,
# e.g. ["http://localhost:3000", "https://yourportfolio.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    category: str


# ============================================================
# STEP 1 - CLASSIFY THE QUESTION
# ============================================================

def analyze_question(question: str) -> dict:
    prompt = f"""
You are analyzing a question about Avinash Wagh's portfolio.

Classify the question into ONE of these categories:

- skills
- experience
- projects
- education
- achievements
- contact
- leadership
- general

Question:
{question}

Return ONLY valid JSON:

{{
    "category": "skills",
    "keywords": ["flutter", "react"]
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You classify portfolio questions into categories."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_completion_tokens=150,
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"category": "general", "keywords": []}


# ============================================================
# STEP 2 - RETRIEVE RELEVANT CONTEXT
# ============================================================

def retrieve_context(category: str) -> dict:
    if category == "skills":
        return {"skills": PORTFOLIO["skills"]}
    if category == "experience":
        return {"experience": PORTFOLIO["experience"]}
    if category == "projects":
        return {"projects": PORTFOLIO["projects"]}
    if category == "education":
        return {"education": PORTFOLIO["education"]}
    if category == "achievements":
        return {"achievements": PORTFOLIO["achievements"]}
    if category == "leadership":
        return {"leadership": PORTFOLIO["leadership"]}
    if category == "contact":
        return {"contact": CONTACT_INFO}
    return PORTFOLIO


SYSTEM_PROMPT = """
You are Avinash Wagh's portfolio assistant.

Answer questions about Avinash using ONLY the provided portfolio
information.

Rules:
- Never invent information.
- Never claim Avinash knows a technology unless it appears in the data.
- Never invent projects or experience.
- Be concise but useful.
- If the information is unavailable, clearly say that it is not
  available in the portfolio.
- If discussing a project, mention the technologies and important
  implementation details when relevant.
- For contact questions, provide the available contact links.
"""


def build_user_prompt(question: str, context: dict) -> str:
    return f"""
Portfolio information:

{json.dumps(context, indent=2)}

User question:
{question}

Answer the user's question naturally.
"""


# ============================================================
# STEP 3a - NON-STREAMING ANSWER
# ============================================================

def generate_answer(question: str, context: dict) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(question, context)},
        ],
        temperature=0.2,
        max_completion_tokens=500,
    )
    return response.choices[0].message.content


# ============================================================
# STEP 3b - STREAMING ANSWER (generator of text chunks)
# ============================================================

def generate_answer_stream(question: str, context: dict):
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(question, context)},
        ],
        temperature=0.2,
        max_completion_tokens=500,
        stream=True,
    )

    for chunk in stream:
        if not chunk.choices:
            continue
        content = chunk.choices[0].delta.content
        if content:
            # Server-Sent Events format: each message starts with "data: "
            yield f"data: {json.dumps({'content': content})}\n\n"

    yield "data: [DONE]\n\n"


# ============================================================
# ROUTES
# ============================================================

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    question = payload.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        analysis = analyze_question(question)
        category = analysis.get("category", "general")
        context = retrieve_context(category)
        answer = generate_answer(question, context)
        return ChatResponse(answer=answer, category=category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat/stream")
def chat_stream(payload: ChatRequest):
    question = payload.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    analysis = analyze_question(question)
    category = analysis.get("category", "general")
    context = retrieve_context(category)

    return StreamingResponse(
        generate_answer_stream(question, context),
        media_type="text/event-stream",
    )