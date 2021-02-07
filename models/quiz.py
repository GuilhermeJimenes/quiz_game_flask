from sqlalchemy import func

from database import database


class QuizModel(database.Model):
    __tablename__ = 'quiz'

    id_quiz = database.Column(database.Integer, primary_key=True)
    question = database.Column(database.String)
    answer_a = database.Column(database.String)
    answer_b = database.Column(database.String)
    answer_c = database.Column(database.String)
    correct_answer = database.Column(database.String)
    category_name = database.Column(database.String, database.ForeignKey('category.name'))
    # pk_category = database.relationship('CategoryModel')

    def __init__(self, question, answer_a, answer_b, answer_c, correct_answer, category_name):
        self.question = question
        self.answer_a = answer_a
        self.answer_b = answer_b
        self.answer_c = answer_c
        self.correct_answer = correct_answer
        self.category_name = category_name

    def quiz_json(self):
        return {
            'id_quiz': self.id_quiz,
            'question': self.question,
            'answer_a': self.answer_a,
            'answer_b': self.answer_b,
            'answer_c': self.answer_c,
            'correct_answer': self.correct_answer,
            'category_name': self.category_name
        }

    @classmethod
    def find_quiz(cls, id_quiz):
        quiz = cls.query.filter_by(id_quiz=id_quiz).first()
        if quiz:
            return quiz
        return None

    @classmethod
    def get_random_quiz(cls, category_name):
        quiz = cls.query.filter_by(category_name=category_name).order_by(func.random()).first()
        if quiz:
            return quiz
        return None

    def save_quiz(self):
        database.session.add(self)
        database.session.commit()

    def update_quiz(self, question, answer_a, answer_b, answer_c, correct_answer, category_name):
        self.question = question
        self.answer_a = answer_a
        self.answer_b = answer_b
        self.answer_c = answer_c
        self.correct_answer = correct_answer
        self.category_name = category_name
        self.save_quiz()

    def delete_quiz(self):
        database.session.delete(self)
        database.session.commit()
