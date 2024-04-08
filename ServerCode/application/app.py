from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import csv
import json
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter

def create_app(config_name=None):
    app = Flask(__name__)
    CORS(app)

    # Ensure uploads directory exists
    uploads_dir = os.path.join(app.instance_path, 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)

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
        print('Content in request files', request.files)  
        print('content in request form', request.form)
        
        if 'file' not in request.files:
            print("Error: No file part in the request.")
            return jsonify({"status": "error", "message": "No file part in the request"})
        
        file = request.files['file']
        
        if file.filename == '':
            print("Error: No selected file.")
            return jsonify({"status": "error", "message": "No selected file"})
        
        if file and file.filename.lower().endswith('.pdf'):
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(uploads_dir, filename)
                file.save(file_path)  # Save the file temporarily to read its content
                
                # Use simulate_ai_data_extraction if you're simulating data extraction
                # Otherwise, use the below code to process actual PDF data
                students_answers = simulate_ai_data_extraction(file_path)
                
                json_filename = filename.rsplit('.', 1)[0] + '_test_data.json'
                json_filepath = os.path.join(uploads_dir, json_filename)
                with open(json_filepath, 'w') as json_file:
                    json.dump(students_answers, json_file, indent=4)

                os.remove(file_path)
                return jsonify({"status": "success", "message": f"PDF processed and test data combined into JSON: {json_filename}"})
            except Exception as e:
                print(f"Error processing PDF: {e}")
                return jsonify({"status": "error", "message": "Error processing PDF"})

        elif file and file.filename.lower().endswith('.json'):
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(uploads_dir, filename)
                file.save(file_path)  # Save the file temporarily to read its content
                
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                
                csv_filename = filename.rsplit('.', 1)[0] + '.csv'
                csv_filepath = os.path.join(uploads_dir, csv_filename)
                
                with open(csv_filepath, 'w', newline='') as csv_file:
                    if 'students' in data and isinstance(data['students'], list):
                        students_data = data['students']
                        headers = ['studentID'] + ['answer_' + str(k) for k in students_data[0]['answers'].keys()]
                        csv_writer = csv.DictWriter(csv_file, fieldnames=headers)
                        csv_writer.writeheader()
                        for student in students_data:
                            row_data = {'studentID': student['studentID']}
                            row_data.update({'answer_' + k: v for k, v in student['answers'].items()})
                            csv_writer.writerow(row_data)
                    else:
                        if isinstance(data, list) and data:
                            headers = data[0].keys()
                            csv_writer = csv.DictWriter(csv_file, fieldnames=headers)
                            csv_writer.writeheader()
                            for row in data:
                                csv_writer.writerow(row)
                        else:
                            raise ValueError("Unsupported JSON structure")
                
                os.remove(file_path)
                return jsonify({"status": "success", "message": f"File converted to CSV and uploaded successfully: {csv_filename}"})
            except Exception as e:
                print(f"Error converting file: {e}")
                return jsonify({"status": "error", "message": "Error converting file to CSV"})
        else:
            return jsonify({"status": "error", "message": "Only PDF or JSON files are allowed"})
        
    def simulate_ai_data_extraction(file_path):
            students_data = {
                "test_answers": []
            }
            
            # Just for simulation, generate mock answers for a given number of students
            for i in range(10):  # Assuming 10 pages/students for the example
                student_id = f"SID{i+1001}"
                answers = {f"Q{k+1}": f"Answer_{chr(65 + (i+k) % 4)}" for k in range(10)}  # A-D for answers
                students_data["test_answers"].append({"student_id": student_id, "answers": answers})
        
    @app.route('/api/download/<filename>', methods=['GET'])
    def download_file(filename):
        try:
            # Ensure the filename is secure and not traversing directories
            filename = secure_filename(filename)
            if filename.lower().endswith('.pdf') or filename.lower().endswith('.csv'):
                return send_from_directory(uploads_dir, filename, as_attachment=True)
            else:
                return jsonify({"status": "error", "message": "Invalid file type"}), 400
        except FileNotFoundError:
            return jsonify({"status": "error", "message": "File not found"}), 404

    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_CONFIG'))
    app.run(debug=True)
