"""
Module to represent MockAI features as a placeholder for future expansion using 
actual machine learning techniques.
"""

import random
import requests

class AIGrader:
    """
    Class docstring goes here.
    """

    def __init__(self, server_url = 'http://localhost:5000', response_file = 'mock_response.txt'):
        """
        Initialization of 'AI grader' object
        :param server_url: the URL of server for processing data
        :param response_file: the file containing mock responses.
        """
        self.server_url = server_url
        self.mock_responses = self.load_responses(response_file)

    def load_responses(self, response_file):
        """
        Loads mock responses from the specified file.

        :return: a list of mock responses.
        """
        with open(response_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return [line.strip().split(',') for line in lines]

    def generate_response(self, student_id):
        """
        Generate a mock response for a given student ID

        :param student_ID: the ID of the student.
        :return: A list of mock answers for each question.
        """
        num_questions = len(self.mock_responses[0])
        return [f"{self.create_response()} for {student_id}" for _ in range(num_questions)]

    def create_response(self):
        """
        Create a mock response for a single question.

        :return: a mock answer for a question.
        """
        answer_choices = ['a', 'b', 'c', 'd', '-']
        return random.choice(answer_choices)

    def process_input(self, file_path):
        """
        Process the input file by sending it to the server and receiving a mock response.

        :param file_path: the path to the input file (PDF or image format)
        :return: A tuple containing the student ID and the mock response
        """
        student_id = self.get_student_id()
        mock_response = self.send_file_to_server(file_path)

        return student_id, mock_response

    def get_student_id(self):
        """
        Generate a mock student ID for a given input file.

        return: a mock student ID
        """
        return f"MockStudentID_{random.randint(1000, 9999)}"

    def send_file_to_server(self, file_path):
        """
        Send the input file to the server and receive a mock response.

        return: a list of mock answers for each question.
        """

        with open(file_path, 'rb') as file:
            files = {'file':file}
            response = requests.post(f"{self.server_url}/process_input", files=files)
            data = response.json()
            return data.get("mock_response", [])

if __name__ == "__main__":
    mock_grader = AIGrader()

    INPUT_FILE_PATH = "path/to/your/input_file.pdf"
    stud_id, mock_resp = mock_grader.process_input(INPUT_FILE_PATH)

    print(f"Mock Student ID: {stud_id}")
    print("Mock Response:")
    print(mock_resp)
