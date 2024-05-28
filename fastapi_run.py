from uuid import UUID

from fastapi import FastAPI, Query

from db_operations import init_db
from network_models import WebhookPayload, GetNameResponse
from phonebook_service import accept_person_updates, retrieve_name, retrieve_name_history

print("Initialize DB before the app starts...")
init_db()
print("Initialize the app...")
app = FastAPI()


# Endpoint to accept webhook notifications
@app.post("/accept_webhook")
async def accept_webhook(payload: WebhookPayload):
    return accept_person_updates(payload)


# Endpoint to fetch the current name of a user
@app.get("/get_name", response_model=GetNameResponse)
async def get_name(person_id: UUID = Query(..., format="uuid")):
    return retrieve_name(person_id)


# Endpoint to fetch the name history of a user
@app.get("/get_name_history")
async def get_name_history(person_id: UUID = Query(..., format="uuid")):
    return retrieve_name_history(person_id)

# Run the application (only for testing purposes, remove if using in production)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
