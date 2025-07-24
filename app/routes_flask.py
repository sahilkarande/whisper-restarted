# routes_flask.py
from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

flask_routes = Blueprint("flask_routes", __name__)

# Home route
@flask_routes.route('/')
def home():
    return render_template("login.html")

# Signup route
@flask_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for('flask_routes.signup'))

        # Check if username or email already exists
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or Email already exists")
            return redirect(url_for('flask_routes.signup'))

        hashed_password = generate_password_hash(password)

        user = User(
            full_name=full_name,
            username=username,
            email=email,
            phone=phone,
            password_hash=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        flash("Signup successful. Please login.")
        return redirect(url_for('flask_routes.login'))

    return render_template("signup.html")

# Login route
@flask_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash("Login successful!")

            if user.is_admin:
                return redirect(url_for('flask_routes.admin_dashboard'))
            else:
                return redirect(url_for('flask_routes.user_dashboard'))

        flash("Invalid username or password")
        return redirect(url_for('flask_routes.login'))

    return render_template("login.html")

# User Dashboard
@flask_routes.route('/dashboard/user')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('flask_routes.login'))

    user = User.query.get(session['user_id'])
    return render_template("user_dashboard.html", user=user)

# Admin Dashboard
@flask_routes.route('/dashboard/admin')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('flask_routes.login'))

    users = User.query.all()
    return render_template("admin_dashboard.html", users=users)

# Logout
@flask_routes.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('flask_routes.login'))
