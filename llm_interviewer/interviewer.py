import json
import random

class Interviewer:
    def __init__(self, question_file):
        with open(question_file, "r") as f:
            self.questions = json.load(f)

        self.difficulty = "easy"
        self.accuracy = 0
        self.total = 0
        self.correct = 0

    def get_question(self):
        if self.difficulty not in self.questions:
            return "No questions available for difficulty: " + self.difficulty

        question_list = self.questions[self.difficulty]
        return random.choice(question_list)

    def update_score(self, is_correct):
        self.total += 1
        if is_correct:
            self.correct += 1

        self.accuracy = (self.correct / self.total) * 100

        # Update difficulty based on performance
        if self.accuracy >= 75:
            self.difficulty = "hard"
        elif self.accuracy >= 50:
            self.difficulty = "medium"
        else:
            self.difficulty = "easy"

        return self.accuracy, self.difficulty
