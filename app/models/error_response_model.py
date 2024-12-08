from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ErrorResponseModel(BaseModel):
    """
    Represents an error response model.

    Attributes:
        http_status_code (Optional[int]): The HTTP status code of the error
            response.
        error_code (Optional[int]): The error code of the error response.
        error_description (Optional[str]): The error description of the error
         response.
        error_origin (Optional[str]): The error origin of the error response.
    """

    model_config = ConfigDict(extra="ignore")
    http_status_code: Optional[int] = Field(
        default=None,
        description="The HTTP status code of the error response.",
        examples=[400],
    )
    error_code: Optional[int] = Field(
        default=None,
        description="The error code of the error response.",
        examples=[1],
    )
    error_description: Optional[str] = Field(
        default=None,
        description="The error description of the error response.",
        examples=["The request body is invalid."],
    )
    error_origin: Optional[str] = Field(
        default=None,
        description="The error origin of the error response.",
        examples=["app/server/routes/learning_profile.py"],
    )
