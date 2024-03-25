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
            # Split PDF into separate pages
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(uploads_dir, filename)
                file.save(file_path)  # Save the file temporarily to read its content
                
                with open(file_path, 'rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    for page_num, page in enumerate(pdf_reader.pages):
                        output_filename = f"{filename}_page_{page_num + 1}.pdf"
                        output_filepath = os.path.join(uploads_dir, output_filename)
                        pdf_writer = PdfWriter()
                        pdf_writer.add_page(page)
                        with open(output_filepath, 'wb') as output_file:
                            pdf_writer.write(output_file)
                
                # Optionally, remove the original PDF file after splitting
                os.remove(file_path)
                
                print(f"PDF split into separate pages and saved successfully.")
                return jsonify({"status": "success", "message": f"PDF split into separate pages and saved successfully."})
            except Exception as e:
                print(f"Error splitting PDF: {e}")
                return jsonify({"status": "error", "message": "Error splitting PDF"})

        elif file and file.filename.lower().endswith('.json'):
            # Convert JSON to CSV
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
                
                # Optionally, remove the JSON file after conversion
                os.remove(file_path)
                
                print(f"File converted and saved successfully: {csv_filepath}")
                return jsonify({"status": "success", "message": f"File converted to CSV and uploaded successfully: {csv_filename}"})
            except Exception as e:
                print(f"Error converting file: {e}")
                return jsonify({"status": "error", "message": "Error converting file to CSV"})
        else:
            return jsonify({"status": "error", "message": "Only PDF or JSON files are allowed"})

    # New endpoint for downloading files
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
