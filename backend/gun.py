import sqlite3
import datetime
import logging
from police import PoliceOfficer

DATABASE = 'gun_tracking.db'
TRANSACTIONS_DATABASE = 'gun_tracking_transactions.db'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Gun:
    GUN_TYPES = {
        'Handgun': 'Handgun',
        'Shotgun': 'Shotgun',
        'Rifle': 'Rifle',
        'Sniper Rifle': 'Sniper Rifle'
    }

    RANK_ELIGIBILITY = {
        'Police Officer': ['Handgun'],
        'Sergeant': ['Handgun', 'Shotgun'],
        'Lieutenant': ['Handgun', 'Shotgun', 'Rifle'],
        'Captain': ['Handgun', 'Shotgun', 'Rifle', 'Sniper Rifle']
    }

    def __init__(self, serialNumber, gunType, manufacturerDate, gunStatus, check_in_time=None, check_out_time=None, check_out_officer=None, officer_Id=None):
        self.serialNumber = serialNumber
        self.gunType = gunType
        self.manufacturerDate = manufacturerDate
        self.gunStatus = gunStatus
        self.check_in_time = check_in_time
        self.check_out_time = check_out_time
        self.check_out_officer = check_out_officer
        self.officer_Id = officer_Id

    @classmethod
    def existing_gun(cls, serialNumber):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM guns WHERE serialNumber=?", (serialNumber,))
        gun_data = cursor.fetchone()
        conn.close()
        if gun_data:
            return cls(*gun_data)
        else:
            return None

    def check_in(self, police_officer):
        if self.gunStatus == 'check_in':
            return {"error": "Gun already checked in"}
        if self.check_out_officer and self.check_out_officer != police_officer:
            return {"error": "This gun was checked out by another officer."}

        self.gunStatus = "check_in"
        self.check_in_time = datetime.datetime.now()
        self.check_out_time = None
        self.check_out_officer = None
        self.officer_Id = police_officer.policeId
        self.update_time_database()
        self.record_transaction(police_officer)
        return {"success": f"Gun checked in successfully by {police_officer.first_name} {police_officer.last_name}"}

    def check_out(self, police_officer):
        if self.gunStatus == 'check_out':
            return {"error": "Gun already checked out"}
        

        # Check if the officer rank is eligible for the gun type
        if not self.is_officer_eligible(police_officer.rank, self.gunType):
            return {"error": f"{police_officer.rank} officers are not eligible to check out this type of gun"}

        self.gunStatus = "check_out"
        self.check_out_time = datetime.datetime.now()
        self.check_in_time = None
        self.officer_Id = police_officer.policeId
        self.check_out_officer = police_officer
        self.update_time_database()
        self.record_transaction(police_officer)
        return {"success": f"Gun checked out successfully to: {police_officer.first_name} {police_officer.last_name}, {police_officer.rank}"}

    def is_officer_eligible(self, officer_rank, gun_type):
        return gun_type in self.RANK_ELIGIBILITY.get(officer_rank, [])

    @classmethod
    def create_transactions_table(cls):
        conn = sqlite3.connect(TRANSACTIONS_DATABASE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS gun_transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    serialNumber TEXT,
                    police_id TEXT,
                    transaction_type TEXT,
                    transaction_date TEXT,
                    FOREIGN KEY (serialNumber) REFERENCES guns (serialNumber)
                )''')
        conn.commit()
        conn.close()

    def record_transaction(self, police_officer=None):
        conn = sqlite3.connect(TRANSACTIONS_DATABASE)
        cursor = conn.cursor()
        transaction_type = 'check_in' if self.gunStatus == 'check_in' else 'check_out'
        cursor.execute(
            "INSERT INTO gun_transactions (serialNumber, police_id, transaction_type, transaction_date) VALUES (?, ?, ?, ?)",
            (self.serialNumber, self.officer_Id, transaction_type, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        

    def save(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO guns (serialNumber, gunType, manufacturerDate, gunStatus, check_in_time, check_out_time) VALUES (?, ?, ?, ?, ?, ?)",
                       (self.serialNumber, self.gunType, self.manufacturerDate, self.gunStatus, self.check_in_time, self.check_out_time))
        conn.commit()
        conn.close()

    def update_time_database(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE guns SET gunStatus=?, check_in_time=?, check_out_time=? WHERE serialNumber=?",
                       (self.gunStatus, self.check_in_time, self.check_out_time, self.serialNumber))
        conn.commit()
        conn.close()

    @classmethod
    def create_table(cls):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS guns (
                        serialNumber TEXT PRIMARY KEY,
                        gunType TEXT NOT NULL,
                        manufacturerDate TEXT,
                        gunStatus TEXT NOT NULL,
                        check_in_time TEXT,
                        check_out_time TEXT,
                        check_out_officer TEXT,
                        officer_Id TEXT
                    )''')
        conn.commit()
        conn.close()

    @staticmethod
    def get(serialNumber):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT serialNumber, gunType, manufacturerDate, gunStatus, check_in_time, check_out_time, check_out_officer, officer_Id FROM guns WHERE serialNumber=?", (serialNumber,))
        gun_data = cursor.fetchone()
        conn.close()
        if gun_data:
            return Gun(*gun_data[:4], check_in_time=gun_data[4], check_out_time=gun_data[5], check_out_officer=gun_data[6], officer_Id=gun_data[7])
        else:
            return None
        
    @staticmethod
    def register_gun(serialNumber, gunType, manufacturerDate, gunStatus):
        gun = Gun(serialNumber, gunType, manufacturerDate, gunStatus)
        gun.save()
        return "Gun registered successfully."

    @staticmethod
    def list_all_guns():
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM guns")
        all_guns = cursor.fetchall()
        conn.close()
        # Convert to list of dictionaries
        guns = []
        for gun in all_guns:
            guns.append({
                'serialNumber': gun[0],
                'gunType': gun[1],
                'manufacturerDate': gun[2],
                'gunStatus': gun[3]
            })
        return guns

    @staticmethod
    def view_transactions():
        conn = sqlite3.connect(TRANSACTIONS_DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gun_transactions")
        transactions = cursor.fetchall()
        conn.close()
        transactions = []
        for transaction in transactions:
            transactions.append({
                'transactionId': transaction[0],
                'serialNumber': transaction[1],
                'police_id ': transaction[2],
                'transaction_type': transaction[3],
                'transaction_date': transaction[4]
            })
        return transactions

    @staticmethod
    def initialize_db():
        Gun.create_table()
        Gun.create_transactions_table()
Gun.initialize_db()
