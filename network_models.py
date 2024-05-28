from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Union, Optional
from uuid import UUID


class GetNameResponse(BaseModel):
    name: Optional[str] = None


class PersonAdded(BaseModel):
    person_id: UUID
    name: str
    timestamp: datetime


class PersonRemoved(BaseModel):
    person_id: UUID
    timestamp: datetime


class PersonRenamed(BaseModel):
    person_id: UUID
    name: str
    timestamp: datetime


class PayloadType(str, Enum):
    person_added = "PersonAdded"
    person_renamed = "PersonRenamed"
    person_removed = "PersonRemoved"


class WebhookPayload(BaseModel):
    payload_type: PayloadType
    payload_content: Union[PersonAdded, PersonRenamed, PersonRemoved]


class Person(BaseModel):
    person_id: str
    current_name: str