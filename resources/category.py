from flask_restful import Resource, reqparse

from models.category import CategoryModel
from tools.message import msg_help

arguments = reqparse.RequestParser()
arguments.add_argument('name', type=str, required=True, help=msg_help('name'))


class Category(Resource):
    def get(self, name):
        """
        Get doc
        """
        category_found = CategoryModel.find_by_name(name)

        if category_found:
            # sucesso
            return category_found.category_json(), 200
        # campo não encontrado
        return {
                   'message': f"the '{name}' category was not found, all were returned.",
                   'categorys': [category.category_json() for category in CategoryModel.query.all()]
               }, 200

    # @jwt_required
    def post(self, name):
        """
        Post doc
        """
        category_found = CategoryModel.find_by_name(name)

        if category_found:
            return {'message': f"the '{name}' category has already been registered."}, 200

        try:
            category_new = CategoryModel(name)
            category_new.save_category()
        except:
            # erro desconhecido
            return {'message': 'An internal error ocurred trying to save category.'}, 500
        # sucesso
        return category_new.category_json(), 200

    # @jwt_required
    def put(self, name):
        """
        Put doc
        """
        data = arguments.parse_args()
        category_found = CategoryModel.find_by_name(name)

        if category_found:
            try:
                category_found.update_category(**data)
            except:
                # erro desconhecido
                return {'message': 'An internal error ocurred trying to update category.'}, 500
            # sucesso
            return category_found.category_json(), 200
        # campo inválido
        return {'message': 'Category not found.'}, 404

    # @jwt_required
    def delete(self, name):
        """
        Delete doc
        """
        category_found = CategoryModel.find_by_name(name)

        if category_found:
            try:
                category_found.delete_category()
            except:
                # erro desconhecido
                return {'message': 'An internal error ocurred trying to delete category.'}, 500
            # sucesso
            return {'message': 'Category deleted.'}, 200
        # campo inválido
        return {'message': f"the '{name}' category was not found."}, 404
