from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/test', methods = ['GET'])
def test():
    
    return jsonify({"message": "Server is working!"})

@app.route('/upload-json', methods=['POST'])
def upload_json_and_convert_to_csv():
    json_data = request.get_json()

    output_csv_path = '/Users/nischitanannapaneni/capstone1/bubble_scan/ServerCode/instance/uploads/results.csv'
    transform_json_to_csv(json_data, output_csv_path)

    return jsonify({"message": "CSV file created successfully"})

@app.route('/get-csv', methods=['GET'])
def get_csv():
    csv_folder = os.path.dirname('path/to/output/data.csv')
    csv_filename = os.path.basename('path/to/output/data.csv')
    return send_from_directory(directory=csv_folder, filename=csv_filename, as_attachment=True)

if __name__ == '__main__':
    
    app.run(debug = True, port = 5000)