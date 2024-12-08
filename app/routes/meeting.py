import os
from typing import Annotated

from fastapi import APIRouter, Body, Response, status

from app.models.database_handler import DatabaseBaseHandler
from app.models.error_response_model import ErrorResponseModel
from app.models.meeting_model import MeetingAddModel, MeetingGetModel

router = APIRouter()
database = DatabaseBaseHandler(
    database_url=os.environ["MONGODB_DATASET_URL"],
    database_name="content_db",
    database_collection_name="meetings_collection",
)


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def add_meeting(
    response: Response,
    meeting_add_model: Annotated[MeetingAddModel, Body(...)],
) -> MeetingGetModel | ErrorResponseModel:
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
            error_origin="app/routes/meeting.py",
        )
