from typing import List, Literal, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
import uvicorn

# LangChain + Ollama
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables import Runnable

# --- Config ---
MODEL_NAME = "gemma3:270m"  # or deepseek-r1:1.5b

app = FastAPI(title="Local LLM (FastAPI + LangChain + Ollama)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# --- Schemas ---
class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.2
    top_p: Optional[float] = 0.9

class ChatResponse(BaseModel):
    content: str

# --- Build the model/chain ---
def build_chain(temperature: float = 0.2, top_p: float = 0.9) -> Runnable:
    llm = ChatOllama(
        model=MODEL_NAME,
        temperature=temperature,
        top_p=top_p,
        # you can also pass: base_url="http://127.0.0.1:11434"
    )
    return llm  # already a Runnable in LangChain

def to_lc_messages(msgs: List[ChatMessage]):
    out = []
    for m in msgs:
        if m.role == "system":
            out.append(SystemMessage(m.content))
        elif m.role == "user":
            out.append(HumanMessage(m.content))
        else:
            out.append(AIMessage(m.content))
    return out

# --- Endpoints ---
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        chain = build_chain(req.temperature, req.top_p)
        lc_msgs = to_lc_messages(req.messages)
        result = chain.invoke(lc_msgs)
        # result can be a BaseMessage — unify to string
        content = getattr(result, "content", str(result))
        return ChatResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    chain = build_chain(req.temperature, req.top_p)
    lc_msgs = to_lc_messages(req.messages)

    def event_gen():
        try:
            for chunk in chain.stream(lc_msgs):
                # chunk is a BaseMessageChunk; get text safely
                text = getattr(chunk, "content", "")
                if text:
                    yield {"event": "token", "data": text}
            yield {"event": "done", "data": "[DONE]"}
        except Exception as e:
            yield {"event": "error", "data": str(e)}
    return EventSourceResponse(event_gen())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)