from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import hashlib
import jwt
from datetime import datetime, timedelta
from functools import wraps
import re

# ------------------- APP CONFIG -------------------

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/train2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'greeva-train-jwt-secret-key-2024-production-secure-12345'  # Strong secret key for JWT

db = SQLAlchemy(app)

# ------------------- UTILITIES -------------------

def hash_password_sha1(password):
    return hashlib.sha1(password.encode()).hexdigest()

def is_valid_phone(phone):
    return str(phone).isdigit() and len(str(phone)) == 10

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# ------------------- TOKEN VALIDATOR -------------------

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Signup.query.get(data['user_id'])
        except Exception as e:
            return jsonify({'message': 'Token is invalid or expired', 'error': str(e)}), 401

        return f(current_user, *args, **kwargs)
    return decorated

# ------------------- MODELS -------------------

class Station(db.Model):
    _tablename_ = 'station'
    SI_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Station_Name = db.Column(db.String(100))
    Station_Code = db.Column(db.String(20), unique=True)

    def to_dict(self):
        return {
            'SI_No': self.SI_No,
            'Station_Name': self.Station_Name,
            'Station_Code': self.Station_Code
        }

class Signup(db.Model):
    _tablename_ = 'signup'
    SI_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Ph_No = db.Column(db.BigInteger, unique=True)
    Station_Code = db.Column(db.String(20), db.ForeignKey('station.Station_Code'), nullable=True)
    Type_of_User = db.Column(db.String(50))
    Password = db.Column(db.String(100))
    Name = db.Column(db.String(100))

    def to_dict(self):
        return {
            'SI_No': self.SI_No,
            'Ph_No': self.Ph_No,
            'Station_Code': self.Station_Code,
            'Type_of_User': self.Type_of_User,
            'Name': self.Name
        }

# ------------------- ROUTES -------------------

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the JWT-Protected Train API!"})

@app.route('/stations')
def show_stations():
    stations = Station.query.all()
    return jsonify([station.to_dict() for station in stations])

# ------------------- SIGNUP -------------------

@app.route('/signup', methods=['POST'])
def create_signup():
    data = request.get_json()

    phone = data.get('Ph_No')
    password = data.get('Password')
    name = data.get('Name')
    station_code = data.get('Station_Code')
    user_type = data.get('Type_of_User')

    if not is_valid_phone(phone):
        return jsonify({'error': 'Phone number must be a 10-digit number.'}), 400

    if not is_valid_password(password):
        return jsonify({
            'error': 'Password must be at least 8 characters and include an uppercase, lowercase, digit, and special character.'
        }), 400

    if Signup.query.filter_by(Ph_No=phone).first():
        return jsonify({'error': 'Phone number already registered.'}), 409

    hashed_password = hash_password_sha1(password)

    try:
        new_user = Signup(
            Ph_No=phone,
            Station_Code=station_code,
            Type_of_User=user_type,
            Password=hashed_password,
            Name=name
        )
        db.session.add(new_user)
        db.session.commit()

        # Use consistent JWT token generation (same as login)
        token = jwt.encode({
            'user_id': new_user.SI_No,
            'exp': datetime.utcnow() + timedelta(hours=2)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user': new_user.to_dict(),
            'access_token': token
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Signup failed: {str(e)}"}), 500

# ------------------- LOGIN -------------------

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    phone = data.get("Ph_No")
    password = data.get("Password")

    user = Signup.query.filter_by(Ph_No=phone).first()

    if user and user.Password == hash_password_sha1(password.strip()):
        try:
            token = jwt.encode({
                'user_id': user.SI_No,
                'exp': datetime.utcnow() + timedelta(hours=2)
            }, app.config['SECRET_KEY'], algorithm="HS256")

            if isinstance(token, bytes):
                token = token.decode('utf-8')

            return jsonify({
                "status": "success",
                "message": f"Welcome {user.Name}!",
                "access_token": token,
                "user": user.to_dict()
            }), 200
        except Exception as e:
            return jsonify({'error': f"Token generation failed: {str(e)}"}), 500

    return jsonify({
        "status": "error",
        "message": "Invalid phone number or password"
    }), 401


# ------------------- TRAIN DATA (PROTECTED) -------------------


# Define Goodstrain model for fetching train data
class Goodstrain(db.Model):
    __tablename__ = 'goodstrains'
    Sl_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Train_Name = db.Column(db.String(50))
    Train_Status = db.Column(db.String(20))

    def to_dict(self):
        return {
            'sl_no': self.Sl_No,
            'name': self.Train_Name,
            'status': self.Train_Status
        }

@app.route('/trains', methods=['GET'])
@token_required
def get_trains(current_user):
    # Fetch train data from the goodstrain table
    trains = Goodstrain.query.all()
    # Get current time in HH:MM AM/PM format
    now = datetime.now().strftime('%I:%M %p')
    train_list = []
    for train in trains:
        train_dict = train.to_dict()
        train_dict['time'] = now  # Always use current time
        train_list.append(train_dict)

    # Get the user's station name
    station_name = None
    if current_user.Station_Code:
        station = Station.query.filter_by(Station_Code=current_user.Station_Code).first()
        if station:
            station_name = station.Station_Name

    return jsonify({
        'trains': train_list,
        'station_name': station_name
    }), 200

# ------------------- PROFILE (PROTECTED) -------------------

@app.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({
        "status": "success",
        "user": current_user.to_dict()
    })

# ------------------- MAIN -------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)