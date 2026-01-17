class QuizState:
    def __init__(self, questions):
        self.questions = questions
        self.current = 0
        self.score = 0
        self.answered = set()
    def current_question(self):
        return self.questions[self.current]
    def answer(self, choice):
        if self.current in self.answered:
            return False
        correct = self.current_question()["correct"]
        self.answered.add(self.current)
        if choice == correct:
            self.score += 1
            return True
        return False
    def next(self):
        self.current += 1
        return self.current < len(self.questions)