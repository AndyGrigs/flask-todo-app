from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Task
from app import db

# Створюємо Blueprint
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

# Головна сторінка з завданнями
@main.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', tasks=tasks)

# Сторінка реєстрації
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Перевірка, чи існує користувач
        if User.query.filter_by(username=username).first():
            flash('Користувач з таким іменем вже існує!')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Користувач з таким email вже існує!')
            return redirect(url_for('auth.register'))
        
        # Створення нового користувача
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Реєстрація успішна! Тепер ви можете увійти.')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

# Сторінка входу
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Неправильне ім\'я користувача або пароль!')
    
    return render_template('login.html')

# Вихід
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))