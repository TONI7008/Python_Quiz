import json

class Direction:
    Left, Right = range(2)
    
class Questionnaire:
    def __init__(self, file_path):
        self.filepath = file_path
        self.data = self.load_data()
    
    def load_data(self):
        with open(self.filepath) as f:
            data = json.load(f)
            return data
    
    def get_question_info(self, index):
        question_name="Question "+str(index)
        question_data = self.data.get(question_name)
            
        if question_data:
            question = question_data.get('question')
            reponse = question_data.get('reponse')
            options = question_data.get('options')
                
            question_info = {
                'question': question,
                'reponse': reponse,
                'options': options
            }
                
            return question_info
        else:
            return None

    def get_length(self):
        return len(self.data)



