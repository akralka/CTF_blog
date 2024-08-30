import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory, session
from models import db, User, Comment, Article
from sqlalchemy import text
from lxml import etree
import hashlib

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///data.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    app.config['SECRET_KEY'] = 'jksdfk484lsgvsrg89sgeu9fno'
    FLAG_FILE = '/flag.txt'
    # SESSION_COOKIE_HTTPONLY=True,
    # REMEMBER_COOKIE_HTTPONLY=True,
    # SESSION_COOKIE_SAMESITE="Strict",

    db.init_app(app)

    def initialize_articles():
        articles = [
            {"title": "XSS - cross-site scripting", "url": "/xss"},
            {"title": "XXE - XML external entity injection", "url": "/xxe"},
            {"title": "Broken Access Control", "url": "/broken_acc"},
            {"title": "SQL Injection", "url": "/sqli"},
        ]

        for article_data in articles:
            article = Article(title=article_data["title"], url=article_data["url"])
            db.session.add(article)
        db.session.commit()

    def initialize_users():
        if not os.path.isfile('.env'):
            return
        users = [
            {
                "login": os.getenv("ADMIN_LOGIN"),
                "password": hashlib.md5(os.getenv("ADMIN_PASSWORD").encode()).hexdigest(),
                "is_admin": os.getenv("ADMIN_IS_ADMIN") == 'True'
            },
            {
                "login": os.getenv("ADMIN2_LOGIN"),
                "password": hashlib.md5(os.getenv("ADMIN2_PASSWORD").encode()).hexdigest(),
                "is_admin": os.getenv("ADMIN2_IS_ADMIN") == 'True'
            },
            {
                "login": os.getenv("SECRET_LOGIN"),
                "password": os.getenv("SECRET_PASSWORD"),
                "is_admin": os.getenv("SECRET_IS_ADMIN") == 'True'
            }
        ]

        for user_data in users:
            if not User.query.filter_by(login=user_data["login"]).first():
                user = User(
                    login=user_data["login"],
                    password=user_data["password"],
                    is_admin=user_data["is_admin"]
                )
                db.session.add(user)
        db.session.commit()

    with app.app_context():
        db.create_all()

        if db.session.query(Article).count() == 0:
            initialize_articles()

        if not User.query.first():
            initialize_users()

    def get_flag(key):
        flags_file = '.n'

        if not os.path.exists(flags_file):
            raise FileNotFoundError(f"File not found.")

        with open(flags_file, 'r') as file:
            for line in file:
                if line.startswith(key + '='):
                    return line.split('=', 1)[1].strip()
        
        raise KeyError(f"Value not found.")

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

        query = request.args.get('search')

        if query in ['1', '2', '3', '4']:
            return render_template('search.html', query=query)
        elif query == '31':
            flag = get_flag('endpoint')
            return "Oh no! There are a few endpoints left that should no longer be accessible. Good job! Here's your flag: flag={" + f"{flag}" + "}" 
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


    @app.route('/xxe', methods=['GET', 'POST'])
    def xxe():
        if request.method == 'POST':
            xml_data = request.data.decode('utf-8')

            try:
                parser = etree.XMLParser(resolve_entities=True)
                root = etree.fromstring(xml_data.encode(), parser)

                result = etree.tostring(root, encoding='unicode')
                return jsonify({"result": result})
            
            except etree.XMLSyntaxError as e:
                return jsonify({"error": f"Error parsing XML: {str(e)}"}), 400

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
                    flag = get_flag('admin_flag')
                    return render_template('login.html', admin_message="Oh no! Admin forget to change his password!\n Here's your flag: flag={" + f"{flag}" + "}")
                
            if user_param_lower == 'administrator':
                users = User.query.all()
                flag = get_flag('administrator')
                return render_template('login.html', users=users, user=session.get('username'), admin_message="Oh no! The administrator does not follow the rule of strong passwords!\n Here's your flag: flag={" + f"{flag}" + "}")
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

            hashed_password = hashlib.md5(password.encode()).hexdigest()
            new_user = User(login=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('User added successfully')
            return redirect(url_for('sign_in'))
        else:
            return render_template('sign_in.html')
    
    @app.route('/change_password', methods=['GET', 'POST'])
    def change_password():
        if 'username' not in session:
            flash('You must be logged in to change your password.')
            return redirect(url_for('login'))

        if request.method == 'POST':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')

            user = User.query.filter_by(login=session['username']).first()
            hashed_current_password = hashlib.md5(current_password.encode()).hexdigest()

            if user.password != hashed_current_password:
                flash('Current password is incorrect.')
                return redirect(url_for('change_password'))

            user.password = hashlib.md5(new_password.encode()).hexdigest()
            db.session.commit()

            flash('Password updated successfully.')

        return render_template('change_password.html')

    @app.route('/uploads/<filename>')
    def photo_display(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


    @app.route('/upload_file', methods=['POST'])
    def upload_file():
        if 'username' not in session or not session.get('is_admin'):
            flash('You do not have the necessary permissions to perform this action.')
            return redirect(url_for('broken_acc', search='4'))

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('broken_acc', search='4'))
                      
        if file and file.filename:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if not filename.endswith('.png'):
                flag = get_flag('upload')
                return redirect(url_for('broken_acc', search='4', upload_message='flag={' + f'{flag}' + '}'))
            else:
                return redirect(url_for('broken_acc', search='4', upload_message='File uploaded successfully!'))
            
        else:
            return redirect(url_for('broken_acc', search='4', upload_message='Invalid file type. Only .png files are allowed.'))

    return app