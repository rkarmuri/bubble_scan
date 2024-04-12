#high level component that interacts with the server to process the data
# - defines an interface for sending input file (pdf or image format)
# - provides a mock student id and mock answers for each input file as a response
# in the form of a list of answers for each question
# - mock response is defined as a file

import requests
import random

class AIGrader:
    def __init__(self, server_url = 'http://localhost:5000', response_file = 'mock_response.txt'):
        self.server_url = server_url
        self.mock_responses = self.load_mock_responses(response_file)
        
    def load_responses(self, response_file):
        with open(response_file, 'r') as file:
            lines = file.readlines()
            return [line.strip().split(',') for line in lines]
        
    def generate_response(self, student_id):
        num_questions = len(self.mock_responses[0])
        return [self.create_response() for _ in range (num_questions)]
        
    def create_response(self):
        answer_choices = ['a', 'b', 'c', 'd', '-']
        return f"{random.choice(answer_choices)}"

    def process_input(self, file_path):
        student_id = self.get_studentID(file_path)
        mock_response = self.send_file_to_server(file_path)

        return student_id, mock_response
        
    def get_studentID(self, file_path):
        return f"MockStudentID_{random.randint(1000, 9999)}"
    
    def send_file_to_server(self, file_path):
        files = {'file': open(file_path, 'rb')}
        response = requests.post(f"{self.server_url}/process_input", files=files)
        data = response.json()
        return data.get("mock_response", [])
    
if __name__ == "__main__":
    mock_grader = AIGrader()

    input_file_path = "path/to/your/input_file.pdf"
    student_id, mock_response = mock_grader.process_input_file(input_file_path)

    print(f"Mock Student ID: {student_id}")
    print("Mock Response:")
    print(mock_response)