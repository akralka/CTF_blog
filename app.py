import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User
from sqlalchemy import text


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///data.db" #db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")  # potem bez os bo bedą widzieli
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'aaa'

    # Inicjalizacja bazy danych
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            # Podatne na SQL injection zapytanie do bazy danych
            query = text(f"SELECT login FROM users WHERE login = '{username}'")
            result = db.session.execute(query)
            user = result.fetchone()

            if user:
                user = User.query.filter_by(login=username).first()
                if user and user.password == password:
                    return redirect(url_for('success'))
                else:
                    flash('Invalid password')
            else:
                flash('Invalid username')

            return redirect(url_for('home'))
        else:
            return render_template('login.html')

    @app.route('/sign_in', methods=['GET', 'POST'])
    def sign_in():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            existing_user = User.query.filter_by(login=username).first()
            if existing_user:
                flash('This login is already taken. Please choose another one.')
                return redirect(url_for('sign_in'))

            # Dodanie użytkownika do bazy danych
            new_user = User(login=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            flash('User added successfully')
            return redirect(url_for('home'))
        else:
            return render_template('sign_in.html')

    @app.route('/success')
    def success():
        return 'Login successful! Welcome to the application.'

    return app