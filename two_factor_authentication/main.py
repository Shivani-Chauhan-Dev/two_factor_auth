from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from database.database import db
from flask import Blueprint
from app.singup import bp as user_bp
from app.auth import bp as auth_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "secret_key"
    app.config["SECRET_KEY"] = "your_jwt_secret_key"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True,port=5006)
