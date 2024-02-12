#high level component that interacts with the server to process the data
# - defines an interface for sending input file (pdf or image format)
# - provides a mock student id and mock answers for each input file as a response
# in the form of a list of answers for each question
# - mock response is defined as a file

import random

class AIGrader:

    def __init__(self, response_file = 'mock_response.txt'):
        self.mock_responses = self.load_mock_responses(response_file)
        
    def load_response():
        with open(response_file, 'r') as file:
            lines = file.readlines()
            return [line.strip().split(',') for line in lines]
        
    def generate_response():
        num_questions = len(self.mock_responses[0])
        return [random.choice(['a', 'b', 'c', 'd', '-']) for _ in range (num_questions)]
        
    def process_input():
        student_id = self.get_studentID(file_path)
        mock_response = self.generate_mock_response(student_id)

        return student_id, mock_response;
        
    def get_studentID():
        return f"MockStudentID_{random.randint(1000, 9999)}"
    
if __name__ == "__main__":
    mock_grader = MockAIGrader()

    input_file_path = "path/to/your/input_file.pdf"
    student_id, mock_response = mock_grader.process_input_file(input_file_path)

    print(f"Mock Student ID: {student_id}")
    print("Mock Response:")
    print(mock_response)