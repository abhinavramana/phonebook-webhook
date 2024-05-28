# phonebook-webhook
A system that is capable of accepting webhooks with updates to a person's name from a simulated phone book provider, which then must be capable of processing the webhooks and updating the system's internal state of understanding about the person

## To run the project
Create a virtual environment and install the dependencies
```bash
pip install -r requirements.txt
python fastapi_run.py
```
To test the project
```bash
python test.py
```

Note : Could have used docker but this is much simpler example

## Code walkthrough

**Models:**

GetNameResponse: Contains the name of the person or None if not available.
PersonAdded, PersonRemoved, PersonRenamed: Models for different types of payloads in the webhook.
PayloadType: Enum to specify the type of payload.
WebhookPayload: The main payload model which uses the union of the above payload models based on the payload_type.

**Endpoints:**

POST /accept_webhook: Accepts webhook notifications and processes them based on the payload type. It updates an in-memory data store (user_data_store) to reflect the current state of each person's name.
GET /get_name: Accepts a person's ID as a query string parameter and returns the person's most up-to-date name.
In-memory Data Store:

A simple dictionary (user_data_store) to store and manage the user data based on their UUID.


