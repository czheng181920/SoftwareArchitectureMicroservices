from flask import Flask, request, jsonify
import requests
import uuid
import re

app = Flask(__name__)

# data layer server IP address and port
# TODO: test this with the actual IP address
DATA_LAYER_URL = 'http://172.20.96.214:5002/store'

# mock, delete later TODO
@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    # result = send_to_data_layer(data)
    return f"Processed data: {data}", 200

def generate_uuid():
    return str(uuid.uuid4())

def is_valid_email(email):
    # Simple regex for validating an email
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None


# Meeting Management
@app.route('/meeting', methods=['POST'])
def create_meeting():
    data = request.get_json()
    meeting_id = data.get('meeting_id', generate_uuid())
    title = data.get('title')
    date_time = data.get('date_time')
    location = data.get('location')
    details = data.get('details')

    # Send the request to the data layer
    response = requests.post(f"{DATA_LAYER_URL}/create_meeting", json={
        "meeting_id": meeting_id,
        "title": title,
        "date_time": date_time,
        "location": location,
        "details": details
    })

    return jsonify(response.json()), response.status_code

@app.route('/meetings', methods=['GET'])
def query_all_meetings():
    response = requests.get(f"{DATA_LAYER_URL}/all_meetings")
    return jsonify(response.json()), response.status_code

@app.route('/meeting/<meeting_id>', methods=['GET'])
def query_meeting_by_id(meeting_id):
    response = requests.get(f"{DATA_LAYER_URL}/meeting/{meeting_id}")
    return jsonify(response.json()), response.status_code

@app.route('/meeting/<meeting_id>', methods=['PUT'])
def update_meeting(meeting_id):
    data = request.get_json()
    title = data.get('title')
    date_time = data.get('date_time')
    location = data.get('location')
    details = data.get('details')

    response = requests.put(f"{DATA_LAYER_URL}/update_meeting/{meeting_id}", json={
        "title": title,
        "date_time": date_time,
        "location": location,
        "details": details
    })
    return jsonify(response.json()), response.status_code

@app.route('/meeting/<meeting_id>', methods=['DELETE'])
def delete_meeting(meeting_id):
    response = requests.delete(f"{DATA_LAYER_URL}/delete_meeting/{meeting_id}")
    return jsonify(response.json()), response.status_code

# List Calendars, Participants, and Attachments by Meeting ID
@app.route('/meeting/<meeting_id>/calendars', methods=['GET'])
def list_calendar_by_meeting_id(meeting_id):
    response = requests.get(f"{DATA_LAYER_URL}/meeting/{meeting_id}/calendars")
    return jsonify(response.json()), response.status_code

@app.route('/meeting/<meeting_id>/participants', methods=['GET'])
def list_participants_by_meeting_id(meeting_id):
    response = requests.get(f"{DATA_LAYER_URL}/meeting/{meeting_id}/participants")
    return jsonify(response.json()), response.status_code

@app.route('/meeting/<meeting_id>/attachments', methods=['GET'])
def list_attachments_by_meeting_id(meeting_id):
    response = requests.get(f"{DATA_LAYER_URL}/meeting/{meeting_id}/attachments")
    return jsonify(response.json()), response.status_code

#Calendar stuff
@app.route('/calendar', methods=['POST'])
def create_calendar():
    # Inputs from API request
    data = request.get_json()
    calendar_id = data.get('calendar_id')
    if not calendar_id:
        calendar_id = generate_uuid()
    title = data.get('title')
    details = data.get('details')

    # Send request to the data layer
    response = requests.post(f"{DATA_LAYER_URL}/create_calendar", json={
        "calendar_id": calendar_id,
        "title": title,
        "details": details
    })

    return jsonify(response.json()), response.status_code

@app.route('/calendars', methods=['GET'])
def query_all_calendars():
    # Send request to the data layer
    response = requests.get(f"{DATA_LAYER_URL}/all_calendars")
    return jsonify(response.json()), response.status_code

@app.route('/calendar/<calendar_id>', methods=['GET'])
def query_calendar_by_id(calendar_id):
    # Send request to the data layer
    response = requests.get(f"{DATA_LAYER_URL}/calendar/{calendar_id}")
    return jsonify(response.json()), response.status_code

@app.route('/calendar/<calendar_id>', methods=['PUT'])
def update_calendar(calendar_id):
    # Inputs from API request
    data = request.get_json()
    title = data.get('calendar_title')
    print('business layer: ', data)
    details = data.get('calendar_details')

    # Send request to the data layer
    response = requests.put(f"{DATA_LAYER_URL}/update_calendar/{calendar_id}", json={
        "title": title,
        "details": details
    })

    return jsonify(response.json()), response.status_code

@app.route('/calendar/<calendar_id>', methods=['DELETE'])
def delete_calendar(calendar_id):
    # Send request to the data layer
    response = requests.delete(f"{DATA_LAYER_URL}/delete_calendar/{calendar_id}")
    return jsonify(response.json()), response.status_code

@app.route('/calendar/<calendar_id>/meetings', methods=['GET'])
def see_meetings_in_calendar(calendar_id):
    # Send request to the data layer
    response = requests.get(f"{DATA_LAYER_URL}/calendar/{calendar_id}/meetings")
    return jsonify(response.json()), response.status_code

# Business layer route for associating a meeting with a calendar
@app.route('/calendar/addMeeting', methods=['POST'])
def add_meeting_to_calendar():
    data = request.get_json()
    meeting_id = data.get('meeting_id')
    calendar_id = data.get('calendar_id')

    if not meeting_id or not calendar_id:
        return jsonify({"error": "Meeting ID and Calendar ID are required"}), 400

    try:
        # Forward the request to the data layer
        response = requests.post(f'{DATA_LAYER_URL}/store/associate_calendar_meeting', json={
            'meeting_id': meeting_id,
            'calendar_id': calendar_id
        })

        # Return the response from the data layer
        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Participant Management
