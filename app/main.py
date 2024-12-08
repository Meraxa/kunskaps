from fastapi import FastAPI

from app.routes.meeting import router as meeting_router
from app.routes.transcribe import router as transcribe_router

app = FastAPI()

app.include_router(meeting_router, tags=["Meetings"], prefix="/meetings")
app.include_router(
    transcribe_router, tags=["Transcribe"], prefix="/transcribe"
)
