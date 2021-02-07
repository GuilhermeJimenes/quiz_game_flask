from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from tools.blacklist import BLACKLIST
from resources.category import Category
from resources.quiz import QuizID, Quiz
from resources.users import User, Register, UserLogin

app = Flask(__name__)  # Flask app instance initiated
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)  # Flask restful wraps Flask app around it.
jwt = JWTManager(app)


@app.before_first_request
def create_database():
    database.create_all()


@jwt.token_in_blacklist_loader
def check_blacklist(token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_invalidated():
    return jsonify({'message': 'You have been logged out.'}), 401


api.add_resource(QuizID, '/quiz/<int:id_quiz>')
api.add_resource(Quiz, '/quiz')

api.add_resource(User, '/user/<int:id_user>')
api.add_resource(Register, '/register')
api.add_resource(UserLogin, '/login')

api.add_resource(Category, '/category/<string:name>')

if __name__ == '__main__':
    from database import database

    database.init_app(app)
    app.run(debug=True)
