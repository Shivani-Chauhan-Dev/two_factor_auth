from flask import Flask, request, jsonify
from functools import wraps
import jwt
from app.model.user import User
import bcrypt
import datetime
from . import bp

secret_key="this is secret"
app = Flask(__name__)
app.config['secret_key'] = secret_key

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        # print(auth_header)
        if auth_header:
            try:
                token = auth_header.split()[1]
            except IndexError:
                return jsonify({'error': 'Token format is invalid'}), 400
        else:
            return jsonify({'error':'Token is missing'}), 403

        try:
            jwt.decode(token, app.config['secret_key'], algorithms="HS256")
        except Exception as error:
           return jsonify({'error': 'token is invalid/expired'})
        return f(*args, **kwargs)

    return decorated


@bp.route("/logging", methods=["POST"])
def user_login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password are required"}), 400

    email = data["email"]
    password = data["password"]
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "Invalid email or password"}), 401
    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return jsonify({"message": "Invalid email or password"}), 401
    token = jwt.encode({'user': user.email,'id': user.id,'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(seconds=3600)}, app.config['secret_key'])
    # return jsonify(token)

    return jsonify({
        "message": "Login successful",
        "token": token,
        # "user": user.to_dict()  
    }), 200