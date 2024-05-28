from datetime import datetime
from enum import Enum
from typing import Union, Optional
from uuid import UUID

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

# In-memory data store
user_data_store = {}

# Pydantic models

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


# Endpoint to accept webhook notifications
@app.post("/accept_webhook")
async def accept_webhook(payload: WebhookPayload):
    try:
        if payload.payload_type == PayloadType.person_added:
            content: PersonAdded = payload.payload_content
            user_data_store[content.person_id] = content.name
        elif payload.payload_type == PayloadType.person_renamed:
            content: PersonRenamed = payload.payload_content
            if content.person_id in user_data_store:
                user_data_store[content.person_id] = content.name
            else:
                raise HTTPException(status_code=400, detail="User not found")
        elif payload.payload_type == PayloadType.person_removed:
            content: PersonRemoved = payload.payload_content
            if content.person_id in user_data_store:
                del user_data_store[content.person_id]
            else:
                raise HTTPException(status_code=400, detail="User not found")
        else:
            raise HTTPException(status_code=400, detail="Invalid payload type")
        return {"message": "Webhook processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to fetch the current name of a user
@app.get("/get_name", response_model=GetNameResponse)
async def get_name(person_id: UUID = Query(..., format="uuid")):
    try:
        name = user_data_store.get(person_id)
        if name is not None:
            return GetNameResponse(name=name)
        else:
            return GetNameResponse(name=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run the application (only for testing purposes, remove if using in production)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
