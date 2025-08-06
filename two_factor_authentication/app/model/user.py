from database.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    otp_secret = db.Column(db.String(16), nullable=False)  # For 2FA
    is_verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
    



