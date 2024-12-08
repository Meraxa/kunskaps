import os
from typing import Annotated

import whisper
from fastapi import APIRouter, File, Response, UploadFile, status

from app.models.database_handler import DatabaseBaseHandler
from app.models.error_response_model import ErrorResponseModel
from app.models.meeting_model import MeetingAddModel, MeetingGetModel

router = APIRouter()
database = DatabaseBaseHandler(
    database_url=os.environ["MONGODB_DATASET_URL"],
    database_name="content_db",
    database_collection_name="meetings_collection",
)

# Load the Whisper model
model = whisper.load_model("base")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def transcribe_audio(
    response: Response,
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
) -> MeetingGetModel | ErrorResponseModel:
    # Save the uploaded file to the server
    filepath = os.path.join("uploads", file.filename)
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    # Transcribe the audio file using Whisper
    result = model.transcribe(filepath)

    meeting_add_model = MeetingAddModel(transcript=result["text"])

    # Add the meeting to the database
    database_response = await database.add_entry_to_database(
        model=meeting_add_model
    )
    if database_response is not None:
        vocabulary_response = MeetingGetModel(**database_response)
        return vocabulary_response
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseModel(
            http_status_code=status.HTTP_400_BAD_REQUEST,
            error_code=0,
            error_description="TODO.",
            error_origin="app/routes/transcribe.py",
        )
