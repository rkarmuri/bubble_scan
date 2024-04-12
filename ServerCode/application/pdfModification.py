import os
import json
import requests
from PyPDF2 import PdfReader, PdfWriter
import csv

def split_pdf_into_pages(pdf_path, output_folder):
    """
    Splits a PDF file into the individual pages and saves each page as a separate PDF file.

    Args: 
        pdf_path (str): Path to the input PDF file.
        output_folder (str): Path to the output folder where individual pages will be
    """

    try: 
        #check if the ouput folder exists, create it if not
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)

        for i in range(num_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
        
            output_filename = os.path.join(output_folder, f"page_{i+1}.pdf")
            with open(output_filename, 'wb') as output_file:
                writer.write(output_file)
        
            print(f"Saved: {output_filename}")

        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False # indicate failure
    
def send_pages_to_mock_ai(pages_folder, mock_ai_url):
    """
    Sends individual PDF pages to the mock AI component for processing.

    Args:
        pages_folder (str): Path to the folder containing individual PDF pages.
        mock_ai_url (str): URL of the mock AI component's endpoint.
    """
    try: 
        for filename in os.listdir(pages_folder):
            if filename.endswith(".pdf"):
                file_path = os.path.join(pages_folder, filename)
                files = {'file': open(file_path, 'rb')}
                response = requests.post(mock_ai_url, files=files)
                if response.status_code == 200:
                    print(f"Successfully sent: {filename} to mock AI component")
                else: 
                    print(f"Failed to send: {filename} to mock AI component")

    except Exception as e:
        print(f"Error: {e}")

def receive_json_from_mock_ai(flask_app):
    """
    Receives JSON format from the mock AI component.

    Args:
        flask_app (Flask app): Instance of the Flask application.

    Returns:
        dict: JSON data received from the mock AI component.
    """
    try: 
        # Assuming the mock AI component sends JSON data via a POST request to the /receive_json endpoint
        json_data = flask_app.request.get_json()
        return json_data
    except Exception as e:
        print(f"Error: {e}")
        return None

def transform_json_to_csv(json_data, output_csv_path):
    """
    Transforms JSON data into CSV format and saves it to a file.

    Args:
        json_data (dict): JSON data to be transformd.
        output_csv_path (str): Path to the output CSV file
    """

    try:
        with open(output_csv_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            #assuming the JSON data is a list of dictionaries with identical keys 
            if json_data:
                keys = json_data[0].keys()
                csv_writer.writerow(keys)
                for item in json_data:
                    csv_writer.writerow(item.values())
            else:
                print("No JSON data to transform")

    except Exception as e:
        print(f"Error: {e}")

# Example usage
pdf_path = 'uploads/Hello.pdf'  # Path to your PDF file
output_folder = 'uploads/pages'  # Folder where individual pages will be saved
mock_ai_url = ' '
output_csv_path = 'output/data.csv' #path to the output CSV file 

#ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

if split_pdf_into_pages(pdf_path, output_folder):
    send_pages_to_mock_ai(output_folder, mock_ai_url)

flask_app = None
json_data = receive_json_from_mock_ai(flask_app)

if json_data:
    transform_json_to_csv(json_data, output_csv_path)
