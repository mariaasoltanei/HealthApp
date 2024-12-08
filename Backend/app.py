from flask import Flask, g
from Database.IoTDBConnection import IoTDBConnection
from WebAPI.User.UserController import user_blueprint
from Database.User.UserRepository import UserRepository
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)

    app.register_blueprint(user_blueprint, url_prefix='/users')

    initialize_database()

    return app

def initialize_database():
    repository = UserRepository()
    repository.create_timeseries()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
