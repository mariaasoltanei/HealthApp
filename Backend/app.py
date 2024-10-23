from flask import Flask, g
from Database.IoTDBConnection import IoTDBConnection
from WebAPI.User.UserController import user_bp
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.register_blueprint(user_bp)

# Helper function to get the IoTDB connection from the Flask g object
def get_db_connection():
    if 'iotdb_connection' not in g:
        g.iotdb_connection = IoTDBConnection(
            host=os.getenv('iotdb_ip'), 
            port=int(os.getenv('iotdb_port')),  # Ensure port is passed as an integer
            username=os.getenv('iotdb_username'), 
            password=os.getenv('iotdb_password')
        )
        g.iotdb_connection.connect()
    return g.iotdb_connection

# Correct decorator: Initialize the database connection before the first request
@app.before_first_request
def init_db():
    get_db_connection()

# Close the connection when the application context ends
@app.teardown_appcontext
def close_db_connection(exception):
    connection = g.pop('iotdb_connection', None)
    if connection is not None:
        connection.close()

if __name__ == "__main__":
    app.run(debug=True)
