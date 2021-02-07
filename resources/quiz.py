from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from models.category import CategoryModel
from models.quiz import QuizModel
from models.rank import RankModel
from models.users import UserModel
from tools.message import msg_help

arguments = reqparse.RequestParser()
arguments.add_argument('question', type=str, required=True, help=msg_help('question'))
arguments.add_argument('answer_a', type=str, required=True, help=msg_help('answer_a'))
arguments.add_argument('answer_b', type=str, required=True, help=msg_help('answer_b'))
arguments.add_argument('answer_c', type=str, required=True, help=msg_help('answer_c'))
arguments.add_argument('correct_answer', type=str, required=True, help=msg_help('correct_answer'))
arguments.add_argument('category_name', type=str, required=True, help=msg_help('category_name'))


class QuizID(Resource):
    def get(self, id_quiz):
        """
        Get pegar um quiz por id se não achar pegar todos
        """
        quiz_found = QuizModel.find_quiz(id_quiz)
        if quiz_found:
            return quiz_found.quiz_json(), 200
        return {
                   'message': 'Quiz id not found, all were returned.',
                   'quizzes': [quiz.quiz_json() for quiz in QuizModel.query.all()]
               }, 200

    @jwt_required
    def post(self, id_quiz):
        """
        Post responde um quiz
        """
        # Parâmetros da requisição
        args = reqparse.RequestParser()
        args.add_argument('answer_user', type=str, required=True, help=msg_help('answer_user'))
        data = args.parse_args()

        # Trata valores inválidos
        quiz_found = QuizModel.find_quiz(id_quiz)
        if not quiz_found:
            return {'message': 'no quiz was registered.'}, 404

        answer_user = data.get('answer_user').lower()
        if answer_user != 'a' and answer_user != 'b' and answer_user != 'c':
            return {'message': "the field 'answer_user' must be 'a' or 'b' or 'c'."}, 400

        # Busca dados do quiz
        # quiz_found = quiz_found.quiz_json()
        correct_answer = quiz_found.correct_answer
        category_name = quiz_found.category_name

        # Busca Rank e cria se não existir
        current_user_id = get_jwt_identity()
        rank = RankModel.find_rank_by_user_and_category(category_name, current_user_id)
        if not rank:
            rank = RankModel(category_name, current_user_id)
            rank.save_rank()

        # Pontua o acerto ou erro
        if correct_answer == answer_user:
            rank.right()
            return {'message': 'very well! right answer.'}, 200
        else:
            rank.wrong()
            return {'message': "Oops! it wasn't this time, you were wrong."}, 200

    # @jwt_required
    def put(self, id_quiz):
        """
        Put altera por id
        """
        data = arguments.parse_args()
        quiz_found = QuizModel.find_quiz(id_quiz)

        if quiz_found:
            quiz_found.update_quiz(**data)
            return quiz_found.quiz_json(), 200
        return {'message': 'Quiz not found.'}, 404

    # @jwt_required
    def delete(self, id_quiz):
        """
        Delete deleta por id
        """
        quiz_found = QuizModel.find_quiz(id_quiz)
        if quiz_found:
            try:
                quiz_found.delete_quiz()
            except:
                return {'message': 'An internal error ocurred trying to delete quiz.'}, 500
            return {'message': 'Quiz deleted.'}
        return {'message': 'Quiz not found.'}, 404


class Quiz(Resource):
    def get(self):
        """
        Get pega um quiz aleatorio pela categoria
        """
        try:
            args = reqparse.RequestParser()
            args.add_argument('category_name', type=str, required=True, help=msg_help('category_name'))
            data = args.parse_args()
            category = data.get('category_name')
            quiz_found = QuizModel.get_random_quiz(category)
        except:
            return {'message': 'An internal error ocurred trying to get random quiz.'}, 500

        if not quiz_found:
            return {'message': 'no quiz was registered.'}, 404
        return quiz_found.quiz_json()

    # @jwt_required
    def post(self):
        """
        Post registra um novo quiz pela categoria
        """
        data = arguments.parse_args()
        category = data.get('category_name')
        quiz_new = QuizModel(**data)

        if not CategoryModel.find_by_name(category):
            return {'message': 'The Quiz must be associated to a valid category_name.'}, 400

        try:
            quiz_new.save_quiz()
        except:
            return {'message': 'An internal error ocurred trying to save quiz.'}, 500
        return quiz_new.quiz_json(), 200
