from uuid import UUID

from fastapi import HTTPException

from db_operations import add_person, rename_person, remove_person, get_current_name, get_name_history
from network_models import WebhookPayload, PayloadType, PersonAdded, PersonRenamed, PersonRemoved, GetNameResponse

# In-memory data store
user_data_store = {}


def accept_person_updates(payload: WebhookPayload):
    try:
        content = payload.payload_content
        timestamp = content.timestamp.isoformat() + 'Z'

        if payload.payload_type == PayloadType.person_added:
            add_person(str(content.person_id), content.name, timestamp)
        elif payload.payload_type == PayloadType.person_renamed:
            rename_person(str(content.person_id), content.name, timestamp)
        elif payload.payload_type == PayloadType.person_removed:
            remove_person(str(content.person_id), timestamp)
        else:
            raise HTTPException(status_code=400, detail="Invalid payload type")
        return {"message": "Webhook processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_name(person_id: UUID):
    try:
        name = get_current_name(str(person_id))
        return GetNameResponse(name=name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_name_history(person_id: UUID):
    try:
        history = get_name_history(str(person_id))
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
