import qrcode
from io import BytesIO
import base64
import pyotp
import mongo_operations as mo
import cryptography_operations as cr
from flask import Flask, request, jsonify
from pymongo.errors import DuplicateKeyError
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    # Hash email for unique index
    email_hash = cr.hash_data(data['email'])
        
    totp_secret = pyotp.random_base32()
    data['totp_secret'] = totp_secret

    # Encrypt fields as necessary
    encrypted_data = {
        'firstName': cr.encrypt_field(data['firstName']),
        'lastName': cr.encrypt_field(data['lastName']),
        'email': cr.encrypt_field(data['email']), 
        'password': generate_password_hash(data['password']),
        'role': data['role'],
        'email_hash': email_hash, 
        'totp_secret': cr.encrypt_field(totp_secret),
    }

    if data['role'] != 'Doctor':
        encrypted_data['weight'] = cr.encrypt_field(str(data['weight']))  # Convert to string before encrypting
        encrypted_data['height'] = cr.encrypt_field(str(data['height']))  
        encrypted_data['activityLevel'] = cr.encrypt_field(data['activityLevel'])
        encrypted_data['dateOfBirth'] = cr.encrypt_field(data['dateOfBirth'])
        encrypted_data['gender'] = cr.encrypt_field(data['gender'])

    try:
        mo.insert_user(encrypted_data)
        return {"message": "User registered successfully!"}, 200
    except DuplicateKeyError:
        return {"message": "A user with this email already exists."}, 401


@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email_hash = cr.hash_data(data['email'])
    user = mo.get_user_by_email_hash(email_hash) 

    if user and check_password_hash(user['password'], data['password']):
        # Verify TOTP code
        totp_secret = cr.decrypt_field(user['totp_secret'])
        totp = pyotp.TOTP(totp_secret)
        if totp.verify(data['totp']):
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"message": "Invalid TOTP code!"}), 401
    else:
        return jsonify({"message": "Invalid email or password!"}), 401
    
@app.route('/qrcode', methods=['GET'])
def get_qrcode():
    email = request.args.get('email')
    email_hash = cr.hash_data(email)
    user = mo.get_user_by_email_hash(email_hash)

    if user:
        totp_secret = cr.decrypt_field(user['totp_secret'])
        totp = pyotp.TOTP(totp_secret)
        provisioning_uri = totp.provisioning_uri(email, issuer_name="SHSApp")

        return jsonify({"totp_secret": totp_secret}), 200
    else:
        return jsonify({"message": "User not found!"}), 404
    
@app.route('/validate-totp', methods=['POST'])
def validate_totp():
    data = request.get_json()
    print(data)
    email_hash = cr.hash_data(data['email'])
    user = mo.get_user_by_email_hash(email_hash)

    if user:
        totp_secret = cr.decrypt_field(user['totp_secret'])
        totp = pyotp.TOTP(totp_secret)
        if totp.verify(data['totp']):
            return jsonify({"message": "TOTP validation successful!"}), 200
        else:
            return jsonify({"message": "Invalid TOTP code!"}), 401
    else:
        return jsonify({"message": "User not found!"}), 404

    
@app.route('/patient', methods=['GET'])
def get_patient_data():
    email = request.args.get('email')
    email_hash = cr.hash_data(email)
    user = mo.get_user_by_email_hash(email_hash)

    if user:
        decrypted_user = {
            'firstName': cr.decrypt_field(user['firstName']),
            'lastName': cr.decrypt_field(user['lastName']),
            'email': cr.decrypt_field(user['email']),
            'dateOfBirth': cr.decrypt_field(user['dateOfBirth']),
            'gender': cr.decrypt_field(user['gender']),
            'weight': cr.decrypt_field(user['weight']),
            'height': cr.decrypt_field(user['height']),
            'activityLevel': cr.decrypt_field(user['activityLevel']),
            
        }
        return jsonify(decrypted_user), 200
    else:
        return jsonify({"message": "User not found!"}), 404

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = mo.get_patients()
    decrypted_patients = []

    for patient in patients:
        decrypted_patient = {
            'firstName': cr.decrypt_field(patient['firstName']),
            'lastName': cr.decrypt_field(patient['lastName']),
            'email': cr.decrypt_field(patient['email']),
            'dateOfBirth': cr.decrypt_field(patient['dateOfBirth']),
            'gender': cr.decrypt_field(patient['gender']),
            'weight': cr.decrypt_field(patient['weight']),
            'height': cr.decrypt_field(patient['height']),
            'activityLevel': cr.decrypt_field(patient['activityLevel']),
        }
        decrypted_patients.append(decrypted_patient)

    return jsonify(decrypted_patients), 200



if __name__ == '__main__':
    patients = mo.get_patients()
    decrypted_patients = []

    for patient in patients:
        print(patient['weight'])
    app.run(host='0.0.0.0', port=5000, debug=True)