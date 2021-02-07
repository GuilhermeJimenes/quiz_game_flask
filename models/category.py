from database import database


class CategoryModel(database.Model):
    __tablename__ = 'category'

    name = database.Column(database.String, primary_key=True, unique=True)
    quizzes = database.relationship('QuizModel')

    def __init__(self, name):
        self.name = name

    def category_json(self):
        return {
            'name': self.name,
            'quizzes': [[quiz.quiz_json() for quiz in self.quizzes]]
        }

    @classmethod
    def find_by_name(cls, name):
        user = cls.query.filter_by(name=name).first()
        if user:
            return user
        return None

    def save_category(self):
        database.session.add(self)
        database.session.commit()

    def update_category(self, name):
        self.name = name
        self.save_category()

    def delete_category(self):
        # deletando TODOS os quizzes associados a categoria informada
        [quiz.delete_quiz() for quiz in self.quizzes]
        # deletando a categoria
        database.session.delete(self)
        database.session.commit()
