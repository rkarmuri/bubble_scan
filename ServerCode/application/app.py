from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
from werkzeug.utils import secure_filename
import requests
import csv
import uuid

app = Flask(__name__)
CORS(app)

# Ensure uploads directory exists
uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

logging.basicConfig(level=logging.DEBUG)
file_info = {}
csv_files = {}

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

@app.route('/api/message', methods=['POST'])
def receive_message():
    message_data = request.json
    message = message_data.get('message', '')
    print(f"Received message: {message}")
    return jsonify({"status": "success", "message": "Message received successfully!"})

@app.route('/api/upload', methods=['POST'])
def file_upload():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part in the request"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"})

    if file and file.filename.lower().endswith('.pdf'):
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(uploads_dir, filename)
            file.save(file_path)

            # Store file information and use a Flag to track if CSV is generated
            file_id = os.urandom(16).hex()
            file_info[file_id] = {
                'filename': filename,
                'path': file_path,
                'processed': False  
            }

            # Send PDF file to mock AI for processing
            mock_ai_url = 'http://localhost:5002/mock_ai'
            files = {'file': open(file_path, 'rb')}
            data = {'file_id': file_id}
            response = requests.post(mock_ai_url, files=files, data=data)

            # os.remove(file_path) 
            # print("The File ID generated on Flask: ", file_id)
            if response.status_code == 200:
                return jsonify({"status": "success", "message": "PDF processed successfully", "file_id": file_id})
            else:
                return jsonify({"status": "error", "message": f"Failed to process PDF: HTTP {response.status_code}"})

        except Exception as e:
            return jsonify({"status": "error", "message": f"Error processing PDF: {e}"})

    else:
        return jsonify({"status": "error", "message": "Only PDF files are allowed"})

@app.route('/json', methods=['POST'])
def json_to_csv():
    json_data = request.json
    file_id = json_data.get('file_id')
    #print("The file id is:",file_id)
    if json_data:
        #print("Received the JSON data from the AI component successfully")
        csv_data = transform_json_to_csv(json_data)
        if csv_data:
            csv_filename = f'output_{file_id}.csv'
            csv_file_path = os.path.join(uploads_dir, csv_filename)
            try:
                with open(csv_file_path, 'w', newline='') as csv_file:
                    csv_file.write(csv_data)
                #print("CSV data successfully written to file.")  # Log success message
                #print("CSV filename:", csv_filename)  # Log the CSV filename
                csv_files[file_id] = {
                    'filename': csv_filename,
                    'path': csv_file_path
                }
                return jsonify({"status": "success", "message": "JSON converted to CSV successfully", "csv_filename": csv_filename,"file_id": file_id})
            except Exception as e:
                print("Error writing CSV data to file:", e)  # Log error message if writing fails
                return jsonify({"status": "error", "message": f"Error writing CSV data to file: {e}"})
        else:
            return jsonify({"status": "error", "message": "Error converting JSON to CSV"})
    else:
        return jsonify({"status": "error", "message": "No or invalid JSON data received"})

def transform_json_to_csv(json_data):
    csv_data = ''
    if isinstance(json_data, dict):
        if 'students' in json_data:
            students = json_data['students']
            if students and isinstance(students, list):
                if 'answers' in students[0]:
                    keys = students[0]['answers'].keys()
                    csv_data += ','.join(['studentID'] + list(keys)) + '\n'
                    for student in students:
                        csv_data += ','.join([student['studentID']] + [student['answers'].get(key, '') for key in keys]) + '\n'

                    return csv_data

    # If the JSON data structure doesn't match the expected format, print the JSON data
    print("Received JSON data does not match the expected format:", json_data)
    return None

@app.route('/api/process_pdf', methods=['POST'])
def process_pdf():
    file_id = request.json.get('file_id')
    if file_id not in file_info:
        return jsonify({"status": "error", "message": "Invalid file ID"})

    # Once CSV is generated, update 'processed' flag
    file_info[file_id]['processed'] = True

    return jsonify({"status": "success", "message": "PDF processed successfully"})

@app.route('/api/download_csv/<file_id>', methods=['GET'])
def download_csv(file_id):
    try:
        if file_id not in csv_files:
            return jsonify({"status": "error", "message": "CSV file not found"})

        csv_file_data = csv_files[file_id]
        file_path = csv_file_data['path']
        
        if os.path.exists(file_path):
            return send_from_directory(uploads_dir, os.path.basename(file_path), as_attachment=True)
        else:
            return jsonify({"status": "error", "message": "CSV file not found"})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error downloading CSV: {e}"}), 500

@app.route('/api/csv_acknowledgment/<file_id>', methods=['POST'])
def csv_acknowledgment(file_id):
    if file_id in file_info:
        file_info[file_id]['csv_sent'] = True
        return jsonify({"status": "success", "message": "CSV is sent to the React successfully"})
    else:
        return jsonify({"status": "error", "message": "File ID not found"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
