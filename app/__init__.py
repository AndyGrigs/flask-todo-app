from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.routes import main, auth

import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Конфігурація
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://todouser:todopass@localhost:5432/todoapp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Ініціалізація розширень
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Будь ласка, увійдіть для доступу до цієї сторінки.'
    
    # Завантаження користувача для Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    # Створення таблиць
    with app.app_context():
        db.create_all()

    return app

# Реєстрація Blueprint'ів
    