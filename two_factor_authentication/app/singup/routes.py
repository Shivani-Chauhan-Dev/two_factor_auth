from database.database import db
from app.model.user import User
from flask import request, jsonify
from . import bp
import bcrypt
import pyotp


@bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    otp_secret = pyotp.random_base32()

    # Create new user
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        otp_secret=otp_secret
    )
    db.session.add(new_user)
    db.session.commit()
    otp = pyotp.TOTP(otp_secret).now()

    return jsonify({
        "message": "User created successfully",
        "otp": otp,          
        "note": "This OTP is valid for 30 seconds"
    }), 201

@bp.route('/verify_2fa', methods=['POST'])
def verify_2fa():
    data = request.json
    email = data.get('email')
    token = data.get('token')

    if not email or not token:
        return jsonify({"message": "Missing email or OTP token"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    totp = pyotp.TOTP(user.otp_secret)
    if totp.verify(token, valid_window=1): 
        return jsonify({"message": "OTP verified successfully"}), 200
    else:
        return jsonify({"message": "Invalid or expired OTP"}), 401
    


