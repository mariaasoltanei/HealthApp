from flask import Blueprint, request, jsonify
from Domain.User.UserService import UserService
from WebAPI.User.Models.CreateUserDto import CreateUserDto
from WebAPI.User.UserMappingExtensions import UserMappingExtensions
from functools import partial

class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.user_bp = Blueprint('user_bp', __name__)
        print('UserController initialized')

        self.user_bp.add_url_rule('/user', 'create_user', partial(self.create_user), methods=['POST'])
    
    def create_user(self):
        data = request.get_json()
        create_user_dto = CreateUserDto(**data)

        user = UserMappingExtensions.create_from_dto(create_user_dto)
        self.user_service.create_user(user)

        return jsonify({"message": "User created successfully"}), 201
