import datetime
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class MeetingModel(BaseModel):
    title: str = Field("Placeholder")
    date: str = Field(datetime.datetime.now().isoformat())
    duration: int = Field(0)
    participants: list[str] = Field(["Placeholder"])
    transcript: str = Field("Placeholder")
    summary: str = Field("Placeholder")


class MeetingAddModel(MeetingModel):
    pass


class MeetingGetModel(MeetingModel):
    id: PyObjectId = Field(
        ...,
        alias="_id",
        description="The ID of the database entry.",
        examples=["658eb49d41d98125d5ad2b82"],
    )
