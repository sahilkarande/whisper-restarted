# app/routes_flask.py

from flask import Blueprint, render_template, request, redirect, session, url_for
from app.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

routes = Blueprint('routes', __name__)

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return redirect('/admin' if user.is_admin else '/dashboard')
        return "Invalid credentials"
    return render_template('login.html')

@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'], method='sha256')
        user = User(username=request.form['username'], email=request.form['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('signup.html')

@routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('is_admin'):
        return redirect('/login')
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@routes.route('/admin')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect('/login')
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)
