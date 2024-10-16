from flask import Flask, request, jsonify
import attachmentsLogic as db

app = Flask(__name__)

#TODO: add endpoints for attachments 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)

@app.route('/store/create_attachment', methods=['POST'])
def create_attachment():
    data = request.json
    attachment_id = data.get('attachment_id')
    meeting_id = data.get('meeting_id')
    url = data.get('url')

    try:
        db.db_create_attachment(attachment_id, meeting_id, url)
        return jsonify({"message": "Attachment created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



#do for the rest!!!!!
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





