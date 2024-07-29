import sqlite3
import jwt
import logging
import re
from datetime import datetime, timedelta

DATABASE = 'gun_tracking.db'
SECRET_KEY = '4560faf6437a9c6505a35059b5e2c5e4'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PoliceOfficer:
    RANKS = {
        1: 'Inspector',
        2: 'Police Officer',
        3: 'Sergeant',
        4: 'Lieutenant',
        5: 'Captain',
        6: 'Chief'
    }

    def __init__(self, policeId, first_name, last_name, rank, email, phone):
        self.policeId = policeId
        self.first_name = first_name
        self.last_name = last_name
        self.rank = rank
        self.email = email
        self.phone = phone

    @staticmethod
    def connect_db():
        try:
            conn = sqlite3.connect(DATABASE)
            logging.info("Database connection established.")
            return conn
        except sqlite3.Error as e:
            logging.error(f"Database connection failed: {e}")
            raise

    @staticmethod
    def create_table():
        conn = PoliceOfficer.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS police_officers (
                    police_id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    rank INTEGER NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL
                )
            ''')
            conn.commit()
            logging.info("Table 'police_officers' created successfully.")
        except sqlite3.Error as e:
            logging.error(f"Error creating table: {e}")
        finally:
            conn.close()

    @staticmethod
    def create_police(first_name, last_name, police_id, rank, email, phone):
        if not PoliceOfficer.validate_email(email):
            return "Error: Invalid email address."
        if not PoliceOfficer.validate_phone(phone):
            return "Error: Invalid phone number."
        if not PoliceOfficer.validate_policeID(police_id):
            return "Error: Invalid police ID."
        
        conn = PoliceOfficer.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO police_officers (police_id, first_name, last_name, rank, email, phone)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (police_id, first_name, last_name, rank, email, phone))
            conn.commit()
            logging.info(f"Police officer {police_id} registered successfully.")
            return "Police officer registered successfully."
        except sqlite3.IntegrityError as e:
            logging.error(f"Error registering police officer: {e}")
            return "Error: Police officer already exists."
        except sqlite3.Error as e:
            logging.error(f"Error registering police officer: {e}")
            return "Error: Could not register police officer."
        finally:
            conn.close()

    @staticmethod
    def list_all_officers():
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM police_officers")
        all_officers = cursor.fetchall()
        conn.close()
        # Convert to list of dictionaries
        officers = []
        for officer in all_officers:
            officers.append({
                'policeId': officer[0],
                'firstName': officer[1],
                'lastName': officer[2],
                'rank': officer[3],
                'email': officer[4],
                'phonenumber': officer[5]
            })
        return officers

    @staticmethod
    def existing_police(police_id):
        conn = PoliceOfficer.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM police_officers WHERE police_id = ?', (police_id,))
            officer = cursor.fetchone()
            if officer:
                logging.info(f"Police officer {police_id} found.")
                return PoliceOfficer(*officer)
            else:
                logging.warning(f"Police officer {police_id} not found.")
                return None
        except sqlite3.Error as e:
            logging.error(f"Error fetching police officer {police_id}: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_email(email):
        conn = PoliceOfficer.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM police_officers WHERE email = ?', (email,))
            officer = cursor.fetchone()
            if officer:
                logging.info(f"Police officer with email {email} found.")
                return PoliceOfficer(*officer)
            else:
                logging.warning(f"Police officer with email {email} not found.")
                return None
        except sqlite3.Error as e:
            logging.error(f"Error fetching police officer with email {email}: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def generate_token(police_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': police_id
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            logging.info(f"Token generated for police officer {police_id}.")
            return token
        except Exception as e:
            logging.error(f"Error generating token: {e}")
            return None

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token.split(' ')[1], SECRET_KEY, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise Exception('Token expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise Exception('Invalid token. Please log in again.')
   
    @staticmethod
    def validate_email(email):
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(regex, email):
            logging.info("Email validation passed.")
            return True
        else:
            logging.warning("Email validation failed.")
            return False

    @staticmethod
    def validate_phone(phone):
        regex = r'^(01|07)\d{8}$'
        if re.match(regex, phone):
            logging.info("Phone number validation passed.")
            return True
        else:
            logging.warning("Phone number validation failed.")
            return False

    @staticmethod
    def validate_policeID(police_id):
        # Example validation: police_id can include alphanumeric characters and special characters (-, _, .)
        regex = r'^[a-zA-Z0-9\.]{4,6}$'
        if re.match(regex, police_id):
            logging.info("Police ID validation passed.")
            return True
        else:
            logging.warning("Police ID validation failed.")
            return False

PoliceOfficer.create_table()
