import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from models import db, User, Comment 
from sqlalchemy import text


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///data.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    app.config['SECRET_KEY'] = 'aaa'

    # Inicjalizacja bazy danych
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/xss', methods=['GET', 'POST'])
    def xss():
        if request.method == 'POST':
            name = request.form['name']
            content = request.form['content']
            if name and content:
                new_comment = Comment(name=name, content=content)
                db.session.add(new_comment)
                db.session.commit()
                return redirect(url_for('xss'))

        comments = Comment.query.order_by(Comment.id.desc()).all()
        return render_template('xss.html', comments=comments)

    @app.route('/xxe')
    def xxe():
        return render_template('xxe.html')

    @app.route('/<query>')
    def search_result(query):
        if query in ['1', '2', '3', '4']:
            return render_template('search.html', query=query)
        else:
            return "Page not found", 404
    
    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            # Podatne na SQL injection zapytanie do bazy danych
            # query = text("SELECT login FROM users WHERE login = ", username)
            query = text(f"SELECT login FROM users WHERE login = '{username}'")
            result = db.session.execute(query)
            user = result.fetchone()

            if user:
                user = User.query.filter_by(login=username).first()
                if user and user.password == password:
                    return redirect(url_for('admin_account'))
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
    
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    @app.route('/admin_account')
    def admin_account():
        return "Oh no! Admin forget to change his password!\n Here's your flag: flag={g0t_ya}"
        
    return app