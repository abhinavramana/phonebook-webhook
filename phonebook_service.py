from uuid import UUID

from fastapi import HTTPException

from network_models import WebhookPayload, PayloadType, PersonAdded, PersonRenamed, PersonRemoved, GetNameResponse

# In-memory data store
user_data_store = {}


def accept_person_updates(payload: WebhookPayload):
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


def retrieve_name(person_id: UUID):
    try:
        name = user_data_store.get(person_id)
        if name is not None:
            return GetNameResponse(name=name)
        else:
            return GetNameResponse(name=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))