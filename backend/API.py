from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from gun import Gun
import jwt
from police import PoliceOfficer
import datetime
from login import authenticate_user, add_admin_user, get_user_by_email, send_reset_email
import sqlite3
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
CORS(app)

# Secret key for JWT
app.config['SECRET_KEY'] = 'f3409b3ed086f6b5756574730a00590a'


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/register_gun', methods=['POST'])
def register_gun():
    try:
        data = request.json
        serialNumber = data.get('serialNumber')
        gunType = data.get('gunType')
        manufacturerDate = data.get('manufacturerDate')
        gunStatus = data.get('gunStatus')

        app.logger.debug(f"Received data: {data}")

        result = Gun.register_gun(serialNumber, gunType, manufacturerDate, gunStatus)

        app.logger.debug(f"Gun registered: {result}")

        return jsonify({"message": result}), 200
    except Exception as e:
        app.logger.error(f"Error registering gun: {e}")
        return jsonify({"error": "An error occurred while registering the gun"}), 500


@app.route('/api/list_guns', methods=['GET'])
def list_guns():
    guns = Gun.list_all_guns()
    return jsonify(guns)

@app.route('/register_police', methods=['POST'])
def register_police():
    data = request.json
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    police_id = data.get('policeId')
    rank = data.get('rank')
    email = data.get('email')
    phone = data.get('phone')

    if not PoliceOfficer.validate_policeID(police_id):
        return jsonify({"error": "Invalid Police ID"})
    if not PoliceOfficer.validate_email(email):
        return jsonify({"error": "Invalid Email"})
    if not PoliceOfficer.validate_phone(phone):
        return jsonify({"error": "Invalid Phone Number"})

    result = PoliceOfficer.create_police(first_name, last_name, police_id, rank, email, phone)
    return jsonify({"message": result})

@app.route('/api/list_officers', methods=['GET'])
def list_officers():
    officers = PoliceOfficer.list_all_officers()
    return jsonify(officers)

@app.route('/check_out', methods=['POST'])
def check_out():
    data = request.json
    serial_number = data.get('serialNumber')
    police_id = data.get('policeId')

    gun = Gun.get(serial_number)
    if not gun:
        return jsonify({"error": "Gun not found"})

    police_officer = PoliceOfficer.existing_police(police_id)
    if not police_officer:
        return jsonify({"error": "Police officer not found"})

    result = gun.check_out(police_officer)
    return jsonify(result)

@app.route('/check_in_gun', methods=['POST'])
def check_in_gun():
    data = request.json
    serial_number = data.get('serialNumber')
    police_id = data.get('policeId')

    gun = Gun.get(serial_number)
    if not gun:
        return jsonify({"error": "Gun not found"})

    police_officer = PoliceOfficer.existing_police(police_id)
    if not police_officer:
        return jsonify({"error": "Police officer not found"})

    result = gun.check_in(police_officer)
    return jsonify(result)

@app.route('/api/transaction', methods=['GET'])
def transaction():
    transactions = Gun.view_transactions()
    return jsonify(transactions)

@app.route('/api/login', methods=['POST'])
def login():
    try:
        login_data = request.get_json()
        email = login_data.get('email')
        password = login_data.get('password')
        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400

        success, message = authenticate_user(email, password)
        if success:
            return jsonify({'message': 'Login successful', 'token': message}), 200
        return jsonify({'error': message}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')
    user = get_user_by_email(email)
    if user:
        reset_token = jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
        send_reset_email(email, reset_token)
        return jsonify({'message': 'Password reset email sent'}), 200
    return jsonify({'error': 'Email not found'}), 404

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        token = request.args.get('token')
        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            return render_template('reset_pass.html', token=token)
        except jwt.ExpiredSignatureError:
            return 'Token expired', 400
        except jwt.InvalidTokenError:
            return 'Invalid token', 400
    elif request.method == 'POST':
        token = request.form['token']
        new_password = request.form['new_password']
        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            email = decoded['email']
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = ? WHERE email = ?', (new_password, email))
            conn.commit()
            conn.close()
            return 'Password reset successful', 200
        except jwt.ExpiredSignatureError:
            return 'Token expired', 400
        except jwt.InvalidTokenError:
            return 'Invalid token', 400

if __name__ == '__main__':

    app.run(debug=True)


