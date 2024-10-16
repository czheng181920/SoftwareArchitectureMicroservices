import sqlite3
from flask import Flask, request, jsonify
import logic as db

app = Flask(__name__)

#Mock, delete later
@app.route('/store', methods=['POST'])
def store_data():
    data = request.get_json()
    #use logic.py to store data in the database
    return f"Data stored", 200

@app.route('/store/create_meeting', methods=['POST'])
def create_meeting():
    data = request.json
    meeting_id = data.get('meeting_id')
    title = data.get('title')
    date_time = data.get('date_time')
    location = data.get('location')
    details = data.get('details')
    
    try:
        db.db_create_meeting(meeting_id, title, date_time, location, details)
        return jsonify({"message": "Meeting created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/store/all_meetings', methods=['GET'])
def get_all_meetings():
    try:
        meetings = db.db_query_all_meetings()
        return jsonify(meetings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store/meeting/<meeting_id>', methods=['GET'])
def get_meeting_by_id(meeting_id):
    try:
        meeting = db.db_query_meeting_by_id(meeting_id)
        if meeting:
            return jsonify(meeting), 200
        else:
            return jsonify({"error": "Meeting not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/store/update_meeting/<meeting_id>', methods=['PUT'])
def update_meeting(meeting_id):
    data = request.json
    title = data.get('title')
    date_time = data.get('date_time')
    location = data.get('location')
    details = data.get('details')
    # print inputs
    print(meeting_id)
    print(title)
    print(date_time)
    print(location)
    print(details)

    try:
        db.db_update_meeting(meeting_id, title, date_time, location, details)
        return jsonify({"message": "Meeting updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/store/delete_meeting/<meeting_id>', methods=['DELETE'])
def delete_meeting(meeting_id):
    try:
        db.db_delete_meeting(meeting_id)
        return jsonify({"message": "Meeting deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/store/meeting/<meeting_id>/calendars', methods=['GET'])
def list_calendars_by_meeting_id(meeting_id):
    try:
        calendars = db.db_list_calendars_by_meeting_ID(meeting_id)
        return jsonify(calendars), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/store/participants/<meeting_id>', methods=['GET'])
def list_participants_by_meeting_id(meeting_id):
    try:
        participants = db.db_list_participants_by_meeting_ID(meeting_id)
        return jsonify(participants), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/store/attachments/<meeting_id>', methods=['GET'])
def list_attachments_by_meeting_id(meeting_id):
    try:
        attachments = db.db_list_attachments_by_meeting_ID(meeting_id)
        return jsonify(attachments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store/create_calendar', methods=['POST'])
def create_calendar():
    data = request.json
    calendar_id = data.get('calendar_id')
    title = data.get('title')
    details = data.get('details')
    
    try:
        db.db_create_calendar(calendar_id, title, details)
        return jsonify({"message": "Calendar created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store/all_calendars', methods=['GET'])
def get_all_calendars():
    try:
        calendars = db.db_find_all_calendar()
        return jsonify(calendars), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/store/calendar/<calendar_id>', methods=['GET'])
def get_calendar_by_id(calendar_id):
    try:
        calendar = db.db_query_calendar_by_id(calendar_id)
        if calendar:
            return jsonify(calendar), 200
        else:
            return jsonify({"error": "Calendar not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/store/update_calendar/<calendar_id>', methods=['PUT'])
def update_calendar(calendar_id):
    data = request.json
    title = data.get('title')
    details = data.get('details')
    print(title)
    try:
        db.db_update_calendar(calendar_id, title, details)
        return jsonify({"message": "Calendar updated successfully"}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/store/delete_calendar/<calendar_id>', methods=['DELETE'])
def delete_calendar(calendar_id):
    try:
        db.db_delete_calendar(calendar_id)
        return jsonify({"message": "Calendar deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/store/associate_calendar_meeting', methods=['POST'])
def create_associated_calendar_meeting():
    data = request.json
    meeting_id = data.get('meeting_id')
    calendar_id = data.get('calendar_id')

    try:
        db.db_create_associated_calendar_meeting(meeting_id, calendar_id)
        return jsonify({"message": "Meeting associated with calendar successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/store/delete_meeting_calendar', methods=['DELETE'])
def delete_meeting_calendar():
    data = request.json
    calendar_id = data.get('calendar_id')
    meeting_id = data.get('meeting_id')

    try:
        db.db_delete_meeting_calendar(calendar_id, meeting_id)
        return jsonify({"message": f"Meeting {meeting_id} deleted from Calendar {calendar_id} successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/store/calendar_meetings/<calendar_id>', methods=['GET'])
def list_meetings_in_calendar(calendar_id):
    try:
        meetings = db.db_calendar_list_meeting(calendar_id)
        return jsonify(meetings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store/create_participant', methods=['POST'])
def create_participant():
    data = request.json
    participant_id = data.get('participant_id')
    meeting_id = data.get('meeting_id')
    name = data.get('name')
    email = data.get('email')

    try:
        db.db_create_participant(participant_id, meeting_id, name, email)
        return jsonify({"message": "Participant created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store/participants', methods=['GET'])
def get_all_participants():
    try:
        participants = db.db_query_all_participants()
        return jsonify(participants), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store/participant/<participant_id>', methods=['GET'])
def get_participant_by_id(participant_id):
    try:
        participant = db.db_query_participant_by_id(participant_id)
        if participant:
            return jsonify(participant), 200
        else:
            return jsonify({"error": "Participant not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/store/update_participant/<participant_id>', methods=['PUT'])
def update_participant(participant_id):
    data = request.json
    name = data.get('name')
    email = data.get('email')

    try:
        db.db_update_participant(participant_id, name, email)
        return jsonify({"message": "Participant updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store/delete_participant/<participant_id>', methods=['DELETE'])
def delete_participant(participant_id):
    try:
        db.db_delete_participant(participant_id)
        return jsonify({"message": "Participant deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def execute_db_function(db_function, *args):
    try:
        db_function(*args)
        return jsonify({"message": "Success"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

@app.route('/store/attachments/<int:attachment_id>', methods=['DELETE'])
def delete_attachment(attachment_id):
    return execute_db_function(db.db_delete_attachment, attachment_id)

@app.route('/store/meetings/<int:meeting_id>/calendars', methods=['GET'])
def list_calendars_for_meeting(meeting_id):
    try:
        calendars = db.db_meeting_list_calendar(meeting_id)
        return jsonify({"calendars": calendars}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

@app.route('/store/meetings/<int:meeting_id>/participants', methods=['GET'])
def list_participants_for_meeting(meeting_id):
    try:
        participants = db.db_participant_list_calendar(meeting_id)
        return jsonify({"participants": participants}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

@app.route('/store/meetings/<int:meeting_id>/attachments', methods=['GET'])
def list_attachments_for_meeting(meeting_id):
    try:
        attachments = db.db_attachment_list_calendar(meeting_id)
        return jsonify({"attachments": attachments}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

@app.route('/store/calendars/<int:calendar_id>/meetings', methods=['GET'])
def list_meetings_for_calendar(calendar_id):
    try:
        meetings = db.db_calendar_list_meeting(calendar_id)
        return jsonify({"meetings": meetings}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500
#TODO: add endpoints for attatchments 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
