from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db
from sqlalchemy import text
import secrets

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['csrf_token'] = secrets.token_hex(16)

        if not username or not password:
            flash('Please fill in all fields.')
            return redirect(url_for('auth.login'))

        query = text("SELECT * FROM users WHERE username=:username;")
        result = db.session.execute(query, {"username": username})
        user = result.fetchone()

        if not user:
            flash('Username does not exist.')
            return redirect(url_for('auth.login'))

        if user and check_password_hash(user._asdict()['password_hash'], password):
            flash('Logged in successfully!', category='success')
            session['user_id'] = user._asdict()['id']
            return redirect(url_for('main.home'))

        else:
            flash('Incorrect password, try again.')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    session.pop('user_id')
    flash(message='Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Please fill in all fields.')
            return redirect(url_for('auth.register'))

        query = text("SELECT * FROM users WHERE username=:username;")
        result = db.session.execute(query, {"username": username})
        user = result.fetchone()

        if user and user._asdict():
            flash('Username already exists.')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password, method='scrypt')
        query = text("""
        INSERT INTO users (username, password_hash) 
        VALUES (:username, :password_hash);
        """)
        db.session.execute(query, {"username": username, "password_hash": hashed_password})
        db.session.commit()

        flash('Account created successfully!', category='success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')
