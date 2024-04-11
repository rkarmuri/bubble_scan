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

            # Store file information
            file_id = os.urandom(16).hex()  # Generate unique identifier
            file_info[file_id] = {
                'filename': filename,
                'path': file_path,
                'processed': False  # Flag to track if CSV is generated
            }

            # Send PDF file to mock AI for processing
            mock_ai_url = 'http://localhost:5002/mock_ai'
            files = {'file': open(file_path, 'rb')}
            response = requests.post(mock_ai_url, files=files)

            # Clean up: remove uploaded PDF
            # os.remove(file_path)

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
    if json_data:
        print("Received JSON data:", json_data)
        csv_data = transform_json_to_csv(json_data)
        if csv_data:
            csv_filename = f'output_{str(uuid.uuid4())}.csv'  # Generate a unique CSV filename
            csv_file_path = os.path.join(uploads_dir, csv_filename)
            print("CSV data before writing to file:", csv_data)  # Print CSV data before writing to file
            try:
                with open(csv_file_path, 'w', newline='') as csv_file:
                    csv_file.write(csv_data)
                print("CSV data successfully written to file.")  # Log success message
                return jsonify({"status": "success", "message": "JSON converted to CSV successfully", "csv_filename": csv_filename})
            except Exception as e:
                print("Error writing CSV data to file:", e)  # Log error message if writing fails
                return jsonify({"status": "error", "message": f"Error writing CSV data to file: {e}"})
        else:
            return jsonify({"status": "error", "message": "Error converting JSON to CSV"})
    else:
        return jsonify({"status": "error", "message": "No or invalid JSON data received"})

def transform_json_to_csv(json_data):
    csv_data = ''
    if isinstance(json_data, dict):  # Check if json_data is a dictionary
        if 'students' in json_data:  # Check if 'students' key is present in the dictionary
            students = json_data['students']
            if students and isinstance(students, list):  # Check if 'students' value is a non-empty list
                if 'answers' in students[0]:  # Check if 'answers' key is present in the first student dictionary
                    keys = students[0]['answers'].keys()
                    csv_data += ','.join(['studentID'] + list(keys)) + '\n'
                    for student in students:
                        csv_data += ','.join([student['studentID']] + [student['answers'].get(key, '') for key in keys]) + '\n'

                    # Log CSV data
                    print("CSV data after transformation:\n", csv_data)
                    return csv_data

    # If the JSON data structure doesn't match the expected format, print the JSON data
    print("Received JSON data does not match the expected format:", json_data)
    return None

# Logic to generate CSV file and update 'processed' flag
@app.route('/api/process_pdf', methods=['POST'])
def process_pdf():
    file_id = request.json.get('file_id')
    if file_id not in file_info:
        return jsonify({"status": "error", "message": "Invalid file ID"})

    # Logic to generate CSV file
    # Once CSV is generated, update 'processed' flag
    file_info[file_id]['processed'] = True

    return jsonify({"status": "success", "message": "PDF processed successfully"})

@app.route('/api/download_csv/<file_id>', methods=['GET'])
def download_csv(file_id):
    try:
        if file_id not in file_info:
            return jsonify({"status": "error", "message": "File not found"})

        file_data = file_info[file_id]
        if not file_data['processed']:
            return jsonify({"status": "error", "message": "CSV not generated yet"})

        file_path = file_data['path']
        if os.path.exists(file_path):
            return send_from_directory(uploads_dir, file_data['filename'], as_attachment=True)
        else:
            return jsonify({"status": "error", "message": "File not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error downloading CSV: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
