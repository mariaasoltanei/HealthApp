from flask import Flask, g
from Database.IoTDBConnection import IoTDBConnection
from WebAPI.User.UserController import user_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(user_bp)


def get_db_connection():
    if 'iotdb_connection' not in g:
        g.iotdb_connection = IoTDBConnection(
            host=os.getenv('iotdb_ip'), 
            port=int(os.getenv('iotdb_port')),
            username=os.getenv('iotdb_username'), 
            password=os.getenv('iotdb_password')
        )
        g.iotdb_connection.connect()
    return g.iotdb_connection

@app.before_first_request
def init_db():
    get_db_connection()

# @app.teardown_appcontext
# def close_db_connection(exception):
#     connection = g.pop('iotdb_connection', None)
#     if connection is not None:
#         connection.close()

if __name__ == "__main__":
    app.run(debug=True)
