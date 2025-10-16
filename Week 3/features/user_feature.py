from main.models import User
from werkzeug.security import check_password_hash, generate_password_hash
from .extensions import db

class UserService:
    @staticmethod
    def create_user(email: str, password: str) -> User:
        hashed = generate_password_hash(password)
        user = User(email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update_password(user_email: str, new_password: str) -> User | None:
        user = User.query.filter_by(email=user_email).first()
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return user
    
    @staticmethod
    def verify_user(user_email: str, password: str) -> bool:
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return False
        return check_password_hash(user.password, password) 
    
    @staticmethod
    def get_role(user_email: str) -> str | None:
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return False
        return user.role
    
    @staticmethod
    def get_id(user_email: str) -> int | None:
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return False
        return user.id