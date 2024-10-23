from Domain.User.Models.User import User
from WebAPI.User.Models import CreateUserDto, UserDto, BaseUserDto, UsersDto
from typing import List

class UserMappingExtensions:
    
    @staticmethod
    def create_from_dto(create_user_dto: CreateUserDto) -> User:
        """Creates a User domain model from a CreateUserDto."""
        return User(
            create_user_dto.first_name,
            create_user_dto.last_name,
            create_user_dto.email,
            create_user_dto.birth_date,
            create_user_dto.height,
            create_user_dto.weight,
            create_user_dto.gender,
            create_user_dto.activity_multiplier
        )

    @staticmethod
    def map_from_dto(user: User, user_dto: BaseUserDto):
        """Maps values from BaseUserDto to an existing User."""
        user.first_name = user_dto.first_name
        user.last_name = user_dto.last_name
        user.email = user_dto.email
        user.birth_date = user_dto.birth_date
        user.height = user_dto.height
        user.weight = user_dto.weight

    @staticmethod
    def map_to_dto(user: User) -> UserDto:
        """Maps a User domain model to a UserDto."""
        return UserDto(
            user.first_name,
            user.last_name,
            user.email,
            user.birth_date,
            user.height,
            user.weight,
            user.gender,
            user.activity_multiplier
        )

    @staticmethod
    def map_to_dto_list(users: List[User]) -> UsersDto:
        """Maps a list of User domain models to a UsersDto (list of UserDto)."""
        return UsersDto([UserMappingExtensions.map_to_dto(user) for user in users])
