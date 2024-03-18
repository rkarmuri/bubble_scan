from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import csv
import json
from werkzeug.utils import secure_filename

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
        
        if file and file.filename.lower().endswith('.json'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(uploads_dir, filename)
            file.save(file_path)  # Save the file temporarily to read its content
            
            try:
                # Convert JSON to CSV
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    
                csv_filename = filename.rsplit('.', 1)[0] + '.csv'
                csv_filepath = os.path.join(uploads_dir, csv_filename)
                
                with open(csv_filepath, 'w', newline='') as csv_file:
                    if data:
                        headers = data[0].keys()
                        csv_writer = csv.DictWriter(csv_file, fieldnames=headers)
                        csv_writer.writeheader()
                        for row in data:
                            csv_writer.writerow(row)
                
                # Optionally, remove the JSON file after conversion
                os.remove(file_path)
                
                print(f"File converted and saved successfully: {csv_filepath}")
                return jsonify({"status": "success", "message": f"File converted to CSV and uploaded successfully: {csv_filename}"})
            except Exception as e:
                print(f"Error converting file: {e}")
                return jsonify({"status": "error", "message": "Error converting file to CSV"})
        else:
            return jsonify({"status": "error", "message": "Only JSON files are allowed"})

    # New endpoint for downloading files
    @app.route('/api/download/<filename>', methods=['GET'])
    def download_file(filename):
        try:
            # Ensure the filename is secure and not traversing directories
            filename = secure_filename(filename)
            if filename.lower().endswith('.csv'):
                return send_from_directory(uploads_dir, filename, as_attachment=True)
            else:
                return jsonify({"status": "error", "message": "Invalid file type"}), 400
        except FileNotFoundError:
            return jsonify({"status": "error", "message": "File not found"}), 404

    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_CONFIG'))
    app.run(debug=True)
