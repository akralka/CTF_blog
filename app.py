import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
from models import db, User, Comment 
from sqlalchemy import text
import hashlib


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

    @app.route('/broken_acc')
    def broken_acc():
        if 'username' in session:
            return render_template('broken_acc.html')
        else:
            flash('You must be logged in to view this page.')
            return redirect(url_for('login'))


    @app.route('/<query>')
    def search_result(query):
        if query in ['1', '2', '3', '4']:
            if 'username' in session:
                return render_template('search.html', query=query)
            else:
                flash('You must be logged in to view this page.')
                return redirect(url_for('login'))
        if query in ['31']:
            return "Oh no! There are a few endpoints left that should no longer be accessible. Good job! Here's your flag: flag={k1nda_sus}"
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

            # query = text(f"SELECT login FROM users WHERE login = '{username}'")
            # result = db.session.execute(query)
            # user = result.fetchone()
            user = User.query.filter_by(login=username).first()

            hashed_password = hashlib.md5(password.encode()).hexdigest()

            if user:
                if user and user.password == hashed_password:
                    session['username'] = username 
                    session['is_admin'] = user.is_admin 

                    if user.login == "admin":
                        return redirect(url_for('admin_account'))
                    
                    return redirect(url_for('broken_acc'))
                
                else:
                    flash('Invalid password')
            else:
                flash('Invalid username')

            return redirect(url_for('login'))
        else:
            return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        flash('You have been logged out.')
        return redirect(url_for('login'))


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
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            new_user = User(login=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('User added successfully')
            return redirect(url_for('sign_in'))
        else:
            return render_template('sign_in.html')
    
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    @app.route('/admin_account')
    def admin_account():
        return "Oh no! Admin forget to change his password!\n Here's your flag: flag={g0t_ya}"
        
    return app