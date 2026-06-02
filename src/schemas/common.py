"""
Common Response Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):

    success: bool = True

    message: str


class ErrorResponse(BaseModel):

    success: bool = False

    error: str


class TimestampMixin(BaseModel):

    created_at: Optional[datetime] = None