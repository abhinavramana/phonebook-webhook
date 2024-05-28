from flask import Flask, request, render_template, jsonify
import requests

from network_models import PUBLIC_ACCESSIBLE_LOCALHOST

app = Flask(__name__)

FASTAPI_URL = "http://localhost:8110"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/query', methods=['POST'])
def query():
    user_query = request.form['query']
    response = handle_query(user_query)
    return jsonify(response)


def handle_query(query):
    if "current name of person ID" in query:
        person_id = query.split("current name of person ID:")[-1].strip()
        return get_current_name(person_id)
    elif "all the previous names of person ID" in query:
        person_id = query.split("all the previous names of person ID:")[-1].strip()
        return get_name_history(person_id)
    elif "get all persons" in query.lower():
        return get_all_persons()
    else:
        return {"message": "Invalid query. Please ask about the current name, previous names, or get all persons."}


def get_current_name(person_id):
    url = f"{FASTAPI_URL}/get_name"
    params = {'person_id': person_id}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {"message": f"The current name of person ID {person_id} is {data['name']}."}
    else:
        return {"message": f"Failed to fetch current name: {response.status_code}, {response.text}"}


def get_name_history(person_id):
    url = f"{FASTAPI_URL}/get_name_history"
    params = {'person_id': person_id}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        history = "\n".join([f"{entry[0]} (at {entry[1]})" for entry in data])
        return {"message": f"The previous names of person ID {person_id} are:\n{history}"}
    else:
        return {"message": f"Failed to fetch name history: {response.status_code}, {response.text}"}


def get_all_persons():
    url = f"{FASTAPI_URL}/get_all_persons"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {"persons": data}
    else:
        return {"message": f"Failed to fetch all persons: {response.status_code}, {response.text}"}


if __name__ == "__main__":
    app.run(debug=True, port=8112, host=PUBLIC_ACCESSIBLE_LOCALHOST)
