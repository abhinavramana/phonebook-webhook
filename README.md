# phonebook-webhook
A system that is capable of accepting webhooks with updates to a person's name from a simulated phone book provider, which then must be capable of processing the webhooks and updating the system's internal state of understanding about the person

## To run the project
Create a virtual environment and install the dependencies
```bash
python -m venv tutorial-env
source tutorial-env/bin/activate
```
**Running backend**
```bash
pip install -r requirements.txt
python run_fastapi_backend.py
```
**To test the project**
```bash
python test.py
```
**Running frontend**
```bash
python run_flask_frontend.py
```
Note : Could have used docker but this is much simpler example

## Code walkthrough

**Models:**

`GetNameResponse`: Contains the name of the person or None if not available.
`PersonAdded, PersonRemoved, PersonRenamed`: Models for different types of payloads in the webhook.
`PayloadType`: Enum to specify the type of payload.
`WebhookPayload`: The main payload model which uses the union of the above payload models based on the payload_type.

**Endpoints:**

`POST /accept_webhook:` Accepts webhook notifications and processes them based on the payload type. It updates an in-memory data store (user_data_store) to reflect the current state of each person's name.

`GET /get_name:` Accepts a person's ID as a query string parameter and returns the person's most up-to-date name.


**Flask Application:**

The Flask application serves the frontend and handles user queries.
The handle_query function processes natural language queries and determines the appropriate FastAPI endpoint to call.
Functions get_current_name and get_name_history send requests to the FastAPI backend and return formatted responses.

**HTML Template:**

A simple form to input queries.
The form submission is handled via jQuery to make an AJAX POST request to the Flask server.
The response is displayed in a segment below the form.

