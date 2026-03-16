class Quiz:
    def __init__(self, questions):
        self.questions = questions
    def display_questions(self):
        for question in self.questions:
            print(question)