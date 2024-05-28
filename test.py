import random
import uuid
from datetime import datetime
import requests


class PhonebookDummyDataGenerator:
    def __init__(self):
        self.person_ids = []

    def generate_webhook(self):
        while True:
            payload_type = random.choice(
                ['PersonAdded', 'PersonRenamed', 'PersonAdded', 'PersonRenamed', 'PersonRemoved'])
            timestamp = datetime.utcnow().isoformat() + 'Z'

            if payload_type == 'PersonAdded':
                person_id = str(uuid.uuid4())
                self.person_ids.append(person_id)
                name = f"Person {random.randint(100, 999)}"
                payload_content = {
                    "person_id": person_id,
                    "name": name,
                    "timestamp": timestamp
                }

            elif payload_type == 'PersonRenamed':
                if self.person_ids:
                    person_id = random.choice(self.person_ids)
                    name = f"Renamed Person {random.randint(1000, 9999)}"
                    payload_content = {
                        "person_id": person_id,
                        "name": name,
                        "timestamp": timestamp
                    }
                else:
                    continue

            elif payload_type == 'PersonRemoved':
                if self.person_ids:
                    person_id = random.choice(self.person_ids)
                    self.person_ids.remove(person_id)
                    payload_content = {
                        "person_id": person_id,
                        "timestamp": timestamp
                    }
                else:
                    continue

            yield {
                "payload_type": payload_type,
                "payload_content": payload_content
            }


# Function to send payload to the FastAPI endpoint
def send_payload_to_fastapi(payload):
    url = "http://localhost:8000/accept_webhook"
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Payload processed successfully")
    else:
        print(f"Failed to process payload: {response.status_code}, {response.text}")


# Example usage:
generator = PhonebookDummyDataGenerator()
webhook_generator = generator.generate_webhook()

# Send 5 sample webhook payloads to the FastAPI server
for _ in range(5):
    payload = next(webhook_generator)
    print(payload)
    send_payload_to_fastapi(payload)
    print("-" * 60)
