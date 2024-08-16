import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory, session
from models import db, User, Comment, Article
from sqlalchemy import text
import hashlib

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///data.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    app.config['SECRET_KEY'] = 'aaa'
    # SESSION_COOKIE_HTTPONLY=True,
    # REMEMBER_COOKIE_HTTPONLY=True,
    # SESSION_COOKIE_SAMESITE="Strict",

    # Inicjalizacja bazy danych
    db.init_app(app)

    with app.app_context():
        db.create_all()


    @app.route('/')
    def home():
        return render_template('index.html')
    
    
    @app.route('/sqli')
    def sqli():
        return render_template('sqli.html')


    @app.route('/search_suggestions', methods=['GET'])
    def search_suggestions():
        query = request.args.get('query', '')

        if query:
            try:
                sql_query = text(f"SELECT id, title, url FROM articles WHERE title LIKE '%{query}%'")
                results = db.session.execute(sql_query)
                articles = [{'id': row.id, 'title': row.title, 'url': row.url} for row in results]

                if articles:
                    return jsonify(articles)
                else:
                    return jsonify({'message': 'There is no such article!'})
                
            except Exception as e:
                app.logger.error(f"Error executing query: {e}")
                return jsonify({'error': 'An error occurred while fetching suggestions.'}), 500

        return jsonify([])


    @app.route('/broken_acc', methods=['GET'])
    def broken_acc():
        if 'username' not in session:
            flash('You must be logged in to view this page.')
            return redirect(url_for('login'))

        # Pobieramy 'search' z URL
        query = request.args.get('search')

        if query in ['1', '2', '3', '4']:
            return render_template('search.html', query=query)
        elif query == '31':
            return "Oh no! There are a few endpoints left that should no longer be accessible. Good job! Here's your flag: flag={k1nda_sus}"
        else:
            return render_template('broken_acc.html')  

    
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
    

    @app.route('/about')
    def about():
        return render_template('about.html')


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(login=username).first()
            hashed_password = hashlib.md5(password.encode()).hexdigest()

            if user and user.password == hashed_password:
                session['username'] = username
                session['is_admin'] = user.is_admin
                return redirect(url_for('login', user=username))
            
            else:
                flash('Invalid username or password')
                return redirect(url_for('login'))

        user_param = request.args.get('user')
        user_param_lower = user_param.lower() if user_param else None

        if 'username' in session:
            if session.get('is_admin'):
                if user_param == 'admin':
                    return render_template('login.html', admin_message="Oh no! Admin forget to change his password!\n Here's your flag: flag={g0t_ya}")
            
            if user_param_lower == 'administrator':
                users = User.query.all()
                return render_template('login.html', users=users, user=session.get('username'))
            else:
                return render_template('login.html', user=session.get('username'))

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
        
    return app