from flask import Blueprint, request, jsonify
from Domain.User.UserService import UserService
from Domain.User.Models.UserMappingExtensions import user_to_userdb
from functools import partial
from Domain.User.Models.User import User

user_blueprint = Blueprint('user', __name__)
user_service = UserService()

@user_blueprint.route('/register', methods=['POST'])
def register_user():
    try:
        user_data = request.json

        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            birth_date=user_data.get('birth_date'),
            height=user_data['height'],
            weight=user_data['weight'],
            gender=user_data['gender'],
            activity_multiplier=user_data['activity_multiplier']
        )
        print("Controller message",user)
        response = user_service.register_user(user)
        return jsonify(response), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": "An unexpected error occurred"}), 500