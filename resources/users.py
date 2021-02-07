from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from tools.blacklist import BLACKLIST
from models.users import UserModel
from tools.message import msg_help

arguments = reqparse.RequestParser()
arguments.add_argument('login', type=str, required=True, help=msg_help('login'))
arguments.add_argument('password', type=str, required=True, help=msg_help('password'))
# arguments.add_argument('activated', type=bool)


#  Restful way of creating APIs through Flask Restful
# @doc(tags=['User'])
class User(Resource):
    def get(self, id_user):
        """
        Get doc
        """
        user_found = UserModel.find_user(id_user)

        if user_found:
            return user_found.user_json(), 200
        return {
                   'message': 'User id not found, all were returned.',
                   'users': [user.user_json() for user in UserModel.query.all()]
               }, 200

    @jwt_required
    def put(self, id_user):
        """
        Put doc
        """
        data = arguments.parse_args()
        user_found = UserModel.find_user(id_user)

        if user_found:
            user_found.update_user(**data)
            return user_found.user_json(), 200
        return {'message': 'User not found.'}, 404

    @jwt_required
    def delete(self, id_user):
        """
        Delete doc
        """
        user_found = UserModel.find_user(id_user)
        if user_found:
            try:
                user_found.delete_user()
            except:
                return {'message': 'An internal error ocurred trying to delete user.'}, 500
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404


class Register(Resource):
    def post(self):
        """
        Post doc
        """
        data = arguments.parse_args()

        user = UserModel.find_by_login(data.get('login'))
        if user:
            return {'message': 'this login is already being used.'}, 401

        user_new = UserModel(**data)
        try:
            user_new.save_user()
        except:
            return {'message': 'An internal error ocurred trying to save user.'}, 500
        return user_new.user_json(), 200


class UserLogin(Resource):
    def post(self):
        data = arguments.parse_args()

        user = UserModel.find_by_login(data.get('login'))

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id_user)
            return {'access_token': access_token}, 200
        return {'message': 'The username or password is incorrect.'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        id_jwt = get_raw_jwt()['jti']  # JWT Token Identifier
        BLACKLIST.add(id_jwt)
        return {'message': 'Logged out successfully!'}, 200