@app.route('/participant', methods=['POST'])
def create_participant():
    data = request.get_json()
    meeting_id = data.get('meeting_id')

    # Validate meeting ID by querying the data layer
    response = requests.get(f"{DATA_LAYER_URL}/check_meeting/{meeting_id}")
    if response.status_code != 200 or not response.json().get('valid'):
        return jsonify({"error": "Invalid meeting ID"}), 400

    name = data.get('name')
    email = data.get('email')
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email"}), 400
    
    participant_id = data.get('participant_id', generate_uuid())

    # Send request to data layer
    response = requests.post(f"{DATA_LAYER_URL}/create_participant", json={
        "participant_id": participant_id,
        "meeting_id": meeting_id,
        "name": name,
        "email": email
    })

    return jsonify(response.json()), response.status_code

@app.route('/participants', methods=['GET'])
def query_all_participants():
    response = requests.get(f"{DATA_LAYER_URL}/all_participants")
    return jsonify(response.json()), response.status_code

@app.route('/participant/<participant_id>', methods=['GET'])
def query_participant_by_id(participant_id):
    response = requests.get(f"{DATA_LAYER_URL}/participant/{participant_id}")
    return jsonify(response.json()), response.status_code

@app.route('/participant/<participant_id>', methods=['PUT'])
def update_participant(participant_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email"}), 400

    response = requests.put(f"{DATA_LAYER_URL}/update_participant/{participant_id}", json={
        "name": name,
        "email": email
    })
    return jsonify(response.json()), response.status_code

@app.route('/participant/<participant_id>', methods=['DELETE'])
def delete_participant(participant_id):
    response = requests.delete(f"{DATA_LAYER_URL}/delete_participant/{participant_id}")
    return jsonify(response.json()), response.status_code

# Attachment Management
@app.route('/attachment', methods=['POST'])
def create_attachment():
    data = request.get_json()
    meeting_id = data.get('meeting_id')

    # Validate meeting ID
    response = requests.get(f"{DATA_LAYER_URL}/check_meeting/{meeting_id}")
    if response.status_code != 200 or not response.json().get('valid'):
        return jsonify({"error": "Invalid meeting ID"}), 400
    
    url = data.get('url')
    attachment_id = data.get('attachment_id', generate_uuid())

    # Send request to data layer
    response = requests.post(f"{DATA_LAYER_URL}/create_attachment", json={
        "attachment_id": attachment_id,
        "meeting_id": meeting_id,
        "url": url
    })

    return jsonify(response.json()), response.status_code

@app.route('/attachments', methods=['GET'])
def query_all_attachments():
    response = requests.get(f"{DATA_LAYER_URL}/all_attachments")
    return jsonify(response.json()), response.status_code

@app.route('/attachment/<attachment_id>', methods=['GET'])
def query_attachment_by_id(attachment_id):
    response = requests.get(f"{DATA_LAYER_URL}/attachment/{attachment_id}")
    return jsonify(response.json()), response.status_code

@app.route('/attachment/<attachment_id>', methods=['PUT'])
def update_attachment(attachment_id):
    data = request.get_json()
    url = data.get('url')

    response = requests.put(f"{DATA_LAYER_URL}/update_attachment/{attachment_id}", json={
        "url": url
    })
    return jsonify(response.json()), response.status_code

@app.route('/attachment/<attachment_id>', methods=['DELETE'])
def delete_attachment(attachment_id):
    response = requests.delete(f"{DATA_LAYER_URL}/delete_attachment/{attachment_id}")
    return jsonify(response.json()), response.status_code

# Calendar-Meeting Management
@app.route('/calendar/<calendar_id>/meeting/<meeting_id>', methods=['DELETE'])
def delete_meeting_calendar(calendar_id, meeting_id):
    response = requests.delete(f"{DATA_LAYER_URL}/calendar/{calendar_id}/meeting/{meeting_id}")
    return jsonify(response.json()), response.status_code

@app.route('/calendar/<calendar_id>/meeting/<meeting_id>', methods=['POST'])
def add_meeting_calendar(calendar_id, meeting_id):
    response = requests.post(f"{DATA_LAYER_URL}/calendar/{calendar_id}/meeting/{meeting_id}")
    return jsonify(response.json()), response.status_code

# List Queries
@app.route('/meeting/<meeting_id>/calendars', methods=['GET'])
def list_of_calendars_meeting(meeting_id):
    response = requests.get(f"{DATA_LAYER_URL}/meeting/{meeting_id}/calendars")
    return jsonify(response.json()), response.status_code

@app.route('/meeting/<meeting_id>/participants', methods=['GET'])
def list_of_participants_meeting(meeting_id):
    response = requests.get(f"{DATA_LAYER_URL}/meeting/{meeting_id}/participants")
    return jsonify(response.json()), response.status_code

@app.route('/meeting/<meeting_id>/attachments', methods=['GET'])
def list_of_attachments_meeting(meeting_id):
    response = requests.get(f"{DATA_LAYER_URL}/meeting/{meeting_id}/attachments")
    return jsonify(response.json()), response.status_code

@app.route('/calendar/<calendar_id>/meetings', methods=['GET'])
def list_of_meetings_calendar(calendar_id):
    response = requests.get(f"{DATA_LAYER_URL}/calendar/{calendar_id}/meetings")
    return jsonify(response.json()), response.status_code

def send_to_data_layer(data):
    url = 'http://<Data_Layer_IP>:5002/store'
    response = requests.post(url, json=data)
    return response.text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)